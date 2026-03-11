from __future__ import annotations

import json
import time
from typing import Any, Callable
from urllib.parse import quote, urlencode, urlparse


K_SEARCH_PLACEHOLDER = "검색"
DOM_HELPERS_JS = r"""
const textOf = (el) => ((el?.innerText || el?.textContent || "").replace(/\s+/g, " ").trim());
const isVisible = (el) => {
  if (!el) return false;
  const rect = el.getBoundingClientRect();
  if (rect.width <= 0 || rect.height <= 0) return false;
  const style = getComputedStyle(el);
  return style.display !== "none" && style.visibility !== "hidden";
};
const isDisabled = (el) =>
  !!el?.disabled
  || el?.getAttribute?.("aria-disabled") === "true"
  || el?.classList?.contains?.("recatch-ant-btn-disabled");
const matchesText = (actual, wanted, exact) => exact ? actual === wanted : actual.includes(wanted);
const candidateMatches = (candidate, wanted, exact, topMin, topMax, leftMin, leftMax) => {
  if (!isVisible(candidate)) return false;
  const actual = textOf(candidate);
  if (!matchesText(actual, wanted, exact)) return false;
  const rect = candidate.getBoundingClientRect();
  if (topMin !== null && rect.top < topMin) return false;
  if (topMax !== null && rect.top > topMax) return false;
  if (leftMin !== null && rect.left < leftMin) return false;
  if (leftMax !== null && rect.left > leftMax) return false;
  return true;
};
const visibleContainers = (containerText) => {
  if (!containerText) return [document.body];
  return [...document.querySelectorAll("div, section, form, main, aside")]
    .filter((el) => isVisible(el) && textOf(el).includes(containerText));
};
const findTextCandidates = (selectors, wanted, exact, containerText, topMin, topMax, leftMin, leftMax) => {
  const containers = visibleContainers(containerText);
  const collected = [];
  for (const container of containers) {
    for (const candidate of container.querySelectorAll(selectors)) {
      if (!candidateMatches(candidate, wanted, exact, topMin, topMax, leftMin, leftMax)) continue;
      collected.push(candidate);
    }
  }
  return [...new Set(collected)];
};
const clickElement = (el) => {
  if (!el) return false;
  try {
    el.scrollIntoView({ block: "center", inline: "nearest" });
  } catch (error) {
    // Keep going.
  }
  ["pointerdown", "mousedown", "mouseup", "click"].forEach((name) => {
    el.dispatchEvent(new MouseEvent(name, { bubbles: true, cancelable: true, view: window }));
  });
  if (typeof el.click === "function") el.click();
  return true;
};
const setInputValue = (el, value) => {
  if (!el) return false;
  const proto = el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
  const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
  if (setter) setter.call(el, value);
  else el.value = value;
  el.dispatchEvent(new Event("input", { bubbles: true }));
  el.dispatchEvent(new Event("change", { bubbles: true }));
  return true;
};
"""


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


def js_quote(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True)


def current_url(session: "vibium.browser_sync.VibeSync") -> str:
    return str(eval_js(session, "location.href"))


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


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def build_default_url(base_url: str, path: str) -> str:
    return f"{normalize_base_url(base_url)}{path}"


def build_segments_path(team_slug: str) -> str:
    query: dict[str, str] = {}
    if team_slug:
        query["teamSlug"] = team_slug
    return "/segments" + (f"?{urlencode(query, quote_via=quote)}" if query else "")


def build_login_url(base_url: str, team_slug: str, redirect_path: str) -> str:
    query: dict[str, str] = {"redirect": redirect_path}
    if team_slug:
        query["teamSlug"] = team_slug
    return build_default_url(base_url, f"/login?{urlencode(query, quote_via=quote)}")


def build_segments_url(base_url: str, team_slug: str) -> str:
    return build_default_url(base_url, build_segments_path(team_slug))


def visible_page_excerpt(
    session: "vibium.browser_sync.VibeSync",
    limit: int = 30,
) -> list[str]:
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


def visible_text_exists(session: "vibium.browser_sync.VibeSync", text: str) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const wanted = {js_quote(text)};
  return [...document.querySelectorAll("body, div, span, button, li, a, input, textarea")]
    .some((el) => isVisible(el) && textOf(el).includes(wanted));
}})()
""",
    )
    return bool(result)


def click_text(
    session: "vibium.browser_sync.VibeSync",
    text: str,
    *,
    selectors: str = "button, [role='button'], a, div, span, li",
    exact: bool = True,
    container_text: str | None = None,
    top_min: float | None = None,
    top_max: float | None = None,
    left_min: float | None = None,
    left_max: float | None = None,
    prefer_last: bool = False,
    allow_disabled: bool = False,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const matches = findTextCandidates(
    {js_quote(selectors)},
    {js_quote(text)},
    {str(exact).lower()},
    {js_quote(container_text)},
    {js_quote(top_min)},
    {js_quote(top_max)},
    {js_quote(left_min)},
    {js_quote(left_max)}
  )
    .filter((candidate) => {str(allow_disabled).lower()} || !isDisabled(candidate))
    .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
  const target = { "matches[matches.length - 1]" if prefer_last else "matches[0]" };
  if (!target) {{
    return {{ ok: false, reason: "target_not_found", matchCount: matches.length }};
  }}
  const rect = target.getBoundingClientRect();
  clickElement(target);
  return {{
    ok: true,
    top: rect.top,
    left: rect.left,
    text: textOf(target),
    matchCount: matches.length
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def set_input_value(
    session: "vibium.browser_sync.VibeSync",
    value: str,
    *,
    selectors: str = "input, textarea",
    container_text: str | None = None,
    placeholder_excludes: tuple[str, ...] = (K_SEARCH_PLACEHOLDER,),
    prefer_last: bool = True,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  const exclude = {js_quote(list(placeholder_excludes))};
  const containers = visibleContainers({js_quote(container_text)});
  const candidates = [];
  for (const container of containers) {{
    for (const candidate of container.querySelectorAll({js_quote(selectors)})) {{
      if (!isVisible(candidate)) continue;
      const placeholder = candidate.getAttribute("placeholder") || "";
      if (exclude.some((item) => placeholder.includes(item))) continue;
      candidates.push(candidate);
    }}
  }}
  const unique = [...new Set(candidates)];
  const sorted = unique.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
  const target = { "sorted[sorted.length - 1]" if prefer_last else "sorted[0]" };
  if (!target) {{
    return {{ ok: false, reason: "input_not_found", count: unique.length }};
  }}
  setInputValue(target, {js_quote(value)});
  target.focus();
  return {{
    ok: true,
    tag: target.tagName,
    placeholder: target.getAttribute("placeholder") || "",
    value: target.value || ""
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def read_visible_button_texts(session: "vibium.browser_sync.VibeSync") -> list[str]:
    result = eval_js(
        session,
        f"""
(() => {{
  {DOM_HELPERS_JS}
  return [...document.querySelectorAll("button, [role='button'], a")]
    .filter((el) => isVisible(el))
    .map((el) => textOf(el))
    .filter(Boolean);
}})()
""",
    )
    return result if isinstance(result, list) else []


def find_button_text(
    session: "vibium.browser_sync.VibeSync",
    contains_text: str,
) -> str | None:
    for button_text in read_visible_button_texts(session):
        if contains_text in button_text:
            return button_text
    return None


def read_recipient_count_from_page(
    session: "vibium.browser_sync.VibeSync",
) -> int | None:
    pattern = js_quote(r"수신자 목록\s*([0-9,]+)")
    result = eval_js(
        session,
        f"""
(() => {{
  const text = ((document.body && document.body.innerText) || "").replace(/\s+/g, " ").trim();
  const match = text.match(new RegExp({pattern}));
  if (!match) return null;
  return Number(match[1].replace(/,/g, ""));
}})()
""",
    )
    return int(result) if isinstance(result, (int, float)) else None


def read_expected_dynamic_count(
    session: "vibium.browser_sync.VibeSync",
) -> int | None:
    pattern = js_quote(r"예상 수신자\s*([0-9,]+)명")
    result = eval_js(
        session,
        f"""
(() => {{
  const text = ((document.body && document.body.innerText) || "").replace(/\s+/g, " ").trim();
  const match = text.match(new RegExp({pattern}));
  if (!match) return null;
  return Number(match[1].replace(/,/g, ""));
}})()
""",
    )
    return int(result) if isinstance(result, (int, float)) else None


def extract_group_id(url: str) -> int | None:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 2 and parts[0] == "segments" and parts[1].isdigit():
        return int(parts[1])
    return None
