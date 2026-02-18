from __future__ import annotations

from typing import Any


K_TITLE_LABEL = "\uc81c\ubaa9"
K_TITLE_REQUIRED_MSG = "\ud544\uc218\uac12\uc744 \uc785\ub825\ud574\uc8fc\uc138\uc694."


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


def set_required_title_field(
    session: "vibium.browser_sync.VibeSync",
    title: str,
) -> dict:
    result = eval_js(
        session,
        f"""
(() => {{
  const normalize = (text) => (text || "").replace(/\\s+/g, "").replace(/\\*/g, "").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const modal = [...document.querySelectorAll(".recatch-ant-modal")]
    .find((el) => isVisible(el));
  if (!modal) return {{ ok: false, reason: "modal_not_found" }};

  const wanted = normalize({K_TITLE_LABEL!r});
  const modalTop = modal.getBoundingClientRect().top;
  const titleNode = [...modal.querySelectorAll("label, div, span, p, strong")]
    .filter(isVisible)
    .find((el) => {{
      const txt = normalize(el.innerText || el.textContent || "");
      if (!txt || txt.length > 25) return false;
      return txt === wanted || txt.includes(wanted);
    }});

  const candidates = [...modal.querySelectorAll("input.recatch-ant-input, input[type='text'], input:not([type])")]
    .filter((el) => isVisible(el) && !el.disabled && !el.readOnly)
    .filter((el) => !(el.className || "").includes("recatch-ant-select-selection-search-input"))
    .filter((el) => el.getBoundingClientRect().top < modalTop + 260)
    .map((el) => {{
      const r = el.getBoundingClientRect();
      return {{ el, x: r.x, y: r.y }};
    }});

  let input = null;
  if (titleNode && candidates.length > 0) {{
    const tr = titleNode.getBoundingClientRect();
    input = candidates
      .sort((a, b) => (Math.abs(a.y - tr.y) - Math.abs(b.y - tr.y)) || (a.y - b.y))[0]
      ?.el || null;
  }}
  if (!input && candidates.length > 0) {{
    input = candidates.sort((a, b) => a.y - b.y)[0].el;
  }}

  if (!input) {{
    const top = (modal.innerText || "").split("\\n").map((x) => x.trim()).filter(Boolean).slice(0, 40);
    return {{ ok: false, reason: "title_input_not_found", top }};
  }}

  const setInputValue = (el, value) => {{
    const desc = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value");
    if (desc && desc.set) {{
      desc.set.call(el, value);
    }} else {{
      el.value = value;
    }}
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};

  input.focus();
  setInputValue(input, "");
  setInputValue(input, {title!r});
  input.dispatchEvent(new KeyboardEvent("keydown", {{ key: "Enter", code: "Enter", bubbles: true }}));
  input.dispatchEvent(new KeyboardEvent("keyup", {{ key: "Enter", code: "Enter", bubbles: true }}));
  input.dispatchEvent(new KeyboardEvent("keydown", {{ key: "Tab", code: "Tab", bubbles: true }}));
  input.dispatchEvent(new KeyboardEvent("keyup", {{ key: "Tab", code: "Tab", bubbles: true }}));
  input.blur();

  const value = (input.value || "").trim();
  const modalText = (modal.innerText || "").trim();
  const hasRequiredError = modalText.includes({K_TITLE_REQUIRED_MSG!r});

  return {{
    ok: value.length > 0,
    value,
    hasRequiredError,
    reason: value.length > 0 ? "ok" : "title_value_empty_after_set"
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}
