from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .browser import click_text, eval_js, js_quote, set_input_value, visible_page_excerpt, visible_text_exists, wait_until


FIELD_TYPE_LABELS: dict[str, str] = {
    "text": "텍스트",
    "long_text": "긴 텍스트",
    "date": "날짜",
    "number": "숫자",
    "percentage": "백분율",
    "currency": "통화",
    "email": "이메일",
    "phone": "전화번호",
    "single_select": "단일 선택 목록",
    "multi_select": "다중 선택 목록",
    "checkbox": "체크박스",
    "url": "URL",
    "user": "사용자",
    "reference": "참조",
}

SUPPORTED_FIELD_TYPES = {
    "text",
    "long_text",
    "date",
    "number",
    "percentage",
    "currency",
    "email",
    "phone",
    "checkbox",
    "url",
    "user",
}


@dataclass(frozen=True)
class FieldSpec:
    name: str
    field_type: str
    description: str = ""
    help_text: str = ""


def load_field_specs(spec_path: Path) -> list[FieldSpec]:
    payload = json.loads(spec_path.read_text(encoding="utf-8"))
    raw_fields = payload.get("fields", payload)
    if not isinstance(raw_fields, list):
        raise ValueError("field spec must be a list or an object with a fields array")

    specs: list[FieldSpec] = []
    for item in raw_fields:
        if not isinstance(item, dict):
            raise ValueError(f"field spec item must be an object: {item!r}")
        field_type = str(item.get("field_type", "")).strip()
        specs.append(
            FieldSpec(
                name=str(item.get("name", "")).strip(),
                field_type=field_type,
                description=str(item.get("description", "")).strip(),
                help_text=str(item.get("help_text", "")).strip(),
            )
        )
    for spec in specs:
        if not spec.name:
            raise ValueError("field name is required")
        if spec.field_type not in FIELD_TYPE_LABELS:
            raise ValueError(f"unsupported field_type in spec: {spec.field_type}")
    return specs


def is_data_fields_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    return visible_text_exists(session, "데이터 필드") and visible_text_exists(session, "필드")


def open_data_fields_page(session: "vibium.browser_sync.VibeSync", url: str) -> None:
    session.go(url)
    ready = wait_until(lambda: is_data_fields_page_ready(session), timeout_sec=20.0, interval_sec=0.3)
    if not ready:
        raise RuntimeError(f"data fields page not ready: excerpt={visible_page_excerpt(session)}")


def open_field_creation_modal(session: "vibium.browser_sync.VibeSync") -> None:
    result = click_text(session, "필드", selectors="button", exact=True)
    if not result.get("ok"):
        raise RuntimeError(f"open field modal failed: {result}")
    ready = wait_until(lambda: visible_text_exists(session, "필드 생성"), timeout_sec=5.0, interval_sec=0.2)
    if not ready:
        raise RuntimeError(f"field modal did not open: excerpt={visible_page_excerpt(session)}")


def close_field_creation_modal(session: "vibium.browser_sync.VibeSync") -> None:
    eval_js(
        session,
        """
(() => {
  const closeButton = document.querySelector("button[aria-label='Close']");
  if (closeButton) closeButton.click();
  return true;
})()
""",
    )
    wait_until(lambda: not visible_text_exists(session, "필드 생성"), timeout_sec=5.0, interval_sec=0.2)


def is_field_listed(session: "vibium.browser_sync.VibeSync", field_name: str) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const wanted = {js_quote(field_name)};
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  return [...document.querySelectorAll("span, div, td, li, a")]
    .filter((el) => isVisible(el))
    .some((el) => normalize(el.innerText || el.textContent || "") === wanted);
}})()
""",
    )
    return bool(result)


def select_field_type(session: "vibium.browser_sync.VibeSync", field_type: str) -> None:
    label = FIELD_TYPE_LABELS[field_type]
    opened = eval_js(
        session,
        """
(() => {
  const selector = document.querySelector(".recatch__field-definition-type__dropdown-selector");
  if (!selector) {
    return { ok: false, reason: "selector_not_found" };
  }
  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {
    selector.dispatchEvent(new MouseEvent(name, { bubbles: true, cancelable: true, view: window }));
  });
  selector.click();
  return { ok: true };
})()
""",
    )
    if not isinstance(opened, dict) or not opened.get("ok"):
        raise RuntimeError(f"field type dropdown open failed: {opened}")

    dropdown_ready = wait_until(
        lambda: bool(
            eval_js(
                session,
                """
(() => !!document.querySelector(".recatch__field-definition-type__dropdown-dropdown"))()
""",
            )
        ),
        timeout_sec=3.0,
        interval_sec=0.1,
    )
    if not dropdown_ready:
        raise RuntimeError(f"field type dropdown did not appear: excerpt={visible_page_excerpt(session)}")

    holder_state = eval_js(
        session,
        """
(() => {
  const holder = document.querySelector(".recatch__field-definition-type__dropdown-dropdown .rc-virtual-list-holder");
  return {
    exists: !!holder,
    scrollHeight: holder ? holder.scrollHeight : 0,
    clientHeight: holder ? holder.clientHeight : 0,
  };
})()
""",
    )
    scroll_height = int(holder_state.get("scrollHeight", 0)) if isinstance(holder_state, dict) else 0
    client_height = int(holder_state.get("clientHeight", 0)) if isinstance(holder_state, dict) else 0
    total_scroll = max(scroll_height - client_height, 0)
    steps = max((total_scroll // 120) + 1, 1)
    last_error: str | None = None
    for index in range(steps + 1):
        clicked = eval_js(
            session,
            f"""
(() => {{
  const wanted = {js_quote(label)};
  const dropdown = document.querySelector(".recatch__field-definition-type__dropdown-dropdown");
  if (!dropdown) {{
    return {{ ok: false, reason: "dropdown_missing_during_click" }};
  }}
  const option = [...dropdown.querySelectorAll(".recatch__field-definition-type__dropdown-item-option")]
    .find((el) => ((el.getAttribute("title") || el.getAttribute("aria-label") || el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim()) === wanted);
  if (!option) {{
    return {{
      ok: false,
      reason: "option_not_in_current_view",
      visibleItems: [...dropdown.querySelectorAll(".recatch__field-definition-type__dropdown-item-option")]
        .map((el) => (el.getAttribute("title") || el.getAttribute("aria-label") || el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim())
        .filter(Boolean)
        .slice(0, 12),
    }};
  }}
  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {{
    option.dispatchEvent(new MouseEvent(name, {{ bubbles: true, cancelable: true, view: window }}));
  }});
  option.click();
  return {{ ok: true }};
}})()
""",
        )
        if isinstance(clicked, dict) and clicked.get("ok"):
            last_error = None
            break
        last_error = str(clicked)
        eval_js(
            session,
            f"""
(() => {{
  const holder = document.querySelector(".recatch__field-definition-type__dropdown-dropdown .rc-virtual-list-holder");
  if (!holder) return false;
  holder.scrollTop = {index + 1} * 120;
  holder.dispatchEvent(new Event("scroll", {{ bubbles: true }}));
  return true;
}})()
""",
        )
        time.sleep(0.1)

    if last_error is not None:
        visible_items = eval_js(
            session,
            """
(() => {
  const dropdown = document.querySelector(".recatch__field-definition-type__dropdown-dropdown");
  if (!dropdown) return [];
  return [...dropdown.querySelectorAll(".recatch__field-definition-type__dropdown-item-option")]
    .map((el) => (el.getAttribute("title") || el.getAttribute("aria-label") || el.innerText || el.textContent || "").replace(/\s+/g, " ").trim())
    .filter(Boolean)
    .slice(0, 12);
})()
""",
        )
        raise RuntimeError(
            "field type selection failed: "
            f"wanted={label}, visibleItems={visible_items}, error={last_error}"
        )

    selected = wait_until(
        lambda: bool(
            eval_js(
                session,
                f"""
(() => {{
  const selected = (document.querySelector(".recatch__field-definition-type__dropdown-selection-item")?.innerText || "")
    .replace(/\\s+/g, " ")
    .trim();
  const wanted = {js_quote(label)};
  return selected === wanted || selected.startsWith(wanted) || selected.includes(wanted);
}})()
""",
            )
        ),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not selected:
        selected_text = eval_js(
            session,
            """
(() => {
  return ((document.querySelector(".recatch__field-definition-type__dropdown-selection-item")?.innerText) || "")
    .replace(/\s+/g, " ")
    .trim();
})()
""",
        )
        raise RuntimeError(
            f"field type did not settle to {label}: selected={selected_text}, excerpt={visible_page_excerpt(session)}"
        )


def create_field(
    session: "vibium.browser_sync.VibeSync",
    spec: FieldSpec,
    log: Callable[[str], None],
) -> dict[str, Any]:
    if spec.field_type not in SUPPORTED_FIELD_TYPES:
        raise NotImplementedError(
            f"{spec.field_type} is not implemented yet. Use simple scalar-like field types for now."
        )

    if is_field_listed(session, spec.name):
        log(f"field already exists, skipping: {spec.name}")
        return {"ok": True, "name": spec.name, "field_type": spec.field_type, "skipped": True}

    open_field_creation_modal(session)
    result = set_input_value(session, spec.name, selector="input[placeholder='직무, 기업 규모, 산업군 등']")
    if not result.get("ok"):
        raise RuntimeError(f"field name input failed: {result}")

    if spec.field_type != "text":
        select_field_type(session, spec.field_type)

    if spec.description:
        set_input_value(session, spec.description, selector="input[placeholder='어떤 필드인지 구분하세요.']")
    if spec.help_text:
        set_input_value(session, spec.help_text, selector="textarea[placeholder='해당 필드에 값을 입력할 때 노출됩니다.']")

    create_button = click_text(session, "생성", selectors="button", exact=True)
    if not create_button.get("ok"):
        raise RuntimeError(f"click create failed: {create_button}")

    created = wait_until(lambda: is_field_listed(session, spec.name), timeout_sec=10.0, interval_sec=0.3)
    if not created:
        raise RuntimeError(f"field was not listed after create: {spec.name}")

    close_field_creation_modal(session)
    return {"ok": True, "name": spec.name, "field_type": spec.field_type}


def create_fields(
    session: "vibium.browser_sync.VibeSync",
    data_fields_url: str,
    specs: list[FieldSpec],
    log: Callable[[str], None],
) -> list[dict[str, Any]]:
    open_data_fields_page(session, data_fields_url)
    results: list[dict[str, Any]] = []
    for index, spec in enumerate(specs, start=1):
        log(f"[field {index}/{len(specs)}] start: {spec.name} ({spec.field_type})")
        result = create_field(session, spec, log=log)
        log(f"[field {index}/{len(specs)}] done: {result}")
        results.append(result)
    return results
