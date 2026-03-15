from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from typing import Any, Callable, Sequence

from .browser import current_url, eval_js, visible_page_excerpt, visible_text_exists, wait_until


NEXT_LABEL = "다음"
UPLOAD_LABEL = "업로드"
CONFIRM_LABEL = "확인"
RESET_LABEL = "초기화"
VALIDATION_OK_TEXT = "데이터에 에러가 없습니다"
UPLOAD_OK_TEXT = "업로드에 성공했습니다."
MAPPING_HINT_TEXT = "모든 필드를 연결하지 않아도"
FIELD_SELECT_PLACEHOLDER = "필드 선택"


def read_csv_headers(csv_path: Path) -> list[str]:
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"csv file is empty: {csv_path}") from exc

    normalized = [value.strip() for value in header]
    if not any(normalized):
        raise ValueError(f"csv header is empty: {csv_path}")

    seen: set[str] = set()
    duplicates: list[str] = []
    for item in normalized:
        if not item:
            continue
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    if duplicates:
        raise ValueError(f"csv header contains duplicates: {csv_path} -> {duplicates}")
    return normalized


def count_csv_rows(csv_text: str) -> int:
    lines = [line for line in csv_text.splitlines() if line.strip()]
    return max(len(lines) - 1, 0)


def has_visible_textarea(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
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
    return bool(result)


def is_import_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    return visible_text_exists(session, "딜 업로드") and (
        has_visible_textarea(session)
        or visible_text_exists(session, NEXT_LABEL)
        or visible_text_exists(session, RESET_LABEL)
    )


def ensure_import_page_ready(session: "vibium.browser_sync.VibeSync", import_url: str) -> None:
    session.go(import_url)
    ready = wait_until(
        lambda: is_import_page_ready(session),
        timeout_sec=20.0,
        interval_sec=0.25,
    )
    if not ready:
        raise RuntimeError(
            f"import page not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )


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


def click_primary_button_if_matches(
    session: "vibium.browser_sync.VibeSync",
    label: str,
) -> dict[str, Any]:
    primary_text = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const button = [...document.querySelectorAll("button.recatch-ant-btn-primary")]
    .find((el) => isVisible(el));
  return button ? (button.innerText || button.textContent || "").replace(/\s+/g, " ").trim() : "";
})()
""",
    )
    if not isinstance(primary_text, str):
        return {"ok": False, "reason": "primary_button_text_unreadable"}
    if label not in primary_text:
        return {"ok": False, "reason": "primary_button_label_mismatch", "text": primary_text}

    try:
        session.find("button.recatch-ant-btn-primary", timeout=1500).click(timeout=3000)
    except Exception as exc:
        return {"ok": False, "reason": "primary_button_click_failed", "error": str(exc), "text": primary_text}
    return {"ok": True, "text": primary_text, "via": "primary_button"}


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
    if label in {NEXT_LABEL, UPLOAD_LABEL, CONFIRM_LABEL}:
        primary_result = click_primary_button_if_matches(session, label)
        if primary_result.get("ok"):
            return primary_result
    result = click_button_by_text(session, label)
    if not result.get("ok"):
        raise RuntimeError(f"button click failed: label={label}, result={result}")
    return result


def reset_import_page_if_needed(session: "vibium.browser_sync.VibeSync") -> bool:
    if has_visible_textarea(session):
        return False

    state = button_state(session, RESET_LABEL)
    if not state.get("enabled"):
        return False

    click_enabled_button(session, RESET_LABEL, timeout_sec=10.0)
    reset_ok = wait_until(
        lambda: has_visible_textarea(session),
        timeout_sec=10.0,
        interval_sec=0.25,
    )
    if not reset_ok:
        raise RuntimeError(f"import page reset did not return to textarea: excerpt={visible_page_excerpt(session)}")
    return True


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
    ready: selectCount >= 2 || body.includes({json.dumps(MAPPING_HINT_TEXT, ensure_ascii=False)}),
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

  const clickable = select.querySelector(".recatch-ant-select-selector") || select;
  try {{
    clickable.scrollIntoView({{ block: "center", inline: "nearest" }});
  }} catch (error) {{
    // Keep going.
  }}

  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    clickable.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true, view: window }}));
  }});
  clickable.click();

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


def click_dropdown_option(session: "vibium.browser_sync.VibeSync", option_text: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const wanted = ((value) => (value || "").replace(/\\s+/g, " ").trim())({json.dumps(option_text, ensure_ascii=False)});
  const leafWanted = wanted.split(">").slice(-1)[0].trim();
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const dropdowns = [...document.querySelectorAll(".recatch-ant-select-dropdown")]
    .filter((el) => isVisible(el));
  if (!dropdowns.length) {{
    return {{ ok: false, reason: "dropdown_not_found", wanted }};
  }}

  const dropdown = dropdowns[dropdowns.length - 1];
  const options = [...dropdown.querySelectorAll(".sc-59d41ecc-0, .recatch-ant-select-item-option, [role='option']")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const text = normalize(el.innerText || el.textContent || "");
      return {{ el, text }};
    }})
    .filter((item) => item.text);

  const exactCandidates = options.filter((item) =>
    item.text === wanted
    || item.text === `${{wanted}}*`
    || item.text === leafWanted
    || item.text === `${{leafWanted}}*`
  );
  const partialCandidates = options.filter((item) => {{
    if (exactCandidates.some((exact) => exact.el === item.el)) {{
      return false;
    }}
    if (wanted.length < 3 && leafWanted.length < 3) {{
      return false;
    }}
    return item.text.includes(wanted) || (leafWanted && item.text.includes(leafWanted));
  }});

  const target = exactCandidates[0] || partialCandidates[0];
  if (!target) {{
    return {{
      ok: false,
      reason: "dropdown_option_not_found",
      wanted,
      topCandidates: options.slice(0, 12).map((item) => item.text),
    }};
  }}

  try {{
    target.el.scrollIntoView({{ block: "nearest", inline: "nearest" }});
  }} catch (error) {{
    // Keep going.
  }}
  if (typeof target.el.click === "function") {{
    target.el.click();
  }}

  return {{
    ok: true,
    wanted,
    matchedText: target.text,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


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
  const wanted = ((value) => (value || "").replace(/\\s+/g, " ").trim())({json.dumps(option_text, ensure_ascii=False)});
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


def selection_matches_header(select_text: str, header_name: str) -> bool:
    current = " ".join(select_text.split())
    header = " ".join(header_name.split())
    if not current or not header:
        return False
    return current == header or current.endswith(header) or header in current


def map_header_select(
    session: "vibium.browser_sync.VibeSync",
    select_index: int,
    header_name: str,
) -> dict[str, Any]:
    prepared = prepare_select_query(session, select_index, header_name)
    if not prepared.get("ok"):
        return {
            "ok": False,
            "stage": "prepare",
            "select_index": select_index,
            "header": header_name,
            "detail": prepared,
        }

    time.sleep(0.3)
    clicked = click_dropdown_option(session, header_name)
    if not clicked.get("ok"):
        return {
            "ok": False,
            "stage": "click",
            "select_index": select_index,
            "header": header_name,
            "prepared": prepared,
            "detail": clicked,
        }

    selected = wait_until(
        lambda: bool(selected_option_state(session, select_index, header_name).get("selected")),
        timeout_sec=4.0,
        interval_sec=0.15,
    )
    state = selected_option_state(session, select_index, header_name)
    return {
        "ok": selected,
        "select_index": select_index,
        "header": header_name,
        "prepared": prepared,
        "clicked": clicked,
        "state": state,
    }


def auto_map_headers(
    session: "vibium.browser_sync.VibeSync",
    headers: Sequence[str],
    log: Callable[[str], None],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    latest_selects = read_mapping_select_texts(session)
    if len(latest_selects) < len(headers):
        log(
            "mapping select count is smaller than csv header count: "
            f"{len(latest_selects)} < {len(headers)}"
        )

    for select_index, header_name in enumerate(headers):
        latest_selects = read_mapping_select_texts(session)
        if select_index >= len(latest_selects):
            results.append(
                {
                    "ok": False,
                    "select_index": select_index,
                    "header": header_name,
                    "reason": "select_index_out_of_range",
                    "available_count": len(latest_selects),
                }
            )
            continue

        current_text = latest_selects[select_index]
        if selection_matches_header(current_text, header_name):
            results.append(
                {
                    "ok": True,
                    "select_index": select_index,
                    "header": header_name,
                    "skipped": True,
                    "reason": "already_selected",
                    "current_text": current_text,
                }
            )
            continue

        if current_text and current_text != FIELD_SELECT_PLACEHOLDER:
            log(
                f"remap header[{select_index}] from current selection "
                f"{current_text!r} to {header_name!r}"
            )

        log(f"mapping header[{select_index}]: {header_name}")
        result = map_header_select(session, select_index, header_name)
        results.append(result)
        if not result.get("ok"):
            log(f"mapping failed for header[{select_index}] {header_name}: {result}")
        time.sleep(0.2)

    return results


def read_success_summary(session: "vibium.browser_sync.VibeSync") -> dict[str, Any]:
    result = eval_js(
        session,
        """
(() => {
  return ((document.body && document.body.innerText) || "")
    .split("\\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, 12);
})()
""",
    )
    return {"excerpt": result if isinstance(result, list) else []}


def advance_to_preview(session: "vibium.browser_sync.VibeSync") -> bool:
    for _ in range(3):
        click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)
        ready = wait_until(
            lambda: bool(button_state(session, UPLOAD_LABEL).get("enabled"))
            or visible_text_exists(session, "동일한 값을 가진 회사, 연락처는 1개로 병합되고"),
            timeout_sec=8.0,
            interval_sec=0.2,
        )
        if ready:
            return True
        time.sleep(0.4)
    return False


def import_csv_file(
    session: "vibium.browser_sync.VibeSync",
    import_url: str,
    csv_path: Path,
    log: Callable[[str], None],
    *,
    preview_only: bool = False,
    upload_timeout_sec: float = 60.0,
) -> dict[str, Any]:
    csv_text = csv_path.read_text(encoding="utf-8")
    headers = read_csv_headers(csv_path)
    row_count = count_csv_rows(csv_text)

    ensure_import_page_ready(session, import_url)
    reset_applied = reset_import_page_if_needed(session)
    paste_result = set_textarea_value(session, csv_text)
    if not paste_result.get("ok"):
        raise RuntimeError(f"csv paste failed for {csv_path.name}: {paste_result}")

    next_enabled = wait_until(
        lambda: bool(button_state(session, NEXT_LABEL).get("enabled")),
        timeout_sec=12.0,
        interval_sec=0.2,
    )
    if not next_enabled:
        raise RuntimeError(f"next button not enabled after paste: excerpt={visible_page_excerpt(session)}")

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)

    mapping_ready = wait_until(
        lambda: bool(mapping_page_state(session).get("ready")),
        timeout_sec=20.0,
        interval_sec=0.2,
    )
    if not mapping_ready:
        raise RuntimeError(f"mapping page not ready for {csv_path.name}: excerpt={visible_page_excerpt(session)}")

    expected_select_count = len(headers)
    mapping_selects_ready = wait_until(
        lambda: len(read_mapping_select_texts(session)) >= expected_select_count,
        timeout_sec=12.0,
        interval_sec=0.2,
    )
    if not mapping_selects_ready:
        log(
            "mapping select count is smaller than csv header count: "
            f"{len(read_mapping_select_texts(session))} < {expected_select_count}"
        )

    mapping_results = auto_map_headers(session, headers, log=log)

    click_enabled_button(session, NEXT_LABEL, timeout_sec=20.0)
    validation_ok = wait_until(
        lambda: visible_text_exists(session, VALIDATION_OK_TEXT),
        timeout_sec=30.0,
        interval_sec=0.2,
    )
    if not validation_ok:
        raise RuntimeError(f"validation step failed for {csv_path.name}: excerpt={visible_page_excerpt(session)}")

    if preview_only:
        return {
            "ok": True,
            "previewOnly": True,
            "file": csv_path.name,
            "rowCount": row_count,
            "headers": headers,
            "resetApplied": reset_applied,
            "pasteResult": paste_result,
            "mappingResults": mapping_results,
            "excerpt": visible_page_excerpt(session),
        }

    preview_ready = advance_to_preview(session)
    if not preview_ready:
        raise RuntimeError(f"preview step not ready for {csv_path.name}: excerpt={visible_page_excerpt(session)}")

    click_enabled_button(session, UPLOAD_LABEL, timeout_sec=30.0)
    upload_ok = wait_until(
        lambda: visible_text_exists(session, UPLOAD_OK_TEXT),
        timeout_sec=upload_timeout_sec,
        interval_sec=0.5,
    )
    if not upload_ok:
        raise RuntimeError(f"upload success text not found for {csv_path.name}: excerpt={visible_page_excerpt(session)}")

    success_summary = read_success_summary(session)
    click_enabled_button(session, CONFIRM_LABEL, timeout_sec=20.0)

    return {
        "ok": True,
        "file": csv_path.name,
        "rowCount": row_count,
        "headers": headers,
        "resetApplied": reset_applied,
        "pasteResult": paste_result,
        "mappingResults": mapping_results,
        "successSummary": success_summary,
        "finalUrl": current_url(session),
    }
