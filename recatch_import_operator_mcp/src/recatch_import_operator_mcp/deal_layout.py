from __future__ import annotations

from typing import Any

from .browser import eval_js, set_input_value, visible_page_excerpt, visible_text_exists, wait_until


def is_layout_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    return visible_text_exists(session, "레이아웃 수정하기") and visible_text_exists(session, "저장하기")


def open_layout_page(session: "vibium.browser_sync.VibeSync", url: str) -> None:
    session.go(url)
    ready = wait_until(lambda: is_layout_page_ready(session), timeout_sec=20.0, interval_sec=0.3)
    if not ready:
        raise RuntimeError(f"layout page not ready: excerpt={visible_page_excerpt(session)}")


def verify_field_in_layout(session: "vibium.browser_sync.VibeSync", field_name: str) -> dict[str, Any]:
    set_input_value(session, field_name, selector="input[placeholder='필드명 검색']")
    visible = wait_until(lambda: visible_text_exists(session, field_name), timeout_sec=5.0, interval_sec=0.2)
    if not visible:
        return {"ok": False, "name": field_name, "reason": "text_not_visible"}

    occurrences = eval_js(
        session,
        f"""
(() => {{
  const body = (document.body && document.body.innerText) || "";
  return body.split({field_name!r}).length - 1;
}})()
""",
    )
    return {
        "ok": bool(occurrences and int(occurrences) >= 2),
        "name": field_name,
        "occurrences": int(occurrences or 0),
    }


def verify_fields_in_layout(
    session: "vibium.browser_sync.VibeSync",
    layout_url: str,
    field_names: list[str],
) -> list[dict[str, Any]]:
    open_layout_page(session, layout_url)
    return [verify_field_in_layout(session, field_name) for field_name in field_names]
