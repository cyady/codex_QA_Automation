from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse


K_EMAIL_LOGIN_BUTTON = "\uc774\uba54\uc77c\ub85c \ub85c\uadf8\uc778"
K_SEARCH_PLACEHOLDER = "\uac80\uc0c9"


@dataclass
class LoginCredential:
    email: str
    password: str


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


def _host_from_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower()


def is_recatch_logged_in(url: str, expected_host: str | None = None) -> bool:
    parsed = urlparse(url)
    current_host = parsed.netloc.lower()
    if not current_host:
        return False
    if expected_host and current_host != expected_host.lower():
        return False
    return "/login" not in parsed.path


def is_leads_page_ready(session: "vibium.browser_sync.VibeSync") -> bool:
    result = eval_js(
        session,
        f"""
(() => {{
  const href = location.href || "";
  const isLeadsRoute = /\\/leads(\\?|$|\\/)/.test(href);
  const isVisible = (el) => {{
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  }};

  const hasTopActionButton = [...document.querySelectorAll("button")]
    .some((el) => isVisible(el) && el.getBoundingClientRect().top < 220);
  const hasSearchInput = [...document.querySelectorAll("input")]
    .some((el) => isVisible(el) && (el.placeholder || "").includes({K_SEARCH_PLACEHOLDER!r}));
  const hasLeadRows = [...document.querySelectorAll("table tbody tr, [role='row'], .recatch-ant-table-row")]
    .some((el) => isVisible(el));
  const hasLeadsMenu = ((document.body && document.body.innerText) || "").includes("모든 리드");
  const spinning = !!document.querySelector(".recatch-ant-spin-spinning, .recatch-ant-spin-dot-spin");
  const bodyTextLen = ((document.body && document.body.innerText) || "").trim().length;

  return (
    isLeadsRoute
    && (hasTopActionButton || hasSearchInput || hasLeadRows || hasLeadsMenu)
    && bodyTextLen > 0
    && !spinning
  );
}})()
""",
    )
    return bool(result)


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


def _read_login_state(session: "vibium.browser_sync.VibeSync") -> dict:
    result = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
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
      || (el.innerText || "").trim().includes("이메일로 로그인")
    ));

  return {
    emailReadback: email?.value || "",
    passwordReadbackLen: (password?.value || "").length,
    submitDisabled: !!(submit && submit.disabled),
    submitText: (submit?.innerText || "").trim()
  };
})()
""",
    )
    return result if isinstance(result, dict) else {}


def _fallback_fill_with_native_setter(
    session: "vibium.browser_sync.VibeSync",
    credential: LoginCredential,
) -> dict:
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
    if (desc && desc.set) {{
      desc.set.call(el, value);
    }} else {{
      el.value = value;
    }}
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};

  email.focus();
  setInputValue(email, {credential.email!r});
  password.focus();
  setInputValue(password, {credential.password!r});
  password.dispatchEvent(new KeyboardEvent("keydown", {{ key: "Tab", code: "Tab", bubbles: true }}));
  password.dispatchEvent(new KeyboardEvent("keyup", {{ key: "Tab", code: "Tab", bubbles: true }}));

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
      || (el.innerText || "").trim().includes({K_EMAIL_LOGIN_BUTTON!r})
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
) -> dict:
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
        # Clear through native setter before typing so previous value does not remain.
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
    leads_url: str,
    credential: LoginCredential | None,
    manual_login_fallback: bool,
    log: Callable[[str], None],
) -> None:
    expected_host = _host_from_url(leads_url) or _host_from_url(login_url)

    def soft_logged_in() -> bool:
        return bool(
            eval_js(
                session,
                """
(() => {
  const href = location.href || "";
  const bodyTextLen = ((document.body && document.body.innerText) || "").trim().length;
  return href.includes("/leads") && bodyTextLen > 0;
})()
""",
            )
        )

    log("navigate to login page")
    session.go(login_url)

    if is_recatch_logged_in(current_url(session), expected_host):
        log("already logged in")
    else:
        wait_until(
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
            ),
            timeout_sec=10.0,
            interval_sec=0.25,
        )

        if credential is not None:
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
                if not logged_in and soft_logged_in():
                    log("credential login fallback: leads route detected")
                    logged_in = True
                if not logged_in:
                    # Some successful logins land on /leads a beat later than the
                    # strict host/path check above. Give the redirect a second chance
                    # before treating it as a hard failure.
                    logged_in = wait_until(
                        lambda: is_recatch_logged_in(current_url(session), expected_host)
                        or soft_logged_in(),
                        timeout_sec=12.0,
                        interval_sec=0.3,
                    )
                    if logged_in:
                        log("credential login fallback: delayed leads route detected")
                if not logged_in and not manual_login_fallback:
                    detail = eval_js(
                        session,
                        """
(() => {
  const text = (document.body?.innerText || "")
    .split("\\n")
    .map((x) => x.trim())
    .filter(Boolean)
    .slice(0, 40);
  return { topText: text };
})()
""",
                        )
                    raise RuntimeError(f"credential login timeout: {detail}")

        if not wait_until(
            lambda: is_recatch_logged_in(current_url(session), expected_host) or soft_logged_in(),
            timeout_sec=8.0,
            interval_sec=0.3,
        ):
            if manual_login_fallback and sys.stdin.isatty():
                while True:
                    url = current_url(session)
                    log(f"current url: {url}")
                    if is_recatch_logged_in(url, expected_host) or soft_logged_in():
                        break
                    input("complete login in browser, then press Enter...")
            else:
                raise RuntimeError(
                    "not logged in after credential login, and manual fallback is unavailable."
                )

    if "/leads" not in current_url(session):
        log("navigate to leads page")
        session.go(leads_url)
        time.sleep(1.0)

    ready = wait_until(
        lambda: is_leads_page_ready(session),
        timeout_sec=20.0,
        interval_sec=0.3,
    )
    if not ready:
        soft_ready = bool(
            eval_js(
                session,
                """
(() => {
  const href = location.href || "";
  const bodyTextLen = ((document.body && document.body.innerText) || "").trim().length;
  return href.includes("/leads") && bodyTextLen > 0;
})()
""",
            )
        )
        if soft_ready:
            log("leads page ready fallback: route/text detected")
            ready = True
    log(f"leads page ready: {ready}")
    if not ready:
        raise RuntimeError("leads page is not ready")

    log(f"final url after login: {current_url(session)}")
