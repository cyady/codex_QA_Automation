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
from urllib.parse import urlparse

from memo_seed_loader import load_memo_seed_records, render_note_text
from recatch_auth import (
    LoginCredential,
    current_url,
    ensure_recatch_login,
    eval_js,
    navigate_url,
    parse_credential_file,
    wait_until,
)


LOG_FILE_PATH: Path | None = None


@dataclass
class MemoRunResult:
    note_index: int
    csv_row: int
    token: str
    posted: bool
    details: str


def init_log_file(log_dir: Path) -> Path:
    global LOG_FILE_PATH
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE_PATH = log_dir / f"lead-memo-{ts}.log"
    return LOG_FILE_PATH


def log(message: str) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        safe = line.encode(enc, errors="replace").decode(enc, errors="replace")
        print(safe, flush=True)
    if LOG_FILE_PATH:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def default_csv_path() -> str:
    base_dir = Path(__file__).resolve().parents[1]
    candidate = base_dir / "recatch_bulk_import_withUI" / "data" / "DB_Migration_Company_Part.csv"
    return str(candidate)


def parse_env_file(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def load_env_file(raw_path: str | None) -> Path | None:
    candidate: Path | None = None
    if raw_path:
        candidate = Path(raw_path).expanduser()
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        if not candidate.exists():
            raise FileNotFoundError(f"env file not found: {candidate}")
    else:
        env_override = os.getenv("RECATCH_ENV_FILE", "").strip()
        if env_override:
            candidate = Path(env_override).expanduser()
            if not candidate.is_absolute():
                candidate = (Path.cwd() / candidate).resolve()
            if not candidate.exists():
                raise FileNotFoundError(f"env file not found: {candidate}")
        else:
            default_env = (Path.cwd() / ".env").resolve()
            if default_env.exists():
                candidate = default_env

    if candidate is None:
        return None

    for key, value in parse_env_file(candidate).items():
        os.environ.setdefault(key, value)
    return candidate


def env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "y"}


def env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return float(raw)


def parse_int_csv(raw: str | None) -> tuple[int, ...]:
    if raw is None:
        return ()
    values = [chunk.strip() for chunk in raw.split(",")]
    parsed = sorted({int(value) for value in values if value})
    return tuple(parsed)


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (Path.cwd() / path).resolve()


def resolve_optional_path(raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    return resolve_path(raw_path)


def extract_token(note_text: str) -> str:
    if note_text.startswith("[") and "]" in note_text:
        return note_text.split("]", 1)[0] + "]"
    return note_text[:24]


def save_screenshot(session: "vibium.browser_sync.VibeSync", step_name: str) -> Path:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_step = step_name.replace(" ", "_")
    filename = Path.cwd() / f"shot-{ts}-{safe_step}.png"
    data = session.screenshot()
    with open(filename, "wb") as handle:
        handle.write(data)
    log(f"screenshot saved: {filename}")
    return filename


def launch_vibium_session(headless: bool):
    import vibium

    browser_launcher = getattr(vibium, "browser", None)
    if browser_launcher is not None and callable(getattr(browser_launcher, "start", None)):
        browser = vibium.browser.start(headless=headless)
        page = browser.new_page()
        return browser, page

    manager = vibium.browser_sync()
    page = manager.launch(headless=headless)
    return manager, page


def close_vibium_session(browser_handle, session) -> None:
    stop = getattr(browser_handle, "stop", None)
    if callable(stop):
        stop()
        return

    quit_page = getattr(session, "quit", None)
    if callable(quit_page):
        quit_page()
        return

    close_page = getattr(session, "close", None)
    if callable(close_page):
        close_page()


def derive_base_url(lead_url: str) -> str:
    parsed = urlparse(lead_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"invalid lead url: {lead_url}")
    return f"{parsed.scheme}://{parsed.netloc}"


def build_login_url(base_url: str) -> str:
    return f"{base_url}/login?redirect=/leads"


def build_leads_url(base_url: str) -> str:
    return f"{base_url}/leads"


def lead_page_state(session: "vibium.browser_sync.VibeSync") -> dict[str, Any]:
    result = eval_js(
        session,
        """
(() => {
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const isDisabled = (el) =>
    !!el.disabled
    || el.getAttribute("aria-disabled") === "true"
    || el.classList.contains("recatch-ant-btn-disabled");

  const findMemoTab = () =>
    [...document.querySelectorAll("[role='tab'], button, a, div")]
      .filter((el) => isVisible(el))
      .map((el) => ({
        el,
        text: normalize(el.innerText || el.textContent || ""),
        role: el.getAttribute("role") || "",
        className: el.className || "",
        rect: el.getBoundingClientRect(),
        selected:
          el.getAttribute("aria-selected") === "true"
          || el.classList.contains("recatch-ant-tabs-tab-active")
      }))
      .filter((item) => item.text === "메모" || item.text.startsWith("메모 "))
      .sort((a, b) =>
        Number(b.selected) - Number(a.selected)
        || Number(b.role === "tab") - Number(a.role === "tab")
        || a.rect.top - b.rect.top
      )[0];

  const findEditor = () =>
    [...document.querySelectorAll("textarea, [contenteditable='true'], [role='textbox']")]
      .filter((el) => isVisible(el))
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const placeholder = normalize(
          el.getAttribute("placeholder")
          || el.getAttribute("data-placeholder")
          || el.getAttribute("aria-label")
          || el.dataset?.placeholder
          || ""
        );
        const text = normalize(el.innerText || el.textContent || el.value || "");
        const memoHint = /메모|memo/i.test(placeholder) || /메모|memo/i.test(text);
        return { el, rect, placeholder, text, memoHint };
      })
      .sort((a, b) =>
        Number(b.memoHint) - Number(a.memoHint)
        || b.rect.top - a.rect.top
        || b.rect.left - a.rect.left
      )[0];

  const editor = findEditor();
  const submit = editor
    ? [...document.querySelectorAll("button, [role='button']")]
        .filter((el) => isVisible(el))
        .map((el) => ({
          el,
          disabled: isDisabled(el),
          text: normalize(el.innerText || el.textContent || ""),
          rect: el.getBoundingClientRect(),
          ariaLabel: normalize(el.getAttribute("aria-label") || "")
        }))
        .filter((item) =>
          item.rect.top >= editor.rect.top - 80
          && item.rect.bottom <= editor.rect.bottom + 120
          && item.rect.left >= editor.rect.left - 40
        )
        .sort((a, b) =>
          Number(a.disabled) - Number(b.disabled)
          || b.rect.left - a.rect.left
          || a.rect.top - b.rect.top
        )[0]
    : null;

  return {
    url: location.href,
    memoTabFound: !!findMemoTab(),
    memoTabSelected: !!findMemoTab()?.selected,
    editorFound: !!editor,
    editorTag: editor?.el.tagName || "",
    editorPlaceholder: editor?.placeholder || "",
    editorTextLen: (editor?.text || "").length,
    submitFound: !!submit,
    submitDisabled: submit ? !!submit.disabled : null,
    submitText: submit?.text || "",
    submitAriaLabel: submit?.ariaLabel || "",
    // Support both lead and deal detail pages because the memo UI is shared.
    ready: (location.pathname.includes("/leads/") || location.pathname.includes("/deals/")) && !!editor,
  };
})()
""",
    )
    return result if isinstance(result, dict) else {"ready": False, "raw": result}


def wait_for_lead_page(session: "vibium.browser_sync.VibeSync", lead_url: str) -> None:
    navigate_url(session, lead_url)
    ready = wait_until(
        lambda: bool(lead_page_state(session).get("ready")),
        timeout_sec=20.0,
        interval_sec=0.3,
    )
    if ready:
        return

    memo_clicked = click_memo_tab(session)
    if memo_clicked:
        ready = wait_until(
            lambda: bool(lead_page_state(session).get("ready")),
            timeout_sec=10.0,
            interval_sec=0.3,
        )
    if not ready:
        raise RuntimeError(f"lead page did not become ready: {lead_page_state(session)}")


def click_memo_tab(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        """
(() => {
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const candidates = [...document.querySelectorAll("[role='tab'], button, a, div")]
    .filter((el) => isVisible(el))
    .map((el) => ({
      el,
      text: normalize(el.innerText || el.textContent || ""),
      role: el.getAttribute("role") || "",
      rect: el.getBoundingClientRect(),
      selected:
        el.getAttribute("aria-selected") === "true"
        || el.classList.contains("recatch-ant-tabs-tab-active")
    }))
    .filter((item) => item.text === "메모" || item.text.startsWith("메모 "))
    .sort((a, b) =>
      Number(a.selected) - Number(b.selected)
      || Number(b.role === "tab") - Number(a.role === "tab")
      || a.rect.top - b.rect.top
    );

  const target = candidates[0];
  if (!target) return { ok: false, reason: "memo_tab_not_found" };

  target.el.click();
  return { ok: true, alreadySelected: target.selected };
})()
""",
    )
    return isinstance(result, dict) and bool(result.get("ok"))


def set_note_input(session: "vibium.browser_sync.VibeSync", text: str) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const payload = {json.dumps(text, ensure_ascii=False)};
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const escapeHtml = (value) =>
    value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  const isVisible = (el) => {{
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const editor = [...document.querySelectorAll("textarea, [contenteditable='true'], [role='textbox']")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      const placeholder = normalize(
        el.getAttribute("placeholder")
        || el.getAttribute("data-placeholder")
        || el.getAttribute("aria-label")
        || el.dataset?.placeholder
        || ""
      );
      const text = normalize(el.innerText || el.textContent || el.value || "");
      const memoHint = /메모|memo/i.test(placeholder) || /메모|memo/i.test(text);
      return {{ el, rect, placeholder, text, memoHint }};
    }})
    .sort((a, b) =>
      Number(b.memoHint) - Number(a.memoHint)
      || b.rect.top - a.rect.top
      || b.rect.left - a.rect.left
    )[0];

  if (!editor) return {{ ok: false, reason: "memo_editor_not_found" }};

  const node = editor.el;
  node.focus();

  if (node.tagName === "TEXTAREA" || node.tagName === "INPUT") {{
    const proto = node.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
    if (setter) setter.call(node, payload);
    else node.value = payload;
    node.dispatchEvent(new Event("input", {{ bubbles: true }}));
    node.dispatchEvent(new Event("change", {{ bubbles: true }}));
    return {{
      ok: true,
      tag: node.tagName,
      readback: node.value || "",
      length: (node.value || "").length,
    }};
  }}

  try {{
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(node);
    selection.removeAllRanges();
    selection.addRange(range);
    document.execCommand("insertText", false, payload);
  }} catch (error) {{
    // Fallback below updates the editor directly.
  }}

  const afterExec = normalize(node.innerText || node.textContent || "");
  if (afterExec !== normalize(payload)) {{
    const html = payload
      .split(/\\r?\\n/)
      .map((line) => `<p>${{escapeHtml(line) || "<br>"}}</p>`)
      .join("");
    node.innerHTML = html;
    try {{
      node.dispatchEvent(new InputEvent("input", {{
        bubbles: true,
        inputType: "insertText",
        data: payload,
      }}));
    }} catch (error) {{
      node.dispatchEvent(new Event("input", {{ bubbles: true }}));
    }}
    node.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }}

  return {{
    ok: true,
    tag: node.tagName,
    readback: node.innerText || node.textContent || "",
    length: normalize(node.innerText || node.textContent || "").length,
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def submit_note(session: "vibium.browser_sync.VibeSync") -> dict[str, Any]:
    result = eval_js(
        session,
        """
(() => {
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const isDisabled = (el) =>
    !!el.disabled
    || el.getAttribute("aria-disabled") === "true"
    || el.classList.contains("recatch-ant-btn-disabled");

  const editor = [...document.querySelectorAll("textarea, [contenteditable='true'], [role='textbox']")]
    .filter((el) => isVisible(el))
    .map((el) => ({
      el,
      rect: el.getBoundingClientRect(),
      placeholder: normalize(
        el.getAttribute("placeholder")
        || el.getAttribute("data-placeholder")
        || el.getAttribute("aria-label")
        || el.dataset?.placeholder
        || ""
      ),
      text: normalize(el.innerText || el.textContent || el.value || "")
    }))
    .sort((a, b) =>
      Number(/메모|memo/i.test(b.placeholder) || /메모|memo/i.test(b.text))
      - Number(/메모|memo/i.test(a.placeholder) || /메모|memo/i.test(a.text))
      || b.rect.top - a.rect.top
      || b.rect.left - a.rect.left
    )[0];

  if (!editor) return { ok: false, reason: "memo_editor_not_found" };

  const composer =
    editor.el.closest?.("[data-testid='crm-conversation-editor'], .crm-conversation-editor")
    || editor.el.parentElement?.closest?.("[data-testid='crm-conversation-editor'], .crm-conversation-editor")
    || null;

  const composerButtons = composer
    ? [...composer.querySelectorAll("button, [role='button'], a, [tabindex='0']")]
        .filter((el) => isVisible(el))
        .map((el) => ({
          el,
          rect: el.getBoundingClientRect(),
          text: normalize(el.innerText || el.textContent || ""),
          ariaLabel: normalize(el.getAttribute("aria-label") || ""),
          disabled: isDisabled(el),
          className: el.className || "",
        }))
        .sort((a, b) =>
          Number(a.disabled) - Number(b.disabled)
          || Number(/primary|solid/.test(b.className)) - Number(/primary|solid/.test(a.className))
          || b.rect.right - a.rect.right
          || a.rect.top - b.rect.top
        )
    : [];

  const submit = composerButtons[0]
    || [...document.querySelectorAll("button, [role='button']")]
    .filter((el) => isVisible(el))
    .map((el) => ({
      el,
      rect: el.getBoundingClientRect(),
      text: normalize(el.innerText || el.textContent || ""),
      ariaLabel: normalize(el.getAttribute("aria-label") || ""),
      disabled: isDisabled(el),
    }))
    .filter((item) =>
      item.rect.top >= editor.rect.top - 80
      && item.rect.bottom <= editor.rect.bottom + 120
      && item.rect.left >= editor.rect.left - 40
    )
    .sort((a, b) =>
      Number(a.disabled) - Number(b.disabled)
      || b.rect.left - a.rect.left
      || a.rect.top - b.rect.top
    )[0];

  const fallbackSubmit = !submit
    ? [...document.querySelectorAll("button, [role='button'], a, [tabindex='0']")]
        .filter((el) => isVisible(el))
        .map((el) => ({
          el,
          rect: el.getBoundingClientRect(),
          text: normalize(el.innerText || el.textContent || ""),
          ariaLabel: normalize(el.getAttribute("aria-label") || ""),
          disabled: isDisabled(el),
          className: el.className || "",
        }))
        .filter((item) =>
          item.rect.top >= editor.rect.bottom - 80
          && item.rect.bottom <= editor.rect.bottom + 80
          && item.rect.left >= editor.rect.right - 240
        )
        .sort((a, b) =>
          Number(a.disabled) - Number(b.disabled)
          || Number(/setting/i.test(a.ariaLabel)) - Number(/setting/i.test(b.ariaLabel))
          || b.rect.right - a.rect.right
          || a.rect.top - b.rect.top
        )[0]
    : null;

  const pointFallback = !submit && !fallbackSubmit
    ? (() => {
        const offsets = [
          [36, 36],
          [52, 44],
          [68, 44],
          [52, 68],
        ];
        const findClickable = (node) => {
          let current = node;
          while (current && current !== document.body) {
            if (
              current.matches?.("button, [role='button'], a, [tabindex='0']")
              || typeof current.onclick === "function"
            ) {
              const rect = current.getBoundingClientRect();
              return {
                el: current,
                rect,
                text: normalize(current.innerText || current.textContent || ""),
                ariaLabel: normalize(current.getAttribute("aria-label") || ""),
                disabled: isDisabled(current),
                className: current.className || "",
              };
            }
            current = current.parentElement;
          }
          return null;
        };

        for (const [dx, dy] of offsets) {
          const x = window.innerWidth - dx;
          const y = window.innerHeight - dy;
          const found = findClickable(document.elementFromPoint(x, y));
          if (!found) continue;
          if (/setting/i.test(found.ariaLabel)) continue;
          return found;
        }
        return null;
      })()
    : null;

  const target = submit || fallbackSubmit || pointFallback;

  if (!target) return { ok: false, reason: "submit_button_not_found" };
  if (target.disabled) {
    return {
      ok: false,
      reason: "submit_button_disabled",
      text: target.text,
      ariaLabel: target.ariaLabel,
    };
  }

  target.el.click();
  return {
    ok: true,
    text: target.text,
    ariaLabel: target.ariaLabel,
  };
})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def page_contains_text(session: "vibium.browser_sync.VibeSync", needle: str) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const haystack = (document.body?.innerText || "").replace(/\\s+/g, " ");
  return haystack.includes({json.dumps(needle, ensure_ascii=False)});
}})()
""",
    )
    return bool(result)


def editor_contains_text(session: "vibium.browser_sync.VibeSync", needle: str) -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const target = {json.dumps(needle, ensure_ascii=False)};
  const normalize = (value) => (value || "").replace(/\\s+/g, " ").trim();
  const isVisible = (el) => {{
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const editor = [...document.querySelectorAll("textarea, [contenteditable='true'], [role='textbox']")]
    .filter((el) => isVisible(el))
    .map((el) => {{
      const rect = el.getBoundingClientRect();
      const placeholder = normalize(
        el.getAttribute("placeholder")
        || el.getAttribute("data-placeholder")
        || el.getAttribute("aria-label")
        || el.dataset?.placeholder
        || ""
      );
      const text = normalize(el.innerText || el.textContent || el.value || "");
      const memoHint = /메모|memo/i.test(placeholder) || /메모|memo/i.test(text);
      return {{ text, rect, memoHint }};
    }})
    .sort((a, b) =>
      Number(b.memoHint) - Number(a.memoHint)
      || b.rect.top - a.rect.top
      || b.rect.left - a.rect.left
    )[0];

  if (!editor) return false;
  return editor.text.includes(target);
}})()
""",
    )
    return bool(result)


def post_note(
    session: "vibium.browser_sync.VibeSync",
    *,
    note_text: str,
    token: str,
    settle_delay_sec: float,
) -> None:
    input_result = set_note_input(session, note_text)
    if not input_result.get("ok"):
        raise RuntimeError(f"set note input failed: {input_result}")

    submit_result = submit_note(session)
    if not submit_result.get("ok"):
        raise RuntimeError(f"submit note failed: {submit_result}")

    cleared = wait_until(
        lambda: not editor_contains_text(session, token),
        timeout_sec=12.0,
        interval_sec=0.25,
    )
    if not cleared:
        raise RuntimeError(f"note editor did not clear after submit: {token}")

    if settle_delay_sec > 0:
        time.sleep(settle_delay_sec)


def write_preview(preview_path: Path, notes: list[str]) -> None:
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text("\n\n".join(notes), encoding="utf-8")


def pause_at_checkpoint(
    *,
    session: "vibium.browser_sync.VibeSync",
    global_posted_count: int,
) -> None:
    save_screenshot(session, f"lead-memo-checkpoint-{global_posted_count:04d}")
    log(f"checkpoint reached: posted={global_posted_count}")
    if sys.stdin.isatty():
        input(f"checkpoint {global_posted_count} reached. complete your task, then press Enter...")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument("--env-file")
    bootstrap_args, _ = bootstrap.parse_known_args(argv)
    loaded_env_file = load_env_file(bootstrap_args.env_file)

    parser = argparse.ArgumentParser(
        description="Bulk-add memos to a single Re:catch lead with Vibium."
    )
    parser.add_argument("--env-file", default=str(loaded_env_file) if loaded_env_file else None)
    parser.add_argument("--lead-url", required=True, help="target lead URL")
    parser.add_argument("--csv", default=os.getenv("RECATCH_MEMO_CSV", default_csv_path()))
    parser.add_argument("--count", type=int, default=int(os.getenv("RECATCH_MEMO_COUNT", "500")))
    parser.add_argument("--start-row", type=int, default=int(os.getenv("RECATCH_MEMO_START_ROW", "1")))
    parser.add_argument(
        "--credential-file",
        default=os.getenv("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt"),
    )
    parser.add_argument(
        "--manual-login-fallback",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_MANUAL_LOGIN_FALLBACK", False),
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_HEADLESS", False),
    )
    parser.add_argument(
        "--keep-open",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_KEEP_OPEN", False),
    )
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_MEMO_DRY_RUN", False),
    )
    parser.add_argument(
        "--run-tag",
        default=os.getenv("RECATCH_MEMO_RUN_TAG", dt.datetime.now().strftime("MEMO-%Y%m%d-%H%M%S")),
    )
    parser.add_argument(
        "--delay-sec",
        type=float,
        default=env_float("RECATCH_MEMO_DELAY_SEC", 0.3),
    )
    parser.add_argument(
        "--screenshot-every",
        type=int,
        default=int(os.getenv("RECATCH_MEMO_SCREENSHOT_EVERY", "100")),
    )
    parser.add_argument(
        "--pause-at",
        default=os.getenv("RECATCH_MEMO_PAUSE_AT", ""),
        help="comma-separated global posted-count checkpoints to pause at",
    )
    parser.add_argument(
        "--progress-offset",
        type=int,
        default=int(os.getenv("RECATCH_MEMO_PROGRESS_OFFSET", "0")),
        help="number of memos already posted before this run",
    )
    parser.add_argument("--preview-output")
    parser.add_argument("--log-dir", default=os.getenv("RECATCH_MEMO_LOG_DIR", "logs"))

    args = parser.parse_args(argv)
    if args.count < 1:
        parser.error("--count must be >= 1")
    if args.start_row < 1:
        parser.error("--start-row must be >= 1")
    if args.progress_offset < 0:
        parser.error("--progress-offset must be >= 0")
    if args.manual_login_fallback and args.headless:
        parser.error("--manual-login-fallback cannot be used with --headless")
    args.pause_points = parse_int_csv(args.pause_at)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    init_log_file(resolve_path(args.log_dir))

    log("=" * 72)
    log("Vibium: lead memo bulk fill")
    log("=" * 72)
    log(f"log file: {LOG_FILE_PATH}")

    csv_path = resolve_path(args.csv)
    log(f"lead url: {args.lead_url}")
    log(f"csv path: {csv_path}")
    log(f"start row: {args.start_row}")
    log(f"count: {args.count}")
    log(f"run tag: {args.run_tag}")
    log(f"progress offset: {args.progress_offset}")
    if args.pause_points:
        log(f"pause checkpoints: {args.pause_points}")

    records = load_memo_seed_records(csv_path, start_row=args.start_row, limit=args.count)
    if not records:
        log("no records loaded from csv")
        return 1

    notes = [
        render_note_text(record, note_index=index, run_tag=args.run_tag)
        for index, record in enumerate(records, start=1)
    ]
    log(f"prepared notes: {len(notes)}")
    log(f"first preview: {notes[0]}")

    if args.preview_output:
        preview_path = resolve_path(args.preview_output)
        write_preview(preview_path, notes)
        log(f"preview output written: {preview_path}")

    if args.dry_run:
        log("dry-run enabled; browser launch skipped")
        return 0

    credential: LoginCredential | None = None
    credential_path = resolve_optional_path(args.credential_file)
    if credential_path is not None:
        try:
            credential = parse_credential_file(credential_path)
            log(f"credential file loaded: {credential_path}")
        except Exception as exc:
            if args.manual_login_fallback:
                log(f"credential load failed, manual fallback enabled: {exc}")
            else:
                log(f"credential load failed: {exc}")
                return 1

    base_url = derive_base_url(args.lead_url)
    login_url = build_login_url(base_url)
    leads_url = build_leads_url(base_url)

    browser_handle, session = launch_vibium_session(headless=args.headless)
    results: list[MemoRunResult] = []
    exit_code = 0

    try:
        ensure_recatch_login(
            session=session,
            login_url=login_url,
            leads_url=leads_url,
            credential=credential,
            manual_login_fallback=args.manual_login_fallback,
            log=log,
        )
        wait_for_lead_page(session, args.lead_url)
        log(f"lead page ready: {lead_page_state(session)}")
        if args.screenshot_every != 0:
            save_screenshot(session, "lead-memo-start")

        for note_index, (record, note_text) in enumerate(zip(records, notes), start=1):
            token = extract_token(note_text)
            log(f"posting memo {note_index}/{len(notes)} from csv row {record.row_number}: {token}")
            try:
                if note_index > 1 and current_url(session) != args.lead_url:
                    wait_for_lead_page(session, args.lead_url)
                post_note(
                    session,
                    note_text=note_text,
                    token=token,
                    settle_delay_sec=args.delay_sec,
                )
                results.append(
                    MemoRunResult(
                        note_index=note_index,
                        csv_row=record.row_number,
                        token=token,
                        posted=True,
                        details="posted",
                    )
                )
            except Exception as exc:
                exit_code = 1
                log(f"memo post failed at index {note_index}: {exc}")
                save_screenshot(session, f"lead-memo-failed-{note_index:04d}")
                results.append(
                    MemoRunResult(
                        note_index=note_index,
                        csv_row=record.row_number,
                        token=token,
                        posted=False,
                        details=str(exc),
                    )
                )
                break

            if args.screenshot_every > 0 and note_index % args.screenshot_every == 0:
                save_screenshot(session, f"lead-memo-{note_index:04d}")

            global_posted_count = args.progress_offset + len(results)
            if global_posted_count in args.pause_points:
                pause_at_checkpoint(
                    session=session,
                    global_posted_count=global_posted_count,
                )

        posted_count = sum(1 for item in results if item.posted)
        log(f"posted memos: {posted_count}/{len(notes)}")
    finally:
        if exit_code == 0 and results and args.screenshot_every != 0:
            save_screenshot(session, "lead-memo-finish")
        if args.keep_open:
            log("keep-open enabled; browser left running")
        else:
            close_vibium_session(browser_handle, session)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
