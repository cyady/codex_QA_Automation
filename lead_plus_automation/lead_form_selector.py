from __future__ import annotations

import time
from typing import Any, Callable


K_MODAL_TITLE = "\uc0c8\ub85c\uc6b4 \ub9ac\ub4dc \uc0dd\uc131"
K_COMPANY_SELECT_LABEL = "\ud68c\uc0ac \uc120\ud0dd"
K_CONTACT_SELECT_LABEL = "\uc5f0\ub77d\ucc98 \uc120\ud0dd"
K_BASIC_INFO_LABEL = "\uae30\ubcf8 \uc815\ubcf4"


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
    predicate: Callable[[], bool],
    timeout_sec: float,
    interval_sec: float = 0.2,
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


def _probe_modal_state(session: "vibium.browser_sync.VibeSync") -> dict:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const modal = [...document.querySelectorAll(".recatch-ant-modal")]
    .find((el) => isVisible(el));
  if (!modal) return {{ modalOpen: false, ready: false, top: [] }};

  const modalTitle = (modal.querySelector(".recatch-ant-modal-title")?.innerText || "").trim();
  const top = (modal.innerText || "").split("\\n").map((x) => x.trim()).filter(Boolean).slice(0, 80);
  const hasBasicInfo = top.some((x) => x.includes({K_BASIC_INFO_LABEL!r}));

  const fieldRowsCount = modal.querySelectorAll(".sc-d9c25054-1").length;
  const dataFieldCount = modal.querySelectorAll("[data-field-id]").length;
  const inputCount = [...modal.querySelectorAll("input, textarea")]
    .filter((el) => isVisible(el) && !el.disabled && !el.readOnly && (el.type || "").toLowerCase() !== "hidden")
    .length;

  const hasCompanySelect = top.some((x) => x.includes({K_COMPANY_SELECT_LABEL!r}));
  const hasContactSelect = top.some((x) => x.includes({K_CONTACT_SELECT_LABEL!r}));

  const ready = hasBasicInfo || fieldRowsCount > 0 || dataFieldCount > 0 || inputCount >= 2;
  return {{
    modalOpen: modalTitle.includes({K_MODAL_TITLE!r}),
    ready,
    hasBasicInfo,
    fieldRowsCount,
    dataFieldCount,
    inputCount,
    hasCompanySelect,
    hasContactSelect,
    top
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"modalOpen": False, "ready": False, "raw": result}


def _click_selector_by_label(session: "vibium.browser_sync.VibeSync", label: str) -> dict:
    result = eval_js(
        session,
        f"""
(() => {{
  const normalize = (text) => (text || "").replace(/\\s+/g, "").replace(/\\*/g, "").replace(/[:]/g, "").trim();
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const modal = [...document.querySelectorAll(".recatch-ant-modal")]
    .find((el) => isVisible(el));
  if (!modal) return {{ ok: false, reason: "modal_not_found" }};

  const wanted = normalize({label!r});
  const labelNode = [...modal.querySelectorAll("*")]
    .filter((el) => isVisible(el))
    .find((el) => {{
      const txt = normalize(el.innerText || el.textContent || "");
      if (!txt) return false;
      if (txt.length > 30) return false;
      return txt === wanted || txt.includes(wanted);
    }});
  if (!labelNode) return {{ ok: false, reason: "label_not_found", label: {label!r} }};

  let row = labelNode.closest("div");
  let target = null;
  for (let i = 0; i < 6 && row && row !== modal; i += 1) {{
    target =
      row.querySelector(".recatch-ant-select-selector")
      || row.querySelector("[role='combobox']")
      || row.querySelector("[aria-haspopup='listbox']")
      || row.querySelector("input.recatch-ant-select-selection-search-input")
      || row.querySelector("input");
    if (target && isVisible(target)) break;
    row = row.parentElement;
  }}
  if (!target || !isVisible(target)) target = labelNode;

  const rect = target.getBoundingClientRect();
  target.click();
  return {{
    ok: true,
    label: {label!r},
    targetTag: target.tagName,
    centerX: rect.left + rect.width / 2,
    centerY: rect.top + rect.height / 2
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def _select_dropdown_option(
    session: "vibium.browser_sync.VibeSync",
    target_text: str | None,
) -> dict:
    script = """
(() => {
  const normalize = (text) => (text || "").replace(/\\s+/g, "").trim().toLowerCase();
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };

  const candidates = [
    ...document.querySelectorAll(".recatch-ant-select-item-option"),
    ...document.querySelectorAll("li[role='option']"),
    ...document.querySelectorAll("[role='option']"),
  ]
    .filter((el) => isVisible(el))
    .filter((el) => (el.getAttribute("aria-disabled") || "").toLowerCase() !== "true")
    .filter((el) => !(el.className || "").includes("disabled"))
    .map((el) => ({
      el,
      text: (el.innerText || el.textContent || "").trim(),
      y: el.getBoundingClientRect().top
    }))
    .filter((x) => x.text && x.text !== "-")
    .sort((a, b) => a.y - b.y);

  if (!candidates.length) return { ok: false, reason: "dropdown_option_not_found" };

  const wanted = normalize(__TARGET_TEXT__);
  let picked = null;
  if (wanted) {
    picked =
      candidates.find((x) => normalize(x.text) === wanted)
      || candidates.find((x) => normalize(x.text).includes(wanted))
      || candidates.find((x) => wanted.includes(normalize(x.text)));
  }
  if (!picked) picked = candidates[0];

  picked.el.click();
  return { ok: true, selectedText: picked.text, wantedText: __TARGET_TEXT__ };
})()
"""
    target_literal = "null" if target_text is None else repr(target_text)
    result = eval_js(
        session,
        script.replace("__TARGET_TEXT__", target_literal),
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def _apply_single_selector(
    session: "vibium.browser_sync.VibeSync",
    label: str,
    target_text: str | None,
) -> dict:
    click_result = _click_selector_by_label(session, label)
    if not click_result.get("ok"):
        return {"ok": False, "label": label, "click": click_result}

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
  const hasOption = [...document.querySelectorAll(".recatch-ant-select-item-option, [role='option']")]
    .some((el) => isVisible(el));
  return hasOption;
})()
""",
            )
        ),
        timeout_sec=2.0,
        interval_sec=0.15,
    )
    if not opened:
        return {"ok": False, "label": label, "reason": "dropdown_not_opened", "click": click_result}

    option_result = _select_dropdown_option(session, target_text=target_text)
    if not option_result.get("ok"):
        return {"ok": False, "label": label, "reason": "option_select_failed", "detail": option_result}

    return {
        "ok": True,
        "label": label,
        "selected": option_result.get("selectedText"),
        "wantedText": target_text,
    }


def ensure_lead_form_ready(
    session: "vibium.browser_sync.VibeSync",
    log: Callable[[str], None],
    company_select_text: str | None = None,
    contact_select_text: str | None = None,
) -> dict:
    initial = _probe_modal_state(session)
    if not initial.get("modalOpen"):
        return {"ok": False, "reason": "create_modal_not_open", "state": initial}
    if initial.get("ready"):
        return {"ok": True, "reason": "already_ready", "state": initial, "steps": []}

    steps: list[dict] = []
    selector_plan = [
        (K_COMPANY_SELECT_LABEL, company_select_text),
        (K_CONTACT_SELECT_LABEL, contact_select_text),
    ]
    for label, target_text in selector_plan:
        step = _apply_single_selector(session, label, target_text=target_text)
        steps.append(step)
        log(f"selector step ({label}): {step}")

        now = _probe_modal_state(session)
        if now.get("ready"):
            return {"ok": True, "reason": "became_ready", "state": now, "steps": steps}

    # Final fallback wait: UI can render field rows with delay after selection.
    wait_until(lambda: bool(_probe_modal_state(session).get("ready")), timeout_sec=3.0, interval_sec=0.2)
    final_state = _probe_modal_state(session)
    if final_state.get("ready"):
        return {"ok": True, "reason": "ready_after_delay", "state": final_state, "steps": steps}

    return {"ok": False, "reason": "form_not_ready_after_selector_steps", "state": final_state, "steps": steps}
