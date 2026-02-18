"""
Vibium-based lead creation automation using CSV seed data.

Flow:
1) Load lead cases from CSV.
2) Log in to Re:catch using credentials from local text file.
3) Open create-lead modal and fill mapped fields.
4) Create lead and verify by searching created title.

Constraints:
- Vibium only (no Selenium/WebDriver/Playwright).
- Credentials are not hardcoded.
- Coordinate click fallback is available when selector click fails.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

import vibium

from lead_seed_loader import (
    LeadFormVariables,
    build_form_variables,
    load_lead_seed_records,
    select_records,
)
from lead_form_selector import ensure_lead_form_ready
from lead_form_title import set_required_title_field
from recatch_auth import LoginCredential, ensure_recatch_login, parse_credential_file


LOG_FILE_PATH: str | None = None


K_LEAD_BTN = "\ub9ac\ub4dc"
K_CREATE_MENU = "\ub9ac\ub4dc \uc0dd\uc131"
K_CREATE_MODAL_TITLE = "\uc0c8\ub85c\uc6b4 \ub9ac\ub4dc \uc0dd\uc131"
K_CREATE_BUTTON = "\uc0dd\uc131"
K_SEARCH_PLACEHOLDER = "\uac80\uc0c9"

K_LABEL_NAME = "\uc131\uba85"
K_LABEL_QA_EMAIL = "QA-\uc774\uba54\uc77c"
K_LABEL_TEST_EMAIL = "\ud14c\uc2a4\ud2b8(\uc774\uba54\uc77c)"
K_LABEL_PHONE = "\uc804\ud654\ubc88\ud638"
K_LABEL_TEST_PHONE = "\ud14c\uc2a4\ud2b8(\uc804\ud654\ubc88\ud638)"
K_LABEL_QA_URL = "QA-URL"
K_LABEL_TEST_DOMAIN = "\ud14c\uc2a4\ud2b8(\ub3c4\uba54\uc778)"
K_LABEL_AMOUNT = "\uae08\uc561"


@dataclass
class CaseRunResult:
    case_id: str
    title: str
    created: bool
    verified: bool
    expected_create_success: bool
    passed: bool
    details: str


def init_log_file() -> None:
    global LOG_FILE_PATH
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    LOG_FILE_PATH = os.path.join(logs_dir, f"run-{ts}.log")


def log(message: str) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"
    try:
        print(line)
    except UnicodeEncodeError:
        enc = (sys.stdout.encoding or "utf-8")
        safe = line.encode(enc, errors="replace").decode(enc, errors="replace")
        print(safe)
    if LOG_FILE_PATH:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(line + "\n")


def ask_yes_no(prompt: str, default_yes: bool = True) -> bool:
    if not sys.stdin.isatty():
        return default_yes
    suffix = "[Y/n]" if default_yes else "[y/N]"
    raw = input(f"{prompt} {suffix} ").strip().lower()
    if not raw:
        return default_yes
    return raw in {"y", "yes"}


def save_screenshot(session: "vibium.browser_sync.VibeSync", step_name: str) -> None:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_step = step_name.replace(" ", "_")
    filename = f"shot-{ts}-{safe_step}.png"
    data = session.screenshot()
    with open(filename, "wb") as file:
        file.write(data)
    log(f"screenshot saved: {os.path.abspath(filename)}")


def unwrap_eval(value: Any) -> Any:
    if isinstance(value, dict):
        if set(value.keys()) == {"type", "value"}:
            return unwrap_eval(value["value"])
        return {k: unwrap_eval(v) for k, v in value.items()}

    if isinstance(value, list):
        # Vibium map-like result: [["key", {"type":"...", "value": ...}], ...]
        if all(
            isinstance(item, list)
            and len(item) == 2
            and isinstance(item[0], str)
            for item in value
        ):
            return {item[0]: unwrap_eval(item[1]) for item in value}
        return [unwrap_eval(item) for item in value]

    return value


def eval_js(session: "vibium.browser_sync.VibeSync", script: str) -> Any:
    return unwrap_eval(session.evaluate(script))


def wait_until(
    predicate: Callable[[], bool],
    timeout_sec: float,
    interval_sec: float = 0.25,
) -> bool:
    end_at = time.time() + timeout_sec
    while time.time() < end_at:
        try:
            if predicate():
                return True
        except Exception:
            pass
        time.sleep(interval_sec)
    return False


def is_leads_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const hasTopActionButton = [...document.querySelectorAll("button")]
    .some((el) => isVisible(el) && el.getBoundingClientRect().top < 220);
  const hasSearchInput = [...document.querySelectorAll("input")]
    .some((el) => isVisible(el) && (el.placeholder || "").includes({K_SEARCH_PLACEHOLDER!r}));

  const spinning = [...document.querySelectorAll(".recatch-ant-spin-spinning, .recatch-ant-spin-dot-spin")]
    .some((el) => isVisible(el));
  const bodyTextLen = ((document.body && document.body.innerText) || "").trim().length;

  return (hasTopActionButton || hasSearchInput) && bodyTextLen > 0 && !spinning;
}})()
""",
    )
    return bool(result)


def resolve_csv_path(raw_csv_path: str) -> Path:
    path = Path(raw_csv_path)
    if path.is_absolute():
        return path
    script_dir = Path(__file__).resolve().parent
    return (script_dir / path).resolve()


def resolve_optional_path(raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path
    script_dir = Path(__file__).resolve().parent
    return (script_dir / path).resolve()


def load_form_variables(csv_path: Path, case_id: str | None, limit: int) -> list[LeadFormVariables]:
    records = load_lead_seed_records(csv_path)
    selected_records = select_records(records, case_id)
    if limit > 0:
        selected_records = selected_records[:limit]
    mapped = [build_form_variables(record) for record in selected_records]

    log(f"CSV loaded: total={len(records)}, selected={len(mapped)}")
    for item in mapped:
        log(
            "selected case: "
            f"case_id={item.case_id}, email={item.contact_email}, "
            f"company={item.company_name}, expected_dynamic_match={item.expected_dynamic_match}, "
            f"expected_create_success={item.expected_create_success}, "
            f"title_should_be_valid={item.title_should_be_valid}, priority={item.priority}"
        )
    return mapped


def click_at(session: "vibium.browser_sync.VibeSync", x: float, y: float) -> dict:
    result = eval_js(
        session,
        f"""
(() => {{
  const x = {x};
  const y = {y};
  const el = document.elementFromPoint(x, y);
  if (!el) return {{ ok: false, reason: "element_not_found" }};

  const events = ["pointerdown", "mousedown", "mouseup", "click"];
  for (const name of events) {{
    el.dispatchEvent(new MouseEvent(name, {{
      bubbles: true,
      cancelable: true,
      clientX: x,
      clientY: y,
      view: window
    }}));
  }}

  return {{
    ok: true,
    tag: el.tagName,
    text: (el.innerText || el.textContent || "").trim().slice(0, 80),
    className: el.className || ""
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def is_create_modal_open(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const modal = [...document.querySelectorAll(".recatch-ant-modal")].find((el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }});
  if (!modal) return false;
  const title = (modal.querySelector(".recatch-ant-modal-title")?.innerText || "").trim();
  return title.includes({K_CREATE_MODAL_TITLE!r});
}})()
""",
    )
    return bool(result)


def open_create_modal(session: "vibium.browser_sync.VibeSync") -> None:
    ready = wait_until(
        lambda: is_leads_page_ready(session),
        timeout_sec=12.0,
        interval_sec=0.2,
    )
    if not ready:
        log("warning: leads page readiness check timed out in open_create_modal; trying create action anyway")

    direct_result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const direct = [...document.querySelectorAll("button")]
    .filter(isVisible)
    .find((b) => {{
      const txt = (b.innerText || b.textContent || "").trim();
      const y = b.getBoundingClientRect().top;
      return txt.includes({K_CREATE_MENU!r}) && y < 180;
    }});

  if (!direct) return {{ ok: false, reason: "direct_create_button_not_found" }};
  direct.click();
  return {{ ok: true }};
}})()
""",
    )
    if isinstance(direct_result, dict) and direct_result.get("ok"):
        opened = wait_until(lambda: is_create_modal_open(session), timeout_sec=6.0, interval_sec=0.2)
        if opened:
            return

    open_result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const buttons = [...document.querySelectorAll("button")]
    .filter(isVisible)
    .map((b) => {{
      const rect = b.getBoundingClientRect();
      return {{
        el: b,
        text: (b.innerText || b.textContent || "").trim(),
        className: b.className || "",
        centerX: rect.left + rect.width / 2,
        centerY: rect.top + rect.height / 2,
        x: rect.left,
        y: rect.top
      }};
    }})
    .filter((x) => x.y < 180);

  const target =
    buttons.find((x) => x.text.includes({K_LEAD_BTN!r}))
    || buttons.find((x) => x.text.includes("由щ뱶") && x.text.includes("?앹꽦"))
    || buttons
      .filter((x) => x.className.includes("primary"))
      .sort((a, b) => b.x - a.x)[0]
    || buttons.sort((a, b) => b.x - a.x)[0];

  if (!target) {{
    return {{
      ok: false,
      reason: "lead_button_not_found",
      candidates: buttons.map((x) => ({{
        text: x.text,
        className: x.className,
        x: x.x,
        y: x.y
      }}))
    }};
  }}

  target.el.click();
  return {{
    ok: true,
    text: target.text,
    centerX: target.centerX,
    centerY: target.centerY
  }};
}})()
""",
    )
    if not isinstance(open_result, dict):
        open_result = {"ok": False, "raw": open_result}

    if not open_result.get("ok"):
        log(f"lead button click failed: {open_result}")
        fallback = eval_js(
            session,
            f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const cands = [...document.querySelectorAll("button.recatch-ant-btn-primary")]
    .filter(isVisible)
    .map((b) => {{
      const r = b.getBoundingClientRect();
      return {{
        text: (b.innerText || b.textContent || "").trim(),
        centerX: r.left + r.width / 2,
        centerY: r.top + r.height / 2,
        y: r.top
      }};
    }})
    .filter((x) => x.y < 180);

  const target = cands.find((x) => x.text.includes({K_LEAD_BTN!r})) || cands[0];
  return target || null;
}})()
""",
        )
        if not isinstance(fallback, dict):
            raise RuntimeError("cannot find lead entry button")
        click_result = click_at(session, fallback["centerX"], fallback["centerY"])
        log(f"lead button coordinate fallback: {click_result}")

    clicked_menu = wait_until(
        lambda: bool(
            eval_js(
                session,
                f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const item = [...document.querySelectorAll("li.recatch-ant-dropdown-menu-item,[role='menuitem']")]
    .filter(isVisible)
    .find((el) => (el.innerText || el.textContent || "").trim().includes({K_CREATE_MENU!r}));
  if (!item) return false;
  item.click();
  return true;
}})()
""",
            )
        ),
        timeout_sec=4.0,
        interval_sec=0.2,
    )
    if not clicked_menu:
        raise RuntimeError("cannot click create menu item")

    opened = wait_until(lambda: is_create_modal_open(session), timeout_sec=6.0, interval_sec=0.2)
    if not opened:
        raise RuntimeError("create modal did not open")


def scroll_modal(session: "vibium.browser_sync.VibeSync", to_top: bool) -> dict:
    if to_top:
        result = eval_js(
            session,
            """
(() => {
  const sc = document.querySelector(".recatch-ant-modal .recatch-record-create-modal");
  if (!sc) return { ok: false, reason: "scroll_container_not_found" };
  sc.scrollTop = 0;
  return { ok: true, scrollTop: sc.scrollTop };
})()
""",
        )
    else:
        result = eval_js(
            session,
            """
(() => {
  const sc = document.querySelector(".recatch-ant-modal .recatch-record-create-modal");
  if (!sc) return { ok: false, reason: "scroll_container_not_found" };
  sc.scrollTop = sc.scrollHeight;
  return { ok: true, scrollTop: sc.scrollTop };
})()
""",
        )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def set_title(session: "vibium.browser_sync.VibeSync", title: str) -> dict:
    scroll_modal(session, to_top=True)
    return set_required_title_field(session, title)


def _normalize_number(value: str) -> str:
    cleaned = re.sub(r"[^\d.-]", "", value)
    return cleaned if cleaned else "0"


def set_modal_field_by_label(session: "vibium.browser_sync.VibeSync", label: str, value: str) -> dict:
    numeric_value = _normalize_number(value)
    locate = eval_js(
        session,
        f"""
(() => {{
  const normalize = (text) => (text || "").replace(/\\s+/g, "").replace(/\\*/g, "").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const modal = [...document.querySelectorAll(".recatch-ant-modal")].find((el) => isVisible(el));
  if (!modal) return {{ ok: false, reason: "modal_not_found", label: {label!r} }};

  const rows = [...modal.querySelectorAll(".sc-d9c25054-1")];
  let row = rows.find((r) => {{
    const labelNode = r.querySelector(".sc-d9c25054-2");
    const txt = normalize(labelNode?.innerText || "");
    return txt.includes(normalize({label!r}));
  }});

  if (!row) {{
    const labelNode = [...modal.querySelectorAll("*")]
      .filter(isVisible)
      .find((el) => {{
        const txt = normalize(el.innerText || el.textContent || "");
        if (!txt) return false;
        if (txt.length > 40) return false;
        return txt.includes(normalize({label!r}));
      }});

    if (labelNode) {{
      row = labelNode.closest("div");
      for (let i = 0; i < 4 && row && row !== modal; i += 1) {{
        if (row.querySelector("[data-field-id], input, textarea")) break;
        row = row.parentElement;
      }}
    }}
  }}

  if (!row) {{
    const top = (modal.innerText || "").split("\\n").map((x) => x.trim()).filter(Boolean).slice(0, 80);
    return {{ ok: false, reason: "row_not_found", label: {label!r}, top }};
  }}

  row.scrollIntoView({{ block: "center" }});
  let valueBox = row.querySelector("[data-field-id]");
  if (!valueBox) {{
    let cursor = row.parentElement;
    for (let i = 0; i < 4 && cursor && cursor !== modal; i += 1) {{
      valueBox = cursor.querySelector("[data-field-id]");
      if (valueBox) break;
      cursor = cursor.parentElement;
    }}
  }}
  if (!valueBox) return {{ ok: false, reason: "value_box_not_found", label: {label!r} }};

  const fieldId = valueBox.getAttribute("data-field-id") || "";
  return {{
    ok: true,
    reason: "value_box_located",
    label: {label!r},
    fieldId,
    selector: `.recatch-ant-modal [data-field-id="${{fieldId}}"]`,
  }};
}})()
""",
    )
    if not isinstance(locate, dict):
        return {"ok": False, "reason": "locate_raw_invalid", "raw": locate}
    if not locate.get("ok"):
        return locate

    field_id = str(locate.get("fieldId") or "").strip()
    if not field_id:
        return {"ok": False, "reason": "field_id_empty", "detail": locate}

    box_selector = f'.recatch-ant-modal [data-field-id="{field_id}"]'
    editor_selector = (
        f'{box_selector} input:not([type="hidden"]), '
        f'{box_selector} textarea, '
        f'{box_selector} [contenteditable="true"]'
    )
    payload = numeric_value if _normalize_text_for_match(label) == _normalize_text_for_match(K_LABEL_AMOUNT) else value

    try:
        box_element = session.find(box_selector, timeout=4000)
        box_element.click(timeout=4000)
        time.sleep(0.05)
        box_element.click(timeout=4000)
    except Exception as exc:
        return {
            "ok": False,
            "reason": "value_box_click_failed",
            "label": label,
            "fieldId": field_id,
            "error": str(exc),
        }

    editor_ready = wait_until(
        lambda: bool(
            eval_js(
                session,
                f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const box = document.querySelector({box_selector!r});
  if (!box) return false;
  const editor = box.querySelector("input:not([type='hidden']), textarea, [contenteditable='true']");
  if (editor && isVisible(editor)) return true;
  const active = document.activeElement;
  return !!(active && box.contains(active) && isVisible(active));
}})()
""",
            )
        ),
        timeout_sec=2.5,
        interval_sec=0.1,
    )
    if editor_ready:
        try:
            session.find(editor_selector, timeout=2500).click(timeout=2500)
            eval_js(
                session,
                f"""
(() => {{
  const editor = document.querySelector({editor_selector!r});
  if (!editor) return false;
  const setInputValue = (el, next) => {{
    const proto = el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const desc = Object.getOwnPropertyDescriptor(proto, "value");
    if (desc && desc.set) desc.set.call(el, next);
    else el.value = next;
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};
  editor.focus();
  if (editor.tagName === "INPUT" || editor.tagName === "TEXTAREA") {{
    setInputValue(editor, "");
  }} else {{
    editor.textContent = "";
    editor.dispatchEvent(new Event("input", {{ bubbles: true }}));
    editor.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }}
  return true;
}})()
""",
            )
            session.find(editor_selector, timeout=2500).type(str(payload), timeout=5000)
            eval_js(
                session,
                f"""
(() => {{
  const editor = document.querySelector({editor_selector!r});
  if (!editor) return false;
  const events = [
    ["keydown", "Enter", "Enter"],
    ["keyup", "Enter", "Enter"],
    ["keydown", "Tab", "Tab"],
    ["keyup", "Tab", "Tab"],
  ];
  for (const [name, key, code] of events) {{
    editor.dispatchEvent(new KeyboardEvent(name, {{ key, code, bubbles: true }}));
  }}
  editor.blur();
  const modalTitle = document.querySelector(".recatch-ant-modal .recatch-ant-modal-title");
  if (modalTitle) modalTitle.dispatchEvent(new MouseEvent("click", {{ bubbles: true }}));
  return true;
}})()
""",
            )
        except Exception as exc:
            log(f"field typing path failed, fallback to native setter: label={label}, error={exc}")

    write = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const setInputValue = (el, next) => {{
    const proto = el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const desc = Object.getOwnPropertyDescriptor(proto, "value");
    if (desc && desc.set) desc.set.call(el, next);
    else el.value = next;
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};
  const normalize = (text) => (text || "").replace(/\\s+/g, "").trim();
  const digitsOnly = (text) => (text || "").replace(/[^\\d]/g, "");

  const modal = document.querySelector(".recatch-ant-modal");
  if (!modal) return {{ ok: false, reason: "modal_not_found_after_click" }};
  const box = modal.querySelector({box_selector!r});
  if (!box) return {{ ok: false, reason: "value_box_missing_after_click", fieldId: {field_id!r} }};

  let editor = box.querySelector("input:not([type='hidden']), textarea, [contenteditable='true']");
  if (!editor || !isVisible(editor)) {{
    const active = document.activeElement;
    if (active && box.contains(active) && isVisible(active)) editor = active;
  }}
  if (!editor || !isVisible(editor)) {{
    const readBack = (box.innerText || "").trim();
    const normalize = (text) => (text || "").replace(/\\s+/g, "").trim();
    const digitsOnly = (text) => (text || "").replace(/[^\\d]/g, "");
    const isAmountByLabel = normalize({label!r}).includes(normalize({K_LABEL_AMOUNT!r}));
    const expectedText = isAmountByLabel ? {numeric_value!r} : {value!r};
    const committed =
      isAmountByLabel
        ? (digitsOnly(readBack).includes(digitsOnly(expectedText)))
        : (normalize(readBack).includes(normalize(expectedText)));
    if (committed) {{
      return {{
        ok: true,
        reason: "committed_without_editor",
        label: {label!r},
        fieldId: {field_id!r},
        editorType: "",
        readBack,
        editorValue: "",
        boxClass: box.className || "",
      }};
    }}
    return {{
      ok: false,
      reason: "editor_not_found_after_click",
      fieldId: {field_id!r},
      boxClass: box.className || "",
      boxText: readBack,
    }};
  }}

  const editorTag = (editor.tagName || "").toUpperCase();
  const editorType = (editor.getAttribute("type") || "").toLowerCase();
  const isAmount = normalize({label!r}).includes(normalize({K_LABEL_AMOUNT!r}));

  editor.focus();
  if (editorTag === "INPUT" || editorTag === "TEXTAREA") {{
    const next = (isAmount || editorType === "number") ? {numeric_value!r} : {value!r};
    setInputValue(editor, next);
  }} else {{
    editor.textContent = {value!r};
    editor.dispatchEvent(new Event("input", {{ bubbles: true }}));
    editor.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }}
  editor.dispatchEvent(new KeyboardEvent("keydown", {{ key: "Enter", code: "Enter", bubbles: true }}));
  editor.dispatchEvent(new KeyboardEvent("keyup", {{ key: "Enter", code: "Enter", bubbles: true }}));
  editor.dispatchEvent(new KeyboardEvent("keydown", {{ key: "Tab", code: "Tab", bubbles: true }}));
  editor.dispatchEvent(new KeyboardEvent("keyup", {{ key: "Tab", code: "Tab", bubbles: true }}));
  editor.blur();

  const readBack = (box.innerText || "").trim();
  const expectedText = (isAmount || editorType === "number") ? {numeric_value!r} : {value!r};
  const committed =
    (isAmount || editorType === "number")
      ? (digitsOnly(readBack).includes(digitsOnly(expectedText)))
      : (normalize(readBack).includes(normalize(expectedText)));

  return {{
    ok: committed,
    reason: committed ? "committed" : "value_not_committed",
    label: {label!r},
    fieldId: {field_id!r},
    editorType,
    readBack,
    editorValue: (editor.value !== undefined ? editor.value : editor.textContent) || "",
    boxClass: box.className || "",
  }};
}})()
""",
    )
    return write if isinstance(write, dict) else {"ok": False, "reason": "write_raw_invalid", "raw": write}


def choose_first_success(
    session: "vibium.browser_sync.VibeSync",
    labels: list[str],
    value: str | None,
) -> dict:
    if value is None:
        return {"ok": False, "reason": "value_is_none"}
    if not str(value).strip():
        return {"ok": False, "reason": "value_is_empty"}

    last: dict = {"ok": False, "reason": "no_label_attempted"}
    for label in labels:
        result = set_modal_field_by_label(session, label, str(value))
        if result.get("ok"):
            return result
        last = result
    return last


def click_create(session: "vibium.browser_sync.VibeSync") -> dict:
    click_result = eval_js(
        session,
        f"""
(() => {{
  const modal = document.querySelector(".recatch-ant-modal");
  if (!modal) return {{ ok: false, reason: "modal_not_found" }};

  const btn = [...modal.querySelectorAll("button")]
    .find((b) => (b.innerText || b.textContent || "").trim() === {K_CREATE_BUTTON!r});
  if (!btn) return {{ ok: false, reason: "create_button_not_found" }};
  if (btn.disabled) {{
    const top = (modal.innerText || "").split("\\n").map((x) => x.trim()).filter(Boolean).slice(0, 25);
    return {{ ok: false, reason: "create_button_disabled", top }};
  }}

  btn.click();
  return {{ ok: true }};
}})()
""",
    )
    if not isinstance(click_result, dict):
        click_result = {"ok": False, "raw": click_result}
    if not click_result.get("ok"):
        return click_result

    closed = wait_until(lambda: not is_create_modal_open(session), timeout_sec=12.0, interval_sec=0.2)
    if not closed:
        detail = eval_js(
            session,
            f"""
(() => {{
  const modal = document.querySelector(".recatch-ant-modal");
  if (!modal) return {{ state: "closed" }};
  const top = (modal.innerText || "").split("\\n").map((x) => x.trim()).filter(Boolean).slice(0, 35);
  const btn = [...modal.querySelectorAll("button")]
    .find((b) => (b.innerText || b.textContent || "").trim() === {K_CREATE_BUTTON!r});
  return {{ state: "open", createDisabled: !!(btn && btn.disabled), top }};
}})()
""",
        )
        return {"ok": False, "reason": "modal_not_closed", "detail": detail}

    return {"ok": True}


def verify_created_by_search(session: "vibium.browser_sync.VibeSync", title: str) -> bool:
    eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const input = [...document.querySelectorAll("input[placeholder={K_SEARCH_PLACEHOLDER!r}]")]
    .filter(isVisible)
    .find((el) => el.getBoundingClientRect().y < 110);
  if (!input) return false;

  input.focus();
  input.value = {title!r};
  input.dispatchEvent(new Event("input", {{ bubbles: true }}));
  input.dispatchEvent(new KeyboardEvent("keydown", {{ key: "Enter", code: "Enter", bubbles: true }}));
  input.dispatchEvent(new KeyboardEvent("keyup", {{ key: "Enter", code: "Enter", bubbles: true }}));
  return true;
}})()
""",
    )

    return wait_until(
        lambda: bool(eval_js(session, f"(document.body && (document.body.innerText || '').includes({title!r}))")),
        timeout_sec=8.0,
        interval_sec=0.3,
    )


def _normalize_text_for_match(text: str) -> str:
    return re.sub(r"\s+", "", (text or "")).lower()


def _open_lead_drawer_by_title(session: "vibium.browser_sync.VibeSync", title: str) -> dict:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const insideDrawer = (el) => !!el.closest(".recatch-ant-drawer,[class*='drawer']");
  const insideModal = (el) => !!el.closest(".recatch-ant-modal");

  const wanted = ({title!r} || "").trim();
  const rows = [...document.querySelectorAll("[role='row'], .table-view-row, .recatch-ant-table-row, tr")]
    .filter((el) => isVisible(el) && el.getBoundingClientRect().height > 24)
    .filter((el) => !insideDrawer(el) && !insideModal(el))
    .map((row) => {{
      const txt = (row.innerText || row.textContent || "").trim();
      if (!txt || !(txt.includes(wanted))) return null;
      const titleNode =
        [...row.querySelectorAll("span,div,a")]
          .find((el) => (el.innerText || el.textContent || "").trim() === wanted)
        || [...row.querySelectorAll("span,div,a")]
          .find((el) => (el.innerText || el.textContent || "").trim().includes(wanted))
        || row;
      const r = row.getBoundingClientRect();
      return {{ row, titleNode, txt, x: r.x, y: r.y, w: r.width, h: r.height }};
    }})
    .filter(Boolean)
    .sort((a, b) => (a.y - b.y) || (a.txt.length - b.txt.length));

  const picked = rows[0];
  if (!picked) return {{ ok: false, reason: "title_row_not_found", wanted }};

  // Must hover on title/row first, then click the explicit '열기' button.
  [picked.row, picked.titleNode].forEach((target) => {{
    ["pointermove", "mousemove", "mouseenter", "mouseover"].forEach((name) => {{
      target.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true }}));
    }});
  }});

  const openBtn = [...picked.row.querySelectorAll("button, a")]
    .filter(isVisible)
    .find((el) => {{
      const t = (el.innerText || el.textContent || "").trim();
      return t.includes("열기") || t.toLowerCase() === "open";
    }});

  if (!openBtn) {{
    return {{
      ok: false,
      reason: "open_button_not_found",
      clickedText: picked.txt.slice(0, 140),
      rowTop: picked.y,
    }};
  }}

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    openBtn.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true }}));
  }});
  openBtn.click();
  return {{
    ok: true,
    clickedText: picked.txt.slice(0, 140),
    x: picked.x,
    y: picked.y,
    openButtonText: (openBtn.innerText || openBtn.textContent || "").trim(),
  }};
}})()
""",
    )
    if not isinstance(result, dict):
        return {"ok": False, "raw": result}

    opened = wait_until(
        lambda: bool(
            eval_js(
                session,
                """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const panel = [...document.querySelectorAll(".recatch-ant-drawer-content-wrapper")]
    .find((el) => isVisible(el) && el.getBoundingClientRect().width > 300);
  const hasRecordId = new URLSearchParams(location.search).has("recordId");
  return !!panel && hasRecordId;
})()
""",
            )
        ),
        timeout_sec=6.0,
        interval_sec=0.2,
    )
    return {**result, "drawerOpened": opened}


def _read_open_drawer_text(session: "vibium.browser_sync.VibeSync") -> dict:
    result = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const panel = [...document.querySelectorAll(".recatch-ant-drawer-content-wrapper")]
    .find((el) => isVisible(el) && el.getBoundingClientRect().width > 300);
  if (!panel) return { ok: false, reason: "drawer_not_open" };

  const body =
    panel.querySelector(".recatch-ant-drawer-body")
    || panel.querySelector(".sc-cce0838e-7")
    || panel;
  if (body && body.scrollHeight > body.clientHeight) {
    body.scrollTop = 0;
  }
  const textTop = (panel.innerText || "").trim();
  if (body && body.scrollHeight > body.clientHeight) {
    body.scrollTop = body.scrollHeight;
  }
  const textBottom = (panel.innerText || "").trim();

  const merged = (textTop + "\\n" + textBottom).trim();
  return {
    ok: true,
    text: merged,
    len: merged.length,
    mode: "drawer",
    bodyScrollTop: body?.scrollTop ?? null,
  };
})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def _close_open_drawer(session: "vibium.browser_sync.VibeSync") -> bool:
    eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const panel = [...document.querySelectorAll(".recatch-ant-drawer-content-wrapper")]
    .find((el) => isVisible(el) && el.getBoundingClientRect().width > 300);
  if (!panel) return false;

  const pr = panel.getBoundingClientRect();
  const headerButtons = [...panel.querySelectorAll("button")]
    .filter(isVisible)
    .filter((b) => {
      const r = b.getBoundingClientRect();
      return r.y < pr.top + 70;
    })
    .sort((a, b) => a.getBoundingClientRect().x - b.getBoundingClientRect().x);

  const closeBtn = headerButtons[0] || null;
  if (!closeBtn) return false;

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {
    closeBtn.dispatchEvent(new MouseEvent(name, { bubbles: true, cancelable: true }));
  });
  closeBtn.click();
  return true;
})()
""",
    )
    return wait_until(
        lambda: not bool(
            eval_js(
                session,
                """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const panel = [...document.querySelectorAll(".recatch-ant-drawer-content-wrapper")]
    .find((el) => isVisible(el) && el.getBoundingClientRect().width > 300);
  const hasRecordId = new URLSearchParams(location.search).has("recordId");
  return !!panel || hasRecordId;
})()
""",
            )
        ),
        timeout_sec=3.0,
        interval_sec=0.15,
    )


def _verify_in_drawer(
    session: "vibium.browser_sync.VibeSync",
    title: str,
    field_expectations: list[tuple[str, str]],
) -> dict:
    opened = _open_lead_drawer_by_title(session, title)
    if not opened.get("ok") or not opened.get("drawerOpened"):
        return {"ok": False, "reason": "drawer_open_failed", "detail": opened}

    drawer_state = _read_open_drawer_text(session)
    if not drawer_state.get("ok"):
        _close_open_drawer(session)
        return {"ok": False, "reason": "drawer_text_read_failed", "detail": drawer_state}

    drawer_text = str(drawer_state.get("text", ""))
    drawer_norm = _normalize_text_for_match(drawer_text)
    drawer_digits = re.sub(r"[^\d]", "", drawer_text)

    checks: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    for field_name, expected_raw in field_expectations:
        expected = (expected_raw or "").strip()
        if not expected:
            continue

        matched = False
        if field_name == "amount_krw":
            digits = re.sub(r"[^\d]", "", expected)
            matched = bool(digits) and (digits in drawer_digits)
            checks.append({"field": field_name, "expected": expected, "matched": matched, "kind": "digits"})
        elif field_name == "company_website":
            norm_expected = _normalize_text_for_match(expected)
            host_only = _normalize_text_for_match(re.sub(r"^https?://", "", expected).split("/")[0])
            matched = (norm_expected in drawer_norm) or (host_only and host_only in drawer_norm)
            checks.append({"field": field_name, "expected": expected, "matched": matched, "kind": "url"})
        else:
            norm_expected = _normalize_text_for_match(expected)
            matched = bool(norm_expected) and (norm_expected in drawer_norm)
            checks.append({"field": field_name, "expected": expected, "matched": matched, "kind": "text"})

        if not matched:
            mismatches.append({"field": field_name, "expected": expected})

    close_ok = _close_open_drawer(session)
    return {
        "ok": not mismatches,
        "checks": checks,
        "mismatches": mismatches,
        "drawerCloseOk": close_ok,
        "drawerLen": drawer_state.get("len"),
    }


def build_case_title(base_title: str, case_id: str) -> str:
    suffix = dt.datetime.now().strftime("%m%d%H%M%S")
    return f"{base_title}-{case_id}-{suffix}"


def resolve_case_title(record: LeadFormVariables) -> str:
    if not record.title_should_be_valid and not record.title_override:
        return ""

    override = record.title_override.strip()
    if override:
        if override == "__EMPTY__":
            return ""
        if "{suffix}" in override:
            suffix = dt.datetime.now().strftime("%m%d%H%M%S")
            return override.replace("{suffix}", suffix)
        return override

    return build_case_title(record.lead_title, record.case_id)


def to_case_result(
    record: LeadFormVariables,
    title: str,
    created: bool,
    verified: bool,
    details: str,
) -> CaseRunResult:
    passed = (created == record.expected_create_success)
    if passed and record.expected_create_success:
        passed = passed and verified
    if passed and (not created) and record.expected_fail_reason:
        expected = record.expected_fail_reason.lower()
        detail_lower = details.lower()
        if expected == "title_required":
            passed = ("title_required" in detail_lower) or ("title_not_set" in detail_lower)
        else:
            passed = expected in detail_lower
    return CaseRunResult(
        case_id=record.case_id,
        title=title,
        created=created,
        verified=verified,
        expected_create_success=record.expected_create_success,
        passed=passed,
        details=details,
    )


def create_lead_from_record(
    session: "vibium.browser_sync.VibeSync",
    record: LeadFormVariables,
    skip_verify: bool,
    field_plan: str,
) -> CaseRunResult:
    title = resolve_case_title(record)
    log(f"[{record.case_id}] create start: title={title}")

    open_create_modal(session)
    selector_result = ensure_lead_form_ready(
        session=session,
        log=log,
        company_select_text=record.company_select_text,
        contact_select_text=record.contact_select_text,
    )
    log(f"[{record.case_id}] selector result: {selector_result}")
    if not selector_result.get("ok"):
        save_screenshot(session, f"{record.case_id}-selector-failed")
        return to_case_result(
            record=record,
            title=title,
            created=False,
            verified=False,
            details=f"selector_not_ready: {selector_result}",
        )

    title_result = set_title(session, title)
    log(f"[{record.case_id}] set title result: {title_result}")
    if not title_result.get("ok"):
        save_screenshot(session, f"{record.case_id}-title-failed")
        return to_case_result(
            record=record,
            title=title,
            created=False,
            verified=False,
            details=f"title_not_set: {title_result}",
        )
    if bool(title_result.get("hasRequiredError")):
        save_screenshot(session, f"{record.case_id}-title-required-error")
        return to_case_result(
            record=record,
            title=title,
            created=False,
            verified=False,
            details=f"title_required_error: {title_result}",
        )

    mappings_minimal: list[tuple[list[str], str | None, str]] = [
        ([K_LABEL_QA_EMAIL, K_LABEL_TEST_EMAIL], record.contact_email, "contact_email"),
        ([K_LABEL_QA_URL, K_LABEL_TEST_DOMAIN], record.company_website, "company_website"),
        ([K_LABEL_AMOUNT], str(record.amount_krw) if record.amount_krw is not None else None, "amount_krw"),
    ]
    mappings_extended: list[tuple[list[str], str | None, str]] = [
        ([K_LABEL_NAME], record.contact_full_name, "contact_full_name"),
        ([K_LABEL_QA_EMAIL, K_LABEL_TEST_EMAIL], record.contact_email, "contact_email"),
        ([K_LABEL_PHONE, K_LABEL_TEST_PHONE], record.contact_phone or record.contact_mobile, "contact_phone"),
        ([K_LABEL_QA_URL, K_LABEL_TEST_DOMAIN], record.company_website, "company_website"),
        ([K_LABEL_AMOUNT], str(record.amount_krw) if record.amount_krw is not None else None, "amount_krw"),
    ]
    mappings = mappings_minimal if field_plan == "minimal" else mappings_extended
    log(f"[{record.case_id}] field plan: {field_plan}, target_count={len(mappings)}")
    field_expectations: list[tuple[str, str]] = [("title", title)]
    for labels, value, name in mappings:
        result = choose_first_success(session, labels, value)
        log(f"[{record.case_id}] field update {name}: labels={labels}, result={result}")
        if result.get("ok") and value is not None and str(value).strip():
            field_expectations.append((name, str(value)))

    # Guard against title field losing focus/value while editing lower fields.
    title_guard_result = set_title(session, title)
    log(f"[{record.case_id}] title guard result: {title_guard_result}")
    if not title_guard_result.get("ok") or bool(title_guard_result.get("hasRequiredError")):
        save_screenshot(session, f"{record.case_id}-title-guard-failed")
        return to_case_result(
            record=record,
            title=title,
            created=False,
            verified=False,
            details=f"title_guard_failed: {title_guard_result}",
        )

    create_result = click_create(session)
    if not create_result.get("ok"):
        log(f"[{record.case_id}] create failed: {create_result}")
        save_screenshot(session, f"{record.case_id}-create-failed")
        return to_case_result(
            record=record,
            title=title,
            created=False,
            verified=False,
            details=str(create_result),
        )

    verified = True
    verify_detail: dict[str, Any] = {"ok": True, "skipped": bool(skip_verify)}
    if not skip_verify:
        list_found = verify_created_by_search(session, title)
        if not list_found:
            verified = False
            verify_detail = {"ok": False, "reason": "title_not_found_in_list"}
        else:
            verify_detail = _verify_in_drawer(
                session=session,
                title=title,
                field_expectations=field_expectations,
            )
            verified = bool(verify_detail.get("ok"))
        log(f"[{record.case_id}] verify result: {verified}, detail={verify_detail}")

    save_screenshot(session, f"{record.case_id}-created")
    return to_case_result(
        record=record,
        title=title,
        created=True,
        verified=verified,
        details=f"ok: {verify_detail}" if verified else f"verify_failed: {verify_detail}",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CSV-based Re:catch lead automation with credential-file login"
    )
    parser.add_argument("--csv", default="data/lead_seed.csv", help="lead seed CSV path")
    parser.add_argument("--case-id", default=None, help="optional case filter")
    parser.add_argument("--limit", type=int, default=0, help="max cases to run (0 means all)")
    parser.add_argument(
        "--credential-file",
        default="credentials/recatch_login.txt",
        help="credential file path",
    )
    parser.add_argument(
        "--manual-login-fallback",
        action="store_true",
        help="allow manual login if credential login fails",
    )
    parser.add_argument("--headless", action="store_true", help="run headless")
    parser.add_argument(
        "--login-url",
        default="https://test.recatch.cc/login?redirect=/leads",
        help="login URL",
    )
    parser.add_argument(
        "--leads-url",
        default="https://test.recatch.cc/leads",
        help="leads URL",
    )
    parser.add_argument("--skip-verify", action="store_true", help="skip list verification")
    parser.add_argument(
        "--field-plan",
        choices=["minimal", "extended"],
        default="minimal",
        help="field input strategy: minimal for stability, extended for more fields",
    )
    parser.add_argument("--auto-close", action="store_true", help="auto close browser")
    return parser.parse_args()


def main() -> int:
    init_log_file()
    args = parse_args()

    print("=" * 72)
    print("Vibium: CSV lead create + verification")
    print("=" * 72)
    log(f"log file: {LOG_FILE_PATH}")

    csv_path = resolve_csv_path(args.csv)
    credential_path = resolve_optional_path(args.credential_file)
    log(f"csv path: {csv_path}")
    log(f"credential file: {credential_path}")

    credential: LoginCredential | None = None
    if credential_path is not None:
        try:
            credential = parse_credential_file(credential_path)
            log("credential file loaded")
        except Exception as exc:
            if args.manual_login_fallback:
                log(f"credential load failed, manual fallback enabled: {exc}")
            else:
                log(f"credential load failed: {exc}")
                return 1

    manager = vibium.browser_sync()
    session = manager.launch(headless=args.headless)

    try:
        records = load_form_variables(csv_path, args.case_id, args.limit)
        if not records:
            log("no records selected")
            return 0

        log(f"first case snapshot: {asdict(records[0])}")

        ensure_recatch_login(
            session=session,
            login_url=args.login_url,
            leads_url=args.leads_url,
            credential=credential,
            manual_login_fallback=args.manual_login_fallback,
            log=log,
        )

        results: list[CaseRunResult] = []
        for idx, record in enumerate(records, start=1):
            log(f"===== case {idx}/{len(records)}: {record.case_id} =====")
            try:
                # Reset state between cases to avoid leftover filter/drawer/detail context.
                session.go(args.leads_url)
                ready = wait_until(
                    lambda: is_leads_page_ready(session),
                    timeout_sec=15.0,
                    interval_sec=0.25,
                )
                if not ready:
                    log(f"[{record.case_id}] warning: leads page readiness check timed out; continuing anyway")

                result = create_lead_from_record(
                    session=session,
                    record=record,
                    skip_verify=args.skip_verify,
                    field_plan=args.field_plan,
                )
            except Exception as exc:
                save_screenshot(session, f"{record.case_id}-exception")
                result = to_case_result(
                    record=record,
                    title="",
                    created=False,
                    verified=False,
                    details=f"exception: {exc}",
                )
            results.append(result)
            log(f"[{record.case_id}] result: {result}")

        created_count = sum(1 for x in results if x.created)
        verified_count = sum(1 for x in results if x.verified)
        passed_count = sum(1 for x in results if x.passed)
        log(
            "summary: "
            f"total={len(results)}, created={created_count}, verified={verified_count}, passed={passed_count}"
        )
        return 0 if passed_count == len(results) else 1
    except KeyboardInterrupt:
        log("interrupted by user")
        return 130
    except Exception as exc:
        log(f"unhandled exception: {exc}")
        save_screenshot(session, "error-state")
        return 1
    finally:
        should_close = args.auto_close or ask_yes_no("close browser now?", default_yes=False)
        if should_close:
            session.quit()
            log("browser closed")
        else:
            log("browser kept open")


if __name__ == "__main__":
    sys.exit(main())

