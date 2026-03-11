from __future__ import annotations

import time
from typing import Any, Callable

from .auth import is_segments_page_ready
from .browser import (
    click_text,
    current_url,
    eval_js,
    extract_group_id,
    find_button_text,
    js_quote,
    read_expected_dynamic_count,
    read_recipient_count_from_page,
    set_input_value,
    visible_page_excerpt,
    visible_text_exists,
    wait_until,
)
from .plans import FilterRule, GroupKind, GroupSpec


OPERATOR_LABELS = {
    "equals": "같음",
    "not_equals": "같지 않음",
    "contains": "포함",
    "not_contains": "포함하지 않음",
    "starts_with": "시작함",
    "ends_with": "끝남",
    "is_empty": "비어있음",
    "is_not_empty": "비어있지 않음",
}
VALUE_REQUIRED_OPERATORS = {
    "equals",
    "not_equals",
    "contains",
    "not_contains",
    "starts_with",
    "ends_with",
}


def _require_ok(result: dict[str, Any], context: str) -> None:
    if not result.get("ok"):
        raise RuntimeError(f"{context} failed: {result}")


def _visible_selector_exists(
    session: "vibium.browser_sync.VibeSync",
    selector: str,
) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const el = document.querySelector({js_quote(selector)});
  if (!el) return false;
  const rect = el.getBoundingClientRect();
  const style = getComputedStyle(el);
  return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
}})()
""",
    )
    return bool(result)


def _detail_page_ready(
    session: "vibium.browser_sync.VibeSync",
    kind: GroupKind,
) -> bool:
    if not _visible_selector_exists(session, "button.recatch-ant-typography-edit"):
        return False
    action_text = "필터 수정" if kind is GroupKind.DYNAMIC else "수신자"
    return visible_text_exists(session, action_text)


def _operator_menu_item_visible(
    session: "vibium.browser_sync.VibeSync",
    label: str,
) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const textOf = (el) => ((el?.innerText || el?.textContent || "").replace(/\\s+/g, " ").trim());
  const isVisible = (el) => {{
    if (!el) return false;
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
  }};
  return [...document.querySelectorAll("ul.recatch-ant-menu li, ul.recatch-ant-menu span, [role='menuitem']")]
    .some((el) => isVisible(el) && textOf(el) === {js_quote(label)});
}})()
""",
    )
    return bool(result)


def _condition_value_input_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    if (!el) return false;
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
  };
  return [...document.querySelectorAll("div.recatch-ant-modal-wrap input, div.recatch-ant-modal-wrap textarea")]
    .some((el) => isVisible(el) && !((el.getAttribute("placeholder") || "").includes("\\uAC80\\uC0C9")));
})()
""",
    )
    return bool(result)


def open_segments_page(
    session: "vibium.browser_sync.VibeSync",
    segments_url: str,
) -> None:
    if current_url(session) != segments_url:
        session.go(segments_url)

    ready = wait_until(
        lambda: is_segments_page_ready(session),
        timeout_sec=20.0,
        interval_sec=0.3,
    )
    if not ready:
        raise RuntimeError(
            f"segments page not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )


def create_group(
    session: "vibium.browser_sync.VibeSync",
    segments_url: str,
    kind: GroupKind,
    log: Callable[[str], None],
) -> int:
    open_segments_page(session, segments_url)

    try:
        session.find("button.recatch-ant-dropdown-trigger", timeout=5000).click(timeout=5000)
    except Exception as exc:
        raise RuntimeError(f"open create-group menu failed: {exc}") from exc

    menu_suffix = "static" if kind is GroupKind.STATIC else "dynamic"
    item_label = "수동 그룹" if kind is GroupKind.STATIC else "자동 그룹"
    menu_click = eval_js(
        session,
        f"""
(() => {{
  const item = document.querySelector("li[data-menu-id$='-{menu_suffix}']");
  if (!item) {{
    return {{ ok: false, reason: "item_not_found" }};
  }}
  item.click();
  return {{
    ok: true,
    text: ((item.innerText || item.textContent || "").replace(/\\s+/g, " ").trim())
  }};
}})()
""",
    )
    if not isinstance(menu_click, dict) or not menu_click.get("ok"):
        raise RuntimeError(f"select {item_label} failed: {menu_click}")

    navigated = wait_until(
        lambda: "/segments/" in current_url(session) and current_url(session) != segments_url,
        timeout_sec=15.0,
        interval_sec=0.25,
    )
    if not navigated:
        raise RuntimeError(f"group detail did not open: url={current_url(session)}")

    group_id = extract_group_id(current_url(session))
    if group_id is None:
        raise RuntimeError(f"cannot parse group id from url: {current_url(session)}")

    ready = wait_until(
        lambda: _detail_page_ready(session, kind),
        timeout_sec=10.0,
        interval_sec=0.25,
    )
    if not ready:
        raise RuntimeError(
            f"group detail action area not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )

    log(f"created {kind.value} group: id={group_id}")
    return group_id


def rename_current_group(
    session: "vibium.browser_sync.VibeSync",
    name: str,
) -> None:
    try:
        session.find("button.recatch-ant-typography-edit", timeout=5000).click(timeout=5000)
    except Exception as exc:
        raise RuntimeError(f"open rename editor failed: {exc}") from exc

    result = set_input_value(
        session,
        name,
        selectors="textarea",
        container_text=None,
        placeholder_excludes=(),
    )
    _require_ok(result, "set group name")

    blur_result = eval_js(
        session,
        """
(() => {
  const active = document.activeElement;
  if (active && typeof active.blur === "function") {
    active.blur();
  }
  return { ok: true };
})()
""",
    )
    if not isinstance(blur_result, dict) or not blur_result.get("ok"):
        raise RuntimeError(f"blur rename editor failed: {blur_result}")

    saved = wait_until(
        lambda: (
            visible_text_exists(session, name)
            and not bool(
                eval_js(
                    session,
                    """
(() => {
  const textarea = document.querySelector("textarea");
  if (!textarea) return false;
  const rect = textarea.getBoundingClientRect();
  const style = getComputedStyle(textarea);
  return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
})()
""",
                )
            )
        ),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not saved:
        raise RuntimeError(f"group name did not update: {name}")


def clear_all_filters_if_present(session: "vibium.browser_sync.VibeSync") -> None:
    if not visible_text_exists(session, "모든 필터 삭제"):
        return
    button_text = find_button_text(session, "모든 필터 삭제")
    if button_text is None:
        return
    result = click_text(session, button_text, exact=True)
    if not result.get("ok"):
        return
    time.sleep(0.3)


def _open_condition_wizard(
    session: "vibium.browser_sync.VibeSync",
    *,
    is_first: bool,
) -> None:
    label = "조건" if is_first else "또는"
    _require_ok(
        click_text(session, label, selectors="button", exact=True),
        f"open {label} wizard",
    )

    ready = wait_until(
        lambda: visible_text_exists(session, "조건 추가"),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not ready:
        raise RuntimeError(f"condition wizard did not open after {label}")
    time.sleep(0.8)


def _configure_title_rule(
    session: "vibium.browser_sync.VibeSync",
    rule: FilterRule,
) -> None:
    title_field_selector = (
        "div.recatch-ant-collapse-content-active "
        "div.recatch-ant-collapse-content-box > div.sc-9ed461ce-6 > div.sc-1e547695-0:nth-child(2)"
    )

    try:
        session.find(
            "div.recatch-ant-collapse-item:first-child div.recatch-ant-collapse-header",
            timeout=5000,
        ).click(timeout=5000)
    except Exception as exc:
        raise RuntimeError(f"select lead/deal category failed: {exc}") from exc

    field_list_ready = wait_until(
        lambda: bool(
            eval_js(
                session,
                f"""
(() => {{
  const el = document.querySelector({js_quote(title_field_selector)});
  if (!el) return false;
  const rect = el.getBoundingClientRect();
  const style = getComputedStyle(el);
  return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
}})()
""",
            )
        ),
        timeout_sec=8.0,
        interval_sec=0.2,
    )
    if not field_list_ready:
        raise RuntimeError("title field list did not appear")
    time.sleep(0.8)

    try:
        session.find(title_field_selector, timeout=5000).click(timeout=5000)
    except Exception as exc:
        raise RuntimeError(f"select title field failed: {exc}") from exc

    operator_label = OPERATOR_LABELS[rule.operator]
    operator_ready = wait_until(
        lambda: _operator_menu_item_visible(session, operator_label),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not operator_ready:
        raise RuntimeError(f"operator menu did not appear for {operator_label}")

    _require_ok(
        click_text(
            session,
            operator_label,
            selectors="ul.recatch-ant-menu li, ul.recatch-ant-menu span, [role='menuitem']",
            exact=True,
        ),
        f"select operator {operator_label}",
    )

    if rule.operator in VALUE_REQUIRED_OPERATORS:
        input_ready = wait_until(
            lambda: _condition_value_input_ready(session),
            timeout_sec=5.0,
            interval_sec=0.2,
        )
        if not input_ready:
            raise RuntimeError(f"value input did not appear for {rule.operator}")
        _require_ok(
            set_input_value(
                session,
                rule.value or "",
                selectors="input, textarea",
                container_text="조건 추가",
            ),
            "fill condition value",
        )

    try:
        session.find(
            "div.recatch-ant-modal-footer button.recatch-ant-btn-primary",
            timeout=5000,
        ).click(timeout=5000)
    except Exception as exc:
        raise RuntimeError(f"confirm condition failed: {exc}") from exc

    closed = wait_until(
        lambda: not visible_text_exists(session, "조건 추가"),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not closed:
        raise RuntimeError(f"condition wizard did not close: rule={rule}")


def apply_filter_rules(
    session: "vibium.browser_sync.VibeSync",
    rules: tuple[FilterRule, ...],
) -> None:
    clear_all_filters_if_present(session)
    for index, rule in enumerate(rules):
        _open_condition_wizard(session, is_first=index == 0)
        _configure_title_rule(session, rule)


def open_dynamic_filter_editor(session: "vibium.browser_sync.VibeSync") -> None:
    _require_ok(
        click_text(session, "필터 수정", selectors="button", exact=True),
        "open dynamic filter editor",
    )
    ready = wait_until(
        lambda: visible_text_exists(session, "모든 필터 삭제"),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not ready:
        raise RuntimeError("dynamic filter editor did not open")


def apply_dynamic_group_filters(
    session: "vibium.browser_sync.VibeSync",
    spec: GroupSpec,
    verification_delay_sec: float,
) -> dict[str, Any]:
    open_dynamic_filter_editor(session)
    apply_filter_rules(session, spec.filter_rules)
    expected_dynamic_count = read_expected_dynamic_count(session)

    _require_ok(
        click_text(session, "완료", selectors="button", exact=True),
        "save dynamic filters",
    )

    closed = wait_until(
        lambda: not visible_text_exists(session, "완료") or visible_text_exists(session, "필터 수정"),
        timeout_sec=8.0,
        interval_sec=0.2,
    )
    if not closed:
        raise RuntimeError("dynamic filter editor did not close")

    if verification_delay_sec > 0:
        time.sleep(verification_delay_sec)

    return {
        "expected_dynamic_count": expected_dynamic_count,
        "detail_recipient_count": read_recipient_count_from_page(session),
    }


def open_static_recipient_picker(session: "vibium.browser_sync.VibeSync") -> None:
    _require_ok(
        click_text(session, "수신자", selectors="button", exact=True, top_max=260),
        "open static recipient picker",
    )
    ready = wait_until(
        lambda: visible_text_exists(session, "선택 추가") and visible_text_exists(session, "전체 추가"),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not ready:
        raise RuntimeError("static recipient picker did not open")


def open_static_filter_panel(session: "vibium.browser_sync.VibeSync") -> None:
    _require_ok(
        click_text(session, "필터", selectors="button", exact=True),
        "open static filter panel",
    )
    ready = wait_until(
        lambda: visible_text_exists(session, "모든 필터 삭제") and visible_text_exists(session, "닫기"),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not ready:
        raise RuntimeError("static filter panel did not open")


def _click_add_filtered_results(session: "vibium.browser_sync.VibeSync") -> str:
    button_text = find_button_text(session, "필터된 결과 전체 추가")
    if button_text is None:
        button_text = find_button_text(session, "전체 추가 (")
    if button_text is None:
        raise RuntimeError(f"add-all button not found: excerpt={visible_page_excerpt(session)}")

    _require_ok(
        click_text(session, button_text, selectors="button", exact=True),
        f"click {button_text}",
    )
    return button_text


def apply_static_group_filters(
    session: "vibium.browser_sync.VibeSync",
    spec: GroupSpec,
    verification_delay_sec: float,
) -> dict[str, Any]:
    open_static_recipient_picker(session)
    open_static_filter_panel(session)
    apply_filter_rules(session, spec.filter_rules)

    button_text = _click_add_filtered_results(session)

    if visible_text_exists(session, "닫기"):
        click_text(session, "닫기", selectors="button", exact=True, prefer_last=True)
    if visible_text_exists(session, "Close"):
        click_text(session, "Close", selectors="button", exact=True)

    if verification_delay_sec > 0:
        time.sleep(verification_delay_sec)

    return {
        "recipient_picker_button": button_text,
        "detail_recipient_count": read_recipient_count_from_page(session),
    }


def create_group_from_spec(
    session: "vibium.browser_sync.VibeSync",
    segments_url: str,
    spec: GroupSpec,
    verification_delay_sec: float,
    log: Callable[[str], None],
) -> dict[str, Any]:
    group_id = create_group(session, segments_url, spec.kind, log=log)
    rename_current_group(session, spec.name)
    settled = wait_until(
        lambda: _detail_page_ready(session, spec.kind) and visible_text_exists(session, spec.name),
        timeout_sec=5.0,
        interval_sec=0.2,
    )
    if not settled:
        raise RuntimeError(
            f"group detail did not settle after rename: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )
    time.sleep(1.5)

    if spec.kind is GroupKind.STATIC:
        details = apply_static_group_filters(
            session,
            spec,
            verification_delay_sec=verification_delay_sec,
        )
    else:
        details = apply_dynamic_group_filters(
            session,
            spec,
            verification_delay_sec=verification_delay_sec,
        )

    result = {
        "group_id": group_id,
        "name": spec.name,
        "kind": spec.kind.value,
        "expected_count": spec.expected_count,
        "url": current_url(session),
    }
    result.update(details)
    return result


def create_groups_from_specs(
    session: "vibium.browser_sync.VibeSync",
    segments_url: str,
    specs: list[GroupSpec],
    verification_delay_sec: float,
    log: Callable[[str], None],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for index, spec in enumerate(specs, start=1):
        log(f"[group {index}/{len(specs)}] start: {spec.kind.value} {spec.name}")
        result = create_group_from_spec(
            session=session,
            segments_url=segments_url,
            spec=spec,
            verification_delay_sec=verification_delay_sec,
            log=log,
        )
        log(f"[group {index}/{len(specs)}] done: {result}")
        results.append(result)
    return results
