from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode, urlparse

import vibium

from recatch_auth import LoginCredential, ensure_recatch_login, is_leads_page_ready, parse_credential_file


LOG_FILE_PATH: str | None = None

NEXT_LABEL = "다음"
UPLOAD_LABEL = "업로드"
CONFIRM_LABEL = "확인"
VALIDATION_OK_TEXT = "데이터에 에러가 없습니다"
UPLOAD_OK_TEXT = "업로드에 성공했습니다."
MAPPING_HINT_TEXT = "모든 필드를 연결하지 않아도"


@dataclass(frozen=True)
class FieldMapping:
    select_index: int
    query: str
    option_text: str
    name: str


DEFAULT_FIELD_MAPPINGS: tuple[FieldMapping, ...] = (
    FieldMapping(select_index=1, query="성명", option_text="성명", name="contact:name"),
    FieldMapping(select_index=2, query="이메일", option_text="이메일", name="contact:email"),
    FieldMapping(select_index=3, query="회사명", option_text="회사명", name="company:name"),
)


def init_log_file() -> None:
    global LOG_FILE_PATH
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE_PATH = str(logs_dir / f"bulk-import-{ts}.log")


def log(message: str) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"
    try:
        print(line)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        safe = line.encode(enc, errors="replace").decode(enc, errors="replace")
        print(safe)
    if LOG_FILE_PATH:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(line + "\n")


def unwrap_eval(value: Any) -> Any:
    if isinstance(value, dict):
        if set(value.keys()) == {"type", "value"}:
            return unwrap_eval(value["value"])
        return {k: unwrap_eval(v) for k, v in value.items()}

    if isinstance(value, list):
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
    predicate,
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


def save_screenshot(session: "vibium.browser_sync.VibeSync", step_name: str) -> str:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_step = step_name.replace(" ", "_")
    file_path = Path.cwd() / f"shot-{ts}-{safe_step}.png"
    data = session.screenshot()
    with open(file_path, "wb") as file:
        file.write(data)
    return str(file_path.resolve())


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (Path(__file__).resolve().parent / path).resolve()


def resolve_optional_path(raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    return resolve_path(raw_path)


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def current_url(session: "vibium.browser_sync.VibeSync") -> str:
    return str(eval_js(session, "location.href"))


def visible_page_excerpt(session: "vibium.browser_sync.VibeSync", limit: int = 25) -> list[str]:
    result = eval_js(
        session,
        f"""
(() => {{
  return ((document.body && document.body.innerText) || "")
    .split("\\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, {limit});
}})()
""",
    )
    return result if isinstance(result, list) else []


def page_contains_text(session: "vibium.browser_sync.VibeSync", text: str) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const body = ((document.body && document.body.innerText) || "")
    .replace(/\\s+/g, " ")
    .trim();
  return body.includes({json.dumps(text, ensure_ascii=False)});
}})()
""",
    )
    return bool(result)


def ensure_import_page_ready(session: "vibium.browser_sync.VibeSync", import_url: str) -> None:
    session.go(import_url)
    ready = wait_until(
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
  return [...document.querySelectorAll("textarea")].some((el) => isVisible(el));
})()
""",
            )
        ),
        timeout_sec=20.0,
        interval_sec=0.25,
    )
    if not ready:
        raise RuntimeError(
            f"import page not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )


def set_textarea_value(session: "vibium.browser_sync.VibeSync", text: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const csvText = {json.dumps(text, ensure_ascii=False)};
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const textarea = [...document.querySelectorAll("textarea")].find((el) => isVisible(el));
  if (!textarea) return {{ ok: false, reason: "textarea_not_found" }};

  const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value")?.set;
  textarea.focus();
  if (setter) setter.call(textarea, csvText);
  else textarea.value = csvText;
  textarea.dispatchEvent(new Event("input", {{ bubbles: true }}));
  textarea.dispatchEvent(new Event("change", {{ bubbles: true }}));
  try {{
    const dt = new DataTransfer();
    dt.setData("text/plain", csvText);
    const pasteEvent = new ClipboardEvent("paste", {{
      bubbles: true,
      cancelable: true,
      clipboardData: dt,
    }});
    textarea.dispatchEvent(pasteEvent);
  }} catch (error) {{
    // Continue even if ClipboardEvent construction is restricted.
  }}
  try {{
    textarea.dispatchEvent(
      new InputEvent("input", {{
        bubbles: true,
        data: csvText,
        inputType: "insertFromPaste",
      }})
    );
  }} catch (error) {{
    textarea.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}
  textarea.dispatchEvent(new Event("change", {{ bubbles: true }}));

  return {{
    ok: true,
    length: textarea.value.length,
    lineCount: textarea.value.split(/\\r?\\n/).length,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def button_state(session: "vibium.browser_sync.VibeSync", label: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const wanted = ((value) => (value || "").replace(/\\s+/g, " ").trim())({json.dumps(label, ensure_ascii=False)});
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const isDisabled = (el) =>
    !!el.disabled
    || el.getAttribute("aria-disabled") === "true"
    || el.classList.contains("recatch-ant-btn-disabled");

  const matches = [...document.querySelectorAll("button, [role='button'], a")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        text: (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim(),
        disabled: isDisabled(el),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text === wanted || item.text.includes(wanted))
    .sort((a, b) => Number(a.disabled) - Number(b.disabled) || a.y - b.y || b.w - a.w);

  if (!matches.length) {{
    return {{ exists: false, enabled: false, matches: [] }};
  }}

  return {{
    exists: true,
    enabled: !matches[0].disabled,
    matches: matches.slice(0, 5),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"exists": False, "enabled": False, "raw": result}


def click_button_by_text(session: "vibium.browser_sync.VibeSync", label: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const wanted = ((value) => (value || "").replace(/\\s+/g, " ").trim())({json.dumps(label, ensure_ascii=False)});
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const isDisabled = (el) =>
    !!el.disabled
    || el.getAttribute("aria-disabled") === "true"
    || el.classList.contains("recatch-ant-btn-disabled");

  const matches = [...document.querySelectorAll("button, [role='button'], a")]
    .filter((el) => isVisible(el) && !isDisabled(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        el,
        text: (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim(),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text === wanted || item.text.includes(wanted))
    .sort((a, b) => a.y - b.y || b.w - a.w);

  const target = matches[0];
  if (!target) {{
    return {{ ok: false, reason: "button_not_found", wanted }};
  }}

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    target.el.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true, view: window }}));
  }});
  target.el.click();

  return {{
    ok: true,
    text: target.text,
    x: target.x,
    y: target.y,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def mapping_page_state(session: "vibium.browser_sync.VibeSync") -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const selectCount = [...document.querySelectorAll(".recatch-ant-select")]
    .filter((el) => isVisible(el)).length;
  const body = ((document.body && document.body.innerText) || "").replace(/\\s+/g, " ").trim();
  return {{
    ready: selectCount >= 4 || body.includes({json.dumps(MAPPING_HINT_TEXT, ensure_ascii=False)}),
    selectCount,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ready": False, "raw": result}


def read_mapping_select_texts(session: "vibium.browser_sync.VibeSync") -> list[str]:
    result = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  return [...document.querySelectorAll(".recatch-ant-select")]
    .filter((el) => isVisible(el))
    .map((el) => (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim());
})()
""",
    )
    return result if isinstance(result, list) else []


def prepare_select_query(
    session: "vibium.browser_sync.VibeSync",
    select_index: int,
    query: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const targetIndex = {select_index};
  const query = {json.dumps(query, ensure_ascii=False)};
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const setInputValue = (el, value) => {{
    const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value")?.set;
    if (setter) setter.call(el, value);
    else el.value = value;
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};

  const selects = [...document.querySelectorAll(".recatch-ant-select")]
    .filter((el) => isVisible(el));
  const select = selects[targetIndex];
  if (!select) {{
    return {{
      ok: false,
      reason: "select_not_found",
      availableCount: selects.length,
      texts: selects.map((el) => (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim()),
    }};
  }}

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    select.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true, view: window }}));
  }});
  select.click();

  const input = select.querySelector("input[type='search']");
  if (!input) {{
    return {{
      ok: false,
      reason: "search_input_not_found",
      selectText: (select.innerText || select.textContent || "").replace(/\\s+/g, " ").trim(),
    }};
  }}

  input.focus();
  setInputValue(input, "");
  setInputValue(input, query);

  return {{
    ok: true,
    inputId: input.id || "",
    selectText: (select.innerText || select.textContent || "").replace(/\\s+/g, " ").trim(),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def locate_dropdown_option(
    session: "vibium.browser_sync.VibeSync",
    select_index: int,
    option_text: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const targetIndex = {select_index};
  const wanted = ({json.dumps(option_text, ensure_ascii=False)} || "").replace(/\\s+/g, " ").trim();
  const wantedParts = wanted.split(">").map((value) => value.trim()).filter(Boolean);
  const groupWanted = wantedParts.length > 1 ? wantedParts[0] : "";
  const leafWanted = wantedParts.length > 1 ? wantedParts[wantedParts.length - 1] : wanted;
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const dropdown = [...document.querySelectorAll(".recatch-ant-select-dropdown")]
    .filter((el) => isVisible(el))
    .sort((a, b) => b.getBoundingClientRect().height - a.getBoundingClientRect().height)[0];
  if (!dropdown) {{
    return {{
      ok: false,
      reason: "dropdown_not_found",
      wanted,
    }};
  }}

  const selects = [...document.querySelectorAll(".recatch-ant-select")]
    .filter((el) => isVisible(el));
  const select = selects[targetIndex];
  const selectRect = select ? select.getBoundingClientRect() : null;

  if (groupWanted) {{
    const groups = [...dropdown.querySelectorAll(".recatch-ant-collapse-item")]
      .filter((el) => isVisible(el))
      .map((el) => {{
        const headerText = normalize(
          el.querySelector(".recatch-ant-collapse-header-text")?.innerText
          || el.querySelector(".recatch-ant-collapse-header")?.innerText
          || ""
        );
        return {{ el, headerText }};
      }});

    const group = groups.find((item) => item.headerText.includes(groupWanted));
    if (group) {{
      const candidateNodes = [...group.el.querySelectorAll("*")]
        .filter((el) => isVisible(el))
        .map((el) => {{
          const rect = el.getBoundingClientRect();
          return {{
            el,
            text: normalize(el.innerText || el.textContent || ""),
            x: rect.left,
            y: rect.top,
            w: rect.width,
            h: rect.height,
          }};
        }})
        .filter((item) => item.text)
        .filter((item) => !item.text.includes(group.headerText))
        .filter((item) => item.text === leafWanted || item.text === `${{leafWanted}}*` || item.text.includes(leafWanted))
        .filter((item) => item.w >= 40 && item.h >= 16)
        .sort((a, b) => {{
          const aExact = Number(a.text === leafWanted || a.text === `${{leafWanted}}*`);
          const bExact = Number(b.text === leafWanted || b.text === `${{leafWanted}}*`);
          return bExact - aExact || a.y - b.y || b.w - a.w;
        }});

      const picked = candidateNodes[0];
      if (picked) {{
        return {{
          ok: true,
          wanted,
          matchedText: picked.text,
          x: picked.x + picked.w / 2,
          y: picked.y + picked.h / 2,
          topCandidates: candidateNodes.slice(0, 5).map((item) => ({{
            text: item.text,
            x: item.x,
            y: item.y,
            w: item.w,
            h: item.h,
          }})),
        }};
      }}
    }}
  }}

  const optionSelectors = [
    ".recatch-ant-select-dropdown .recatch-ant-select-item-option",
    ".recatch-ant-select-dropdown [role='option']",
    ".recatch-ant-select-item-option",
    "[role='option']",
  ];

  const explicitOptions = [...new Set(optionSelectors.flatMap((selector) => [...document.querySelectorAll(selector)]))]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        el,
        text: normalize(el.innerText || el.textContent || ""),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text)
    .filter((item) => item.text === wanted || item.text === `${{wanted}}*` || item.text.includes(wanted));

  const fallbackOptions = [...dropdown.querySelectorAll("*")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        el,
        text: normalize(el.innerText || el.textContent || ""),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
      }};
    }})
    .filter((item) => item.text)
    .filter((item) => item.text === wanted || item.text === `${{wanted}}*`)
    .filter((item) => item.w >= 80 && item.h >= 24)
    .filter((item) => !selectRect || item.y >= selectRect.top - 8);

  const candidates = (explicitOptions.length ? explicitOptions : fallbackOptions)
    .sort((a, b) => {{
      const aExact = Number(a.text === wanted || a.text === `${{wanted}}*`);
      const bExact = Number(b.text === wanted || b.text === `${{wanted}}*`);
      return bExact - aExact || a.y - b.y || b.w - a.w;
    }});

  const picked = candidates[0];
  if (!picked) {{
    return {{
      ok: false,
      reason: "dropdown_option_not_found",
      wanted,
      topCandidates: candidates.slice(0, 5),
    }};
  }}

  return {{
    ok: true,
    wanted,
    matchedText: picked.text,
    x: picked.x + picked.w / 2,
    y: picked.y + picked.h / 2,
    topCandidates: candidates.slice(0, 5).map((item) => ({{
      text: item.text,
      x: item.x,
      y: item.y,
      w: item.w,
      h: item.h,
    }})),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def click_at(session: "vibium.browser_sync.VibeSync", x: float, y: float) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const x = {x};
  const y = {y};
  const el = document.elementFromPoint(x, y);
  if (!el) return {{ ok: false, reason: "element_not_found" }};

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    el.dispatchEvent(new MouseEvent(name, {{
      bubbles: true,
      cancelable: true,
      clientX: x,
      clientY: y,
      view: window,
    }}));
  }});
  if (typeof el.click === "function") {{
    el.click();
  }}

  return {{
    ok: true,
    tag: el.tagName,
    text: (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim().slice(0, 120),
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def leaf_option_text(option_text: str) -> str:
    return option_text.split(">")[-1].strip()


def selected_option_state(
    session: "vibium.browser_sync.VibeSync",
    select_index: int,
    option_text: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const targetIndex = {select_index};
  const wanted = ({json.dumps(option_text, ensure_ascii=False)} || "").replace(/\\s+/g, " ").trim();
  const leafWanted = wanted.split(">").slice(-1)[0].trim();
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const selects = [...document.querySelectorAll(".recatch-ant-select")]
    .filter((el) => isVisible(el));
  const select = selects[targetIndex];
  if (!select) return {{ selected: false, reason: "select_not_found" }};

  const text = normalize(
    select.querySelector(".recatch-ant-select-selection-item")?.innerText
    || select.innerText
    || select.textContent
    || ""
  );

  return {{
    selected: text.includes(wanted) || (leafWanted && text.includes(leafWanted)),
    text,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"selected": False, "raw": result}


def mapping_variants(mapping: FieldMapping) -> list[tuple[str, str]]:
    if mapping.name == "contact:name":
        return [
            ("성명", "연락처 > 성명"),
            ("연락처", "연락처 > 성명"),
            ("성명", "성명"),
        ]
    if mapping.name == "contact:email":
        return [
            ("이메일", "연락처 > 이메일"),
            ("연락처", "연락처 > 이메일"),
            ("이메일", "이메일"),
        ]
    if mapping.name == "company:name":
        return [
            ("회사명", "회사 > 회사명"),
            ("회사", "회사 > 회사명"),
            ("회사명", "회사명"),
        ]
    return [(mapping.query, mapping.option_text)]


def map_field(
    session: "vibium.browser_sync.VibeSync",
    mapping: FieldMapping,
) -> dict[str, Any]:
    last_detail: dict[str, Any] = {"ok": False, "reason": "not_started"}
    attempt = 0
    for query, option_text in mapping_variants(mapping):
        for _ in range(2):
            attempt += 1
            prepared = prepare_select_query(session, mapping.select_index, query)
            if not prepared.get("ok"):
                last_detail = {
                    "attempt": attempt,
                    "stage": "prepare",
                    "query": query,
                    "option_text": option_text,
                    "detail": prepared,
                }
                time.sleep(0.3)
                continue

            time.sleep(0.5)
            located = locate_dropdown_option(session, mapping.select_index, option_text)
            if not located.get("ok"):
                last_detail = {
                    "attempt": attempt,
                    "stage": "locate",
                    "query": query,
                    "option_text": option_text,
                    "detail": located,
                }
                time.sleep(0.3)
                continue

            clicked = click_at(session, float(located["x"]), float(located["y"]))
            selected = wait_until(
                lambda: bool(selected_option_state(session, mapping.select_index, option_text).get("selected")),
                timeout_sec=4.0,
                interval_sec=0.15,
            )
            state = selected_option_state(session, mapping.select_index, option_text)
            if selected:
                return {
                    "ok": True,
                    "attempt": attempt,
                    "query": query,
                    "option_text": option_text,
                    "prepared": prepared,
                    "located": located,
                    "clicked": clicked,
                    "state": state,
                }
            last_detail = {
                "attempt": attempt,
                "stage": "verify",
                "query": query,
                "option_text": option_text,
                "prepared": prepared,
                "located": located,
                "clicked": clicked,
                "state": state,
            }
            time.sleep(0.3)

    return {"ok": False, "mapping": mapping.name, "detail": last_detail}


def apply_default_mappings(session: "vibium.browser_sync.VibeSync") -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for mapping in DEFAULT_FIELD_MAPPINGS:
        result = map_field(session, mapping)
        results.append(result)
        if not result.get("ok"):
            raise RuntimeError(f"mapping failed for {mapping.name}: {result}")
    return results


def wait_for_enabled_button(
    session: "vibium.browser_sync.VibeSync",
    label: str,
    timeout_sec: float,
) -> dict[str, Any]:
    found = wait_until(
        lambda: bool(button_state(session, label).get("enabled")),
        timeout_sec=timeout_sec,
        interval_sec=0.2,
    )
    state = button_state(session, label)
    if not found:
        raise RuntimeError(
            f"button not enabled: label={label}, state={state}, excerpt={visible_page_excerpt(session)}"
        )
    return state


def click_enabled_button(
    session: "vibium.browser_sync.VibeSync",
    label: str,
    timeout_sec: float,
) -> dict[str, Any]:
    wait_for_enabled_button(session, label, timeout_sec)
    result = click_button_by_text(session, label)
    if not result.get("ok"):
        raise RuntimeError(f"button click failed: label={label}, result={result}")
    return result


def count_csv_rows(csv_text: str) -> int:
    lines = [line for line in csv_text.splitlines() if line.strip()]
    if not lines:
        return 0
    return max(len(lines) - 1, 0)


def import_csv_part(
    session: "vibium.browser_sync.VibeSync",
    import_url: str,
    csv_path: Path,
    upload_timeout_sec: float,
) -> dict[str, Any]:
    csv_text = csv_path.read_text(encoding="utf-8")
    row_count = count_csv_rows(csv_text)

    ensure_import_page_ready(session, import_url)
    paste_result = set_textarea_value(session, csv_text)
    if not paste_result.get("ok"):
        raise RuntimeError(f"csv paste failed for {csv_path.name}: {paste_result}")

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)

    mapping_ready = wait_until(
        lambda: bool(mapping_page_state(session).get("ready")),
        timeout_sec=20.0,
        interval_sec=0.2,
    )
    if not mapping_ready:
        raise RuntimeError(
            f"mapping page not ready for {csv_path.name}: excerpt={visible_page_excerpt(session)}"
        )

    mapping_selects = read_mapping_select_texts(session)
    mapping_results = apply_default_mappings(session)

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)
    validation_ok = wait_until(
        lambda: page_contains_text(session, VALIDATION_OK_TEXT),
        timeout_sec=30.0,
        interval_sec=0.2,
    )
    if not validation_ok:
        raise RuntimeError(
            f"validation step failed for {csv_path.name}: excerpt={visible_page_excerpt(session)}"
        )

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)
    click_enabled_button(session, UPLOAD_LABEL, timeout_sec=30.0)

    upload_ok = wait_until(
        lambda: page_contains_text(session, UPLOAD_OK_TEXT),
        timeout_sec=upload_timeout_sec,
        interval_sec=0.5,
    )
    if not upload_ok:
        raise RuntimeError(
            f"upload success text not found for {csv_path.name}: excerpt={visible_page_excerpt(session)}"
        )

    click_enabled_button(session, CONFIRM_LABEL, timeout_sec=20.0)
    leads_ready = wait_until(
        lambda: is_leads_page_ready(session),
        timeout_sec=20.0,
        interval_sec=0.25,
    )
    if not leads_ready:
        raise RuntimeError(
            f"did not return to leads page after {csv_path.name}: url={current_url(session)}"
        )

    return {
        "ok": True,
        "file": csv_path.name,
        "rowCount": row_count,
        "pasteResult": paste_result,
        "mappingSelects": mapping_selects,
        "mappingResults": mapping_results,
    }


def build_default_url(base_url: str, path: str) -> str:
    return f"{base_url}{path}"


def build_leads_path(team_slug: str) -> str:
    query: dict[str, str] = {}
    if team_slug:
        query["teamSlug"] = team_slug
    return "/leads" + (f"?{urlencode(query, quote_via=quote)}" if query else "")


def build_login_url(base_url: str, team_slug: str) -> str:
    query: dict[str, str] = {"redirect": build_leads_path(team_slug)}
    if team_slug:
        query["teamSlug"] = team_slug
    return build_default_url(base_url, f"/login?{urlencode(query, quote_via=quote)}")


def build_leads_url(base_url: str, team_slug: str) -> str:
    return build_default_url(base_url, build_leads_path(team_slug))


def build_import_url(base_url: str, team_slug: str, record_type_id: int) -> str:
    query: dict[str, str | int] = {"recordTypeId": record_type_id}
    if team_slug:
        query["teamSlug"] = team_slug
    return build_default_url(
        base_url,
        f"/leads/import?{urlencode(query, quote_via=quote)}",
    )


def default_state_path(base_url: str, team_slug: str) -> Path:
    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    host = urlparse(base_url).netloc.replace(".", "_").replace(":", "_")
    slug = team_slug or "default"
    return logs_dir / f"bulk-import-state-{host}-{slug}.json"


def load_completed_parts(state_path: Path) -> set[int]:
    if not state_path.exists():
        return set()
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    raw_parts = payload.get("completed_parts", [])
    return {int(part) for part in raw_parts}


def write_state_file(
    state_path: Path,
    base_url: str,
    team_slug: str,
    record_type_id: int,
    start: int,
    end: int,
    completed_parts: set[int],
) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "base_url": base_url,
        "team_slug": team_slug,
        "record_type_id": record_type_id,
        "start": start,
        "end": end,
        "completed_parts": sorted(completed_parts),
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bulk import split lead CSV files into Re:catch with Vibium."
    )
    parser.add_argument("--base-url", default=os.getenv("RECATCH_BASE_URL", ""))
    parser.add_argument(
        "--team-slug",
        default=os.getenv("RECATCH_TEAM_SLUG", ""),
        help="optional team slug for routes that use ?teamSlug=...",
    )
    parser.add_argument(
        "--record-type-id",
        type=int,
        default=int(os.getenv("RECATCH_RECORD_TYPE_ID", "0")),
    )
    parser.add_argument("--login-url")
    parser.add_argument("--leads-url")
    parser.add_argument("--import-url")
    parser.add_argument(
        "--csv-dir",
        default="data/lead_seed_instance_email_50000_csv_split",
        help="directory that contains the split CSV files",
    )
    parser.add_argument(
        "--file-prefix",
        default="lead_seed_instance_email_50000_part_",
        help="file prefix before the 3-digit part number",
    )
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=50)
    parser.add_argument(
        "--credential-file",
        default=os.getenv("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt"),
    )
    parser.add_argument("--manual-login-fallback", action="store_true")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--keep-open", action="store_true")
    parser.add_argument("--delay-between-parts", type=float, default=0.0)
    parser.add_argument("--upload-timeout-sec", type=float, default=300.0)
    parser.add_argument("--state-file")
    parser.add_argument("--skip-completed", action="store_true")
    args = parser.parse_args()

    if not args.base_url:
        parser.error("--base-url or RECATCH_BASE_URL is required")
    if args.start < 1 or args.end < args.start:
        parser.error("--start/--end range is invalid")
    return args


def main() -> int:
    init_log_file()
    args = parse_args()

    base_url = normalize_base_url(args.base_url)
    login_url = args.login_url or build_login_url(base_url, args.team_slug)
    leads_url = args.leads_url or build_leads_url(base_url, args.team_slug)
    import_url = args.import_url or build_import_url(base_url, args.team_slug, args.record_type_id)
    csv_dir = resolve_path(args.csv_dir)
    credential_path = resolve_optional_path(args.credential_file)
    state_path = resolve_optional_path(args.state_file) or default_state_path(base_url, args.team_slug)

    log(f"log file: {LOG_FILE_PATH}")
    log(f"base url: {base_url}")
    log(f"team slug: {args.team_slug}")
    log(f"login url: {login_url}")
    log(f"leads url: {leads_url}")
    log(f"import url: {import_url}")
    log(f"csv dir: {csv_dir}")
    log(f"part range: {args.start}..{args.end}")
    log(f"state file: {state_path}")

    credential: LoginCredential | None = None
    if credential_path is not None:
        try:
            credential = parse_credential_file(credential_path)
            log(f"credential file loaded: {credential_path}")
        except Exception as exc:
            if not args.manual_login_fallback:
                log(f"credential file load failed: {exc}")
                return 1
            log(f"credential file load failed, manual fallback enabled: {exc}")

    completed_parts = load_completed_parts(state_path) if state_path.exists() else set()
    if completed_parts:
        log(f"loaded completed parts from state: {sorted(completed_parts)}")

    manager = vibium.browser_sync()
    session = manager.launch(headless=args.headless)

    try:
        ensure_recatch_login(
            session=session,
            login_url=login_url,
            leads_url=leads_url,
            credential=credential,
            manual_login_fallback=args.manual_login_fallback,
            log=log,
        )

        for part in range(args.start, args.end + 1):
            if args.skip_completed and part in completed_parts:
                log(f"[part {part:03d}] skipped by state file")
                continue

            csv_path = csv_dir / f"{args.file_prefix}{part:03d}.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"csv file not found: {csv_path}")

            log(f"[part {part:03d}] start: {csv_path.name}")
            result = import_csv_part(
                session=session,
                import_url=import_url,
                csv_path=csv_path,
                upload_timeout_sec=args.upload_timeout_sec,
            )
            log(f"[part {part:03d}] done: {result}")

            completed_parts.add(part)
            write_state_file(
                state_path=state_path,
                base_url=base_url,
                team_slug=args.team_slug,
                record_type_id=args.record_type_id,
                start=args.start,
                end=args.end,
                completed_parts=completed_parts,
            )

            if args.delay_between_parts > 0 and part != args.end:
                time.sleep(args.delay_between_parts)

        log(f"completed all requested parts: {sorted(completed_parts)}")
        return 0
    except KeyboardInterrupt:
        log("interrupted by user")
        return 130
    except Exception as exc:
        screenshot = save_screenshot(session, "bulk-import-error")
        log(f"bulk import failed: {exc}")
        log(f"error screenshot: {screenshot}")
        log(f"current url: {current_url(session)}")
        log(f"page excerpt: {visible_page_excerpt(session)}")
        return 1
    finally:
        if args.keep_open:
            log("browser kept open")
        else:
            session.quit()
            log("browser closed")


if __name__ == "__main__":
    sys.exit(main())
