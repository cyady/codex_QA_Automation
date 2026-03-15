from __future__ import annotations

import json
import time
from typing import Any, Callable
from urllib.parse import quote, urlencode


DOM_HELPERS_JS = r"""
const textOf = (el) => ((el?.innerText || el?.textContent || "").replace(/\s+/g, " ").trim());
const isVisible = (el) => {
  if (!el) return false;
  const rect = el.getBoundingClientRect();
  if (rect.width <= 0 || rect.height <= 0) return false;
  const style = getComputedStyle(el);
  return style.display !== "none" && style.visibility !== "hidden";
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
        return {key: unwrap_eval(item) for key, item in value.items()}

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


def build_login_url(base_url: str, redirect_path: str) -> str:
    query = urlencode({"redirect": redirect_path}, quote_via=quote)
    return build_default_url(base_url, f"/login?{query}")


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
