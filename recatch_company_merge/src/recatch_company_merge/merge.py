from __future__ import annotations

from typing import Any

from .browser import (
    DOM_HELPERS_JS,
    current_url,
    eval_js,
    js_quote,
    visible_page_excerpt,
    visible_text_exists,
    wait_until,
)


COMPANIES_TITLE = "모든 회사"
SEARCH_PLACEHOLDER = "검색"
MERGE_MODAL_TITLE = "회사 병합"
NEXT_LABEL = "다음"
PREV_LABEL = "이전"
MERGE_LABEL = "병합"


def is_company_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const hasSearch = [...document.querySelectorAll("input")]
    .some((el) => isVisible(el) && (el.placeholder || "").includes({js_quote(SEARCH_PLACEHOLDER)}));
  const hasTitle = [...document.querySelectorAll("body, div, span, h1, h2")]
    .some((el) => isVisible(el) && textOf(el) === {js_quote(COMPANIES_TITLE)});
  return hasSearch && hasTitle;
}})()
""",
    )
    return bool(result)


def _page_state(session: "vibium.browser_sync.VibeSync") -> dict[str, Any]:
    result = eval_js(
        session,
        r"""
(() => {
  const textOf = (el) => ((el?.innerText || el?.textContent || "").replace(/\s+/g, " ").trim());
  const isVisible = (el) => {
    if (!el) return false;
    const rect = el.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return false;
    const style = getComputedStyle(el);
    return style.display !== "none" && style.visibility !== "hidden";
  };

  const searchInput = [...document.querySelectorAll("input")]
    .find((el) => isVisible(el) && (el.placeholder || "").includes("검색"));
  const countMatch = ((document.body?.innerText || "").match(/(\d+)\s*중\s*(\d+)/) || []);
  const rows = [...document.querySelectorAll("div.table-view-row")]
    .filter((row) => isVisible(row))
    .map((row) => {
      const checkbox = row.querySelector("input.recatch-ant-checkbox-input[type='checkbox']");
      return {
        text: textOf(row),
        checked: !!checkbox?.checked,
      };
    });
  return {
    searchValue: searchInput?.value || "",
    countVisible: countMatch[1] ? Number(countMatch[1]) : null,
    countTotal: countMatch[2] ? Number(countMatch[2]) : null,
    rows,
    selectedCount: rows.filter((row) => row.checked).length,
    modalTitleVisible: [...document.querySelectorAll("body, div, span, h1, h2")]
      .some((el) => isVisible(el) && textOf(el) === "회사 병합"),
  };
})()
""",
    )
    return result if isinstance(result, dict) else {"raw": result}


def fill_search_input(
    session: "vibium.browser_sync.VibeSync",
    company_name: str,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const input = [...document.querySelectorAll("input")]
    .find((el) => isVisible(el) && (el.placeholder || "").includes({js_quote(SEARCH_PLACEHOLDER)}));
  if (!input) {{
    return {{ ok: false, reason: "search_input_not_found" }};
  }}
  setInputValue(input, {js_quote(company_name)});
  return {{ ok: true, value: input.value || "" }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def wait_for_search_results(
    session: "vibium.browser_sync.VibeSync",
    company_name: str,
    min_rows: int,
    timeout_sec: float = 15.0,
) -> dict[str, Any]:
    def ready() -> bool:
        state = _page_state(session)
        rows = state.get("rows") or []
        return (
            state.get("searchValue") == company_name
            and len(rows) >= min_rows
            and all(company_name in (row.get("text") or "") for row in rows[:min_rows])
        )

    found = wait_until(ready, timeout_sec=timeout_sec, interval_sec=0.25)
    state = _page_state(session)
    if not found:
        raise RuntimeError(
            f"search results not ready: company_name={company_name}, state={state}, "
            f"url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )
    return state


def select_company_rows(
    session: "vibium.browser_sync.VibeSync",
    company_name: str,
    select_count: int,
) -> dict[str, Any]:
    if select_count > 20:
        raise ValueError("select_count cannot exceed 20 for one merge")

    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const rows = [...document.querySelectorAll("div.table-view-row")]
    .filter((row) => isVisible(row) && textOf(row).includes({js_quote(company_name)}));
  if (rows.length < {select_count}) {{
    return {{
      ok: false,
      reason: "not_enough_matching_rows",
      wanted: {select_count},
      found: rows.length,
      rows: rows.map((row) => textOf(row)),
    }};
  }}

  const clicked = [];
  for (const row of rows.slice(0, {select_count})) {{
    const checkbox = row.querySelector("input.recatch-ant-checkbox-input[type='checkbox']");
    const clickTarget =
      checkbox?.closest("label.recatch-ant-checkbox-wrapper")
      || checkbox?.parentElement
      || checkbox;
    if (!checkbox || !clickTarget) {{
      return {{
        ok: false,
        reason: "checkbox_not_found",
        rowText: textOf(row),
      }};
    }}
    if (!checkbox.checked) {{
      clickElement(clickTarget);
    }}
    clicked.push({{
      rowText: textOf(row),
      checked: !!checkbox.checked,
    }});
  }}

  return {{
    ok: rows.slice(0, {select_count}).every((row) => !!row.querySelector("input.recatch-ant-checkbox-input[type='checkbox']")?.checked),
    clicked,
  }};
}})()
""",
    )
    payload = result if isinstance(result, dict) else {"ok": False, "raw": result}
    if not payload.get("ok"):
        raise RuntimeError(f"row selection failed: {payload}")

    selected = wait_until(
        lambda: (_page_state(session).get("selectedCount") or 0) >= select_count,
        timeout_sec=8.0,
        interval_sec=0.2,
    )
    state = _page_state(session)
    if not selected:
        raise RuntimeError(f"selected row count did not reach {select_count}: {state}")
    return state


def _click_button(
    session: "vibium.browser_sync.VibeSync",
    label: str,
    *,
    modal_only: bool,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const wanted = {js_quote(label)};
  const dialog = [...document.querySelectorAll("[role='dialog'], .recatch-ant-modal, .recatch-ant-modal-root")]
    .find((el) => isVisible(el) && textOf(el).includes({js_quote(MERGE_MODAL_TITLE)}));
  const scope = {str(modal_only).lower()} ? (dialog || null) : document;
  if ({str(modal_only).lower()} && !scope) {{
    return {{ ok: false, reason: "modal_not_found", wanted }};
  }}

  const isDisabled = (el) =>
    !!el.disabled
    || el.getAttribute("aria-disabled") === "true"
    || [...el.classList].some((name) => name.includes("disabled"));

  const buttons = [...scope.querySelectorAll("button, [role='button'], a")]
    .filter((el) => isVisible(el) && !isDisabled(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      return {{
        el,
        text: textOf(el),
        top: rect.top,
        left: rect.left,
      }};
    }})
    .filter((item) => item.text === wanted || item.text.includes(wanted))
    .sort((a, b) => a.top - b.top || a.left - b.left);

  const target = buttons[0];
  if (!target) {{
    return {{ ok: false, reason: "button_not_found", wanted }};
  }}
  clickElement(target.el);
  return {{
    ok: true,
    text: target.text,
    top: target.top,
    left: target.left,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def _click_modal_radio(
    session: "vibium.browser_sync.VibeSync",
    survivor_index: int,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const dialog = [...document.querySelectorAll("[role='dialog'], .recatch-ant-modal, .recatch-ant-modal-root")]
    .find((el) => isVisible(el) && textOf(el).includes({js_quote(MERGE_MODAL_TITLE)}));
  if (!dialog) {{
    return {{ ok: false, reason: "modal_not_found" }};
  }}

  const labels = [...dialog.querySelectorAll("label.recatch-ant-radio-wrapper")]
    .filter((el) => isVisible(el));
  if (!labels.length) {{
    return {{ ok: {str(survivor_index == 1).lower()}, reason: "radio_controls_not_found" }};
  }}

  const target = labels[{survivor_index - 1}] || null;
  if (!target) {{
    return {{
      ok: false,
      reason: "radio_index_out_of_range",
      wanted: {survivor_index},
      found: labels.length,
    }};
  }}
  clickElement(target);
  return {{
    ok: true,
    selectedIndex: {survivor_index},
    labelText: textOf(target),
  }};
}})()
""",
    )
    payload = result if isinstance(result, dict) else {"ok": False, "raw": result}
    if not payload.get("ok"):
        raise RuntimeError(f"merge survivor selection failed: {payload}")
    return payload


def open_merge_modal(
    session: "vibium.browser_sync.VibeSync",
    survivor_index: int,
) -> dict[str, Any]:
    action = _click_button(session, MERGE_LABEL, modal_only=False)
    if not action.get("ok"):
        raise RuntimeError(f"merge action button click failed: {action}")

    ready = wait_until(
        lambda: _page_state(session).get("modalTitleVisible") is True and visible_text_exists(session, NEXT_LABEL),
        timeout_sec=10.0,
        interval_sec=0.2,
    )
    if not ready:
        raise RuntimeError(
            f"merge modal step 1 not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )

    survivor = _click_modal_radio(session, survivor_index)
    next_click = _click_button(session, NEXT_LABEL, modal_only=True)
    if not next_click.get("ok"):
        raise RuntimeError(f"merge modal next click failed: {next_click}")

    step2_ready = wait_until(
        lambda: visible_text_exists(session, PREV_LABEL) and visible_text_exists(session, MERGE_LABEL),
        timeout_sec=10.0,
        interval_sec=0.2,
    )
    if not step2_ready:
        raise RuntimeError(
            f"merge modal step 2 not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )

    return {
        "actionClick": action,
        "survivorSelection": survivor,
        "nextClick": next_click,
    }


def complete_merge(
    session: "vibium.browser_sync.VibeSync",
    *,
    before_count: int,
    select_count: int,
) -> dict[str, Any]:
    final_click = _click_button(session, MERGE_LABEL, modal_only=True)
    if not final_click.get("ok"):
        raise RuntimeError(f"final merge click failed: {final_click}")

    expected_after = before_count - (select_count - 1)

    def completed() -> bool:
        state = _page_state(session)
        return state.get("countVisible") == expected_after

    merged = wait_until(completed, timeout_sec=20.0, interval_sec=0.25)
    state = _page_state(session)
    if not merged:
        raise RuntimeError(
            f"merge completion not detected: expected_after={expected_after}, state={state}, "
            f"url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )

    return {
        "finalClick": final_click,
        "expectedVisibleCountAfterMerge": expected_after,
        "state": state,
        "finalUrl": current_url(session),
    }


def merge_company_name(
    session: "vibium.browser_sync.VibeSync",
    *,
    company_name: str,
    select_count: int,
    survivor_index: int,
    preview_only: bool,
    log,
) -> dict[str, Any]:
    if select_count < 2:
        raise ValueError("select_count must be at least 2")
    if select_count > 20:
        raise ValueError("select_count cannot exceed 20 for one merge")
    if survivor_index < 1:
        raise ValueError("survivor_index must be at least 1")

    search_result = fill_search_input(session, company_name)
    if not search_result.get("ok"):
        raise RuntimeError(f"search input fill failed: {search_result}")
    log(f"search input filled: {search_result}")

    search_state = wait_for_search_results(session, company_name, min_rows=select_count)
    before_count = search_state.get("countVisible")
    if not isinstance(before_count, int):
        raise RuntimeError(f"visible search result count unreadable: {search_state}")
    log(f"search state: visible_count={before_count}, selected_count={search_state.get('selectedCount')}")

    selection_state = select_company_rows(session, company_name, select_count)
    log(f"row selection state: {selection_state}")

    modal_state = open_merge_modal(session, survivor_index)
    log(f"merge modal state: {modal_state}")

    payload = {
        "ok": True,
        "companyName": company_name,
        "beforeVisibleCount": before_count,
        "selectedCount": select_count,
        "survivorIndex": survivor_index,
        "modalState": modal_state,
        "previewOnly": preview_only,
    }
    if preview_only:
        return payload

    completion = complete_merge(
        session,
        before_count=before_count,
        select_count=select_count,
    )
    payload.update(
        {
            "afterVisibleCount": completion["state"].get("countVisible"),
            "expectedVisibleCountAfterMerge": completion["expectedVisibleCountAfterMerge"],
            "finalUrl": completion["finalUrl"],
            "completion": completion,
        }
    )
    return payload
