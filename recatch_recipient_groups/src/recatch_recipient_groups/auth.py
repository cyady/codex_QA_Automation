from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from .browser import current_url, eval_js, js_quote, visible_page_excerpt, wait_until


K_EMAIL_LOGIN_BUTTON = "이메일로 로그인"
K_SEARCH_PLACEHOLDER = "검색"


@dataclass(frozen=True)
class LoginCredential:
    email: str
    password: str


def parse_credential_file(credential_path: Path) -> LoginCredential:
    if not credential_path.exists():
        raise FileNotFoundError(f"credential file not found: {credential_path}")

    raw_lines = credential_path.read_text(encoding="utf-8").splitlines()
    lines = [
        line.strip()
        for line in raw_lines
        if line.strip() and not line.strip().startswith("#")
    ]

    kv: dict[str, str] = {}
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            kv[key.strip().lower()] = value.strip()

    email = (
        kv.get("email")
        or kv.get("id")
        or kv.get("username")
        or kv.get("user")
        or ""
    )
    password = kv.get("password") or kv.get("pw") or kv.get("passwd") or ""

    if (not email or not password) and len(lines) >= 2:
        if "=" not in lines[0] and "=" not in lines[1]:
            email = lines[0]
            password = lines[1]

    if not email or not password:
        raise ValueError(
            "credential file format invalid. Use either:\n"
            "email=...\npassword=...\n"
            "or first two lines as email/password."
        )

    return LoginCredential(email=email, password=password)


def _host_from_url(url: str) -> str:
    return urlparse(url).netloc.lower()


def is_recatch_logged_in(url: str, expected_host: str | None = None) -> bool:
    parsed = urlparse(url)
    current_host = parsed.netloc.lower()
    if not current_host:
        return False
    if expected_host and current_host != expected_host.lower():
        return False
    return "/login" not in parsed.path


def is_login_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const emailInput = [...document.querySelectorAll("input[name='email'], input#email, input[type='email'], input")]
    .find((el) => isVisible(el) && (
      (el.name || "").toLowerCase().includes("email")
      || (el.id || "").toLowerCase().includes("email")
      || (el.placeholder || "").toLowerCase().includes("email")
      || (el.type || "").toLowerCase() === "email"
    ));
  const pwInput = [...document.querySelectorAll("input[name='password'], input#password, input[type='password'], input")]
    .find((el) => isVisible(el) && (
      (el.name || "").toLowerCase().includes("password")
      || (el.id || "").toLowerCase().includes("password")
      || (el.type || "").toLowerCase() === "password"
    ));
  return !!emailInput && !!pwInput;
})()
""",
    )
    return bool(result)


def is_segments_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const buttons = [...document.querySelectorAll("button, [role='button'], a")]
    .filter((el) => isVisible(el))
    .map((el) => (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim());
  const hasTopAction = buttons.includes("수신자 그룹");
  const hasSearch = [...document.querySelectorAll("input")]
    .some((el) => isVisible(el) && (el.placeholder || "").includes({js_quote(K_SEARCH_PLACEHOLDER)}));
  const bodyTextLen = ((document.body && document.body.innerText) || "").trim().length;
  return bodyTextLen > 0 && (hasTopAction || hasSearch);
}})()
""",
    )
    return bool(result)


def _find_first(
    session: "vibium.browser_sync.VibeSync",
    selectors: list[str],
    timeout_ms: int,
) -> tuple[str | None, Any | None]:
    for selector in selectors:
        try:
            return selector, session.find(selector, timeout=timeout_ms)
        except Exception:
            continue
    return None, None


def _read_login_state(session: "vibium.browser_sync.VibeSync") -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const email = [...document.querySelectorAll("input#email, input[name='email'], input[placeholder='email@recatch.cc'], input[type='email'], input")]
    .find((el) => isVisible(el) && (
      (el.name || "").toLowerCase().includes("email")
      || (el.id || "").toLowerCase().includes("email")
      || (el.placeholder || "").toLowerCase().includes("email")
      || (el.type || "").toLowerCase() === "email"
    ));
  const password = [...document.querySelectorAll("input#password, input[name='password'], input[placeholder='password'], input[type='password'], input")]
    .find((el) => isVisible(el) && (
      (el.name || "").toLowerCase().includes("password")
      || (el.id || "").toLowerCase().includes("password")
      || (el.type || "").toLowerCase() === "password"
    ));
  const submit = [...document.querySelectorAll("button[type='submit'], button")]
    .find((el) => isVisible(el) && (
      (el.type || "").toLowerCase() === "submit"
      || (el.innerText || "").trim().includes({js_quote(K_EMAIL_LOGIN_BUTTON)})
    ));
  return {{
    emailReadback: email?.value || "",
    passwordReadbackLen: (password?.value || "").length,
    submitDisabled: !!(submit && submit.disabled),
    submitText: (submit?.innerText || "").trim()
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {}


def _fallback_fill_with_native_setter(
    session: "vibium.browser_sync.VibeSync",
    credential: LoginCredential,
) -> dict[str, Any]:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const email = [...document.querySelectorAll("input#email, input[name='email'], input[placeholder='email@recatch.cc'], input[type='email'], input")]
    .find((el) => isVisible(el) && (
      (el.name || "").toLowerCase().includes("email")
      || (el.id || "").toLowerCase().includes("email")
      || (el.placeholder || "").toLowerCase().includes("email")
      || (el.type || "").toLowerCase() === "email"
    ));
  const password = [...document.querySelectorAll("input#password, input[name='password'], input[placeholder='password'], input[type='password'], input")]
    .find((el) => isVisible(el) && (
      (el.name || "").toLowerCase().includes("password")
      || (el.id || "").toLowerCase().includes("password")
      || (el.type || "").toLowerCase() === "password"
    ));
  if (!email || !password) return {{ ok: false, reason: "fallback_input_not_found" }};
  const setInputValue = (el, value) => {{
    const desc = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value");
    if (desc && desc.set) desc.set.call(el, value);
    else el.value = value;
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};
  setInputValue(email, {js_quote(credential.email)});
  setInputValue(password, {js_quote(credential.password)});
  return {{
    ok: true,
    emailReadback: email.value || "",
    passwordReadbackLen: (password.value || "").length
  }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def _click_submit(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};
  const btn = [...document.querySelectorAll("button[type='submit'], button")]
    .find((el) => isVisible(el) && (
      (el.type || "").toLowerCase() === "submit"
      || (el.innerText || "").trim().includes({js_quote(K_EMAIL_LOGIN_BUTTON)})
    ));
  if (!btn || btn.disabled) return false;
  btn.click();
  return true;
}})()
""",
    )
    return bool(result)


def login_with_credentials(
    session: "vibium.browser_sync.VibeSync",
    credential: LoginCredential,
) -> dict[str, Any]:
    email_selectors = [
        "input#email",
        "input[name='email']",
        "input[placeholder='email@recatch.cc']",
        "input[type='email']",
    ]
    password_selectors = [
        "input#password",
        "input[name='password']",
        "input[placeholder='password']",
        "input[type='password']",
    ]

    email_selector, email_el = _find_first(session, email_selectors, 4000)
    password_selector, password_el = _find_first(session, password_selectors, 4000)
    if email_el is None:
        return {"ok": False, "reason": "email_input_not_found", "selectors": email_selectors}
    if password_el is None:
        return {"ok": False, "reason": "password_input_not_found", "selectors": password_selectors}

    try:
        _fallback_fill_with_native_setter(session, LoginCredential(email="", password=""))
        email_el.click(timeout=3000)
        email_el.type(credential.email, timeout=6000)
        password_el.click(timeout=3000)
        password_el.type(credential.password, timeout=6000)
    except Exception as exc:
        return {"ok": False, "reason": "vibium_type_failed", "error": str(exc)}

    state = _read_login_state(session)
    if not state.get("emailReadback") or bool(state.get("submitDisabled")):
        fallback = _fallback_fill_with_native_setter(session, credential)
        state = _read_login_state(session)
        state["fallback"] = fallback

    clicked = _click_submit(session)
    if not clicked:
        return {
            "ok": False,
            "reason": "submit_click_failed_or_disabled",
            "state": state,
        }

    return {
        "ok": True,
        "method": "hybrid-type-plus-native-fallback",
        "emailSelector": email_selector,
        "passwordSelector": password_selector,
        "submitDisabled": state.get("submitDisabled"),
        "emailReadback": state.get("emailReadback"),
        "passwordReadbackLen": state.get("passwordReadbackLen"),
        "submitText": state.get("submitText"),
    }


def ensure_recatch_login(
    session: "vibium.browser_sync.VibeSync",
    login_url: str,
    destination_url: str,
    credential: LoginCredential | None,
    manual_login_fallback: bool,
    log: Callable[[str], None],
    ready_check: Callable[["vibium.browser_sync.VibeSync"], bool] | None = None,
) -> None:
    expected_host = _host_from_url(destination_url) or _host_from_url(login_url)
    ready_check = ready_check or is_segments_page_ready

    log("navigate to login page")
    session.go(login_url)

    if is_recatch_logged_in(current_url(session), expected_host):
        log("already logged in")
    else:
        login_ready = wait_until(
            lambda: is_login_page_ready(session),
            timeout_sec=10.0,
            interval_sec=0.25,
        )
        if not login_ready and not manual_login_fallback:
            raise RuntimeError(
                f"login page not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
            )

        if credential is not None and is_login_page_ready(session):
            login_result = login_with_credentials(session, credential)
            log(f"credential login attempt: {login_result}")
            if not login_result.get("ok"):
                if not manual_login_fallback:
                    raise RuntimeError(f"credential login failed: {login_result}")
            else:
                logged_in = wait_until(
                    lambda: is_recatch_logged_in(current_url(session), expected_host),
                    timeout_sec=18.0,
                    interval_sec=0.3,
                )
                if not logged_in and not manual_login_fallback:
                    raise RuntimeError(
                        f"credential login timeout: excerpt={visible_page_excerpt(session)}"
                    )

        if not is_recatch_logged_in(current_url(session), expected_host):
            if manual_login_fallback and sys.stdin.isatty():
                while True:
                    url = current_url(session)
                    log(f"current url: {url}")
                    if is_recatch_logged_in(url, expected_host):
                        break
                    input("complete login in browser, then press Enter...")
            else:
                raise RuntimeError(
                    "not logged in after credential login, and manual fallback is unavailable."
                )

    if destination_url != current_url(session):
        log("navigate to destination page")
        session.go(destination_url)

    ready = wait_until(
        lambda: ready_check(session),
        timeout_sec=20.0,
        interval_sec=0.3,
    )
    log(f"destination page ready: {ready}")
    if not ready:
        raise RuntimeError(
            f"destination page is not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )

    log(f"final url after login: {current_url(session)}")
