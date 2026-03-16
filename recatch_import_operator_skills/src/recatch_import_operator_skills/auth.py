from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qsl, quote, urlencode, urlparse, urlunparse

from .browser import current_url, eval_js, js_quote, visible_page_excerpt, wait_until


K_EMAIL_LOGIN_BUTTON = "이메일로 로그인"
K_EMAIL_LOGIN_MAX_ATTEMPTS = 3
K_EMAIL_LOGIN_SETTLE_TIMEOUT_SEC = 5.0


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

    email = kv.get("email") or kv.get("id") or kv.get("username") or kv.get("user") or ""
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


def _is_alphakey_host(url: str) -> bool:
    return "alphakey.kr" in _host_from_url(url)


def _build_credential_query_url(destination_url: str, credential: LoginCredential) -> str:
    parsed = urlparse(destination_url)
    query_items = [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True) if key != "credential"]
    credential_payload = json.dumps(
        {
            "email": credential.email,
            "password": credential.password,
            "signInMethod": "password",
            "tenantId": None,
        },
        ensure_ascii=False,
    )
    query_items.append(("credential", credential_payload))
    return urlunparse(parsed._replace(query=urlencode(query_items, doseq=True, quote_via=quote)))


def _supports_credential_query_auth(destination_url: str) -> bool:
    host = _host_from_url(destination_url)
    return "vercel.app" in host


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


def login_with_credentials(
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
  const email = [...document.querySelectorAll("input[name='email'], input#email, input[type='email'], input")]
    .find((el) => isVisible(el) && (
      (el.name || "").toLowerCase().includes("email")
      || (el.id || "").toLowerCase().includes("email")
      || (el.placeholder || "").toLowerCase().includes("email")
      || (el.type || "").toLowerCase() === "email"
    ));
  const password = [...document.querySelectorAll("input[name='password'], input#password, input[type='password'], input")]
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
  if (!email || !password || !submit) {{
    return {{ ok: false, reason: "login_controls_not_found" }};
  }}

  const setInputValue = (el, value) => {{
    const desc = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value");
    if (desc && desc.set) desc.set.call(el, value);
    else el.value = value;
    el.dispatchEvent(new Event("input", {{ bubbles: true }}));
    el.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }};

  setInputValue(email, {js_quote(credential.email)});
  setInputValue(password, {js_quote(credential.password)});
  submit.click();
  return {{ ok: true }};
}})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def find_workspace_login_button(
    session: "vibium.browser_sync.VibeSync",
) -> dict[str, Any]:
    result = eval_js(
        session,
        """
(() => {
  const isVisible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
  };
  const textOf = (el) => (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim();

  const buttons = [...document.querySelectorAll("button")]
    .filter((el) => isVisible(el))
    .map((el) => ({ el, text: textOf(el) }))
    .filter((item) =>
      item.text.endsWith("로그인")
      && !item.text.includes("Google")
      && !item.text.includes("Microsoft")
      && !item.text.includes("이메일")
    );

  const target = buttons[0];
  if (!target) {
    return { ok: false, reason: "workspace_button_not_found" };
  }
  return { ok: true, text: target.text };
})()
""",
    )
    return result if isinstance(result, dict) else {"ok": False, "raw": result}


def ensure_recatch_login(
    session: "vibium.browser_sync.VibeSync",
    login_url: str,
    destination_url: str,
    credential: LoginCredential,
    ready_check: Callable[["vibium.browser_sync.VibeSync"], bool],
    log: Callable[[str], None],
) -> None:
    expected_host = _host_from_url(destination_url) or _host_from_url(login_url)

    if _supports_credential_query_auth(destination_url):
        log("attempt credential query auth")
        session.go(_build_credential_query_url(destination_url, credential))
        credential_ready = wait_until(
            lambda: ready_check(session),
            timeout_sec=25.0,
            interval_sec=0.5,
        )
        if credential_ready:
            if current_url(session) != destination_url:
                session.go(destination_url)
                cleaned = wait_until(
                    lambda: ready_check(session),
                    timeout_sec=10.0,
                    interval_sec=0.3,
                )
                if not cleaned:
                    raise RuntimeError(
                        f"destination page not ready after credential query auth: "
                        f"url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
                    )
            log(f"final url after login: {current_url(session)}")
            return

    log("navigate to login page")
    session.go(login_url)
    current = current_url(session)
    if _is_alphakey_host(current):
        raise RuntimeError(
            f"alphakey redirect blocked on login navigation: url={current}, "
            "automation is configured not to enter Alphakey"
        )

    if not is_recatch_logged_in(current, expected_host):
        login_ready = wait_until(
            lambda: is_login_page_ready(session) or _is_alphakey_host(current_url(session)),
            timeout_sec=10.0,
            interval_sec=0.25,
        )
        if not login_ready:
            raise RuntimeError(
                f"login page not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
            )

        current = current_url(session)
        if _is_alphakey_host(current):
            raise RuntimeError(
                f"alphakey redirect blocked before credential login: url={current}, "
                "automation is configured not to enter Alphakey"
            )

        logged_in = False
        last_login_result: dict[str, Any] | None = None
        workspace_prompt: dict[str, Any] | None = None

        def login_completed() -> bool:
            current = current_url(session)
            if _is_alphakey_host(current):
                raise RuntimeError(
                    f"alphakey redirect blocked after credential login: url={current}, "
                    "automation is configured not to enter Alphakey"
                )
            return is_recatch_logged_in(current, expected_host)

        for attempt in range(1, K_EMAIL_LOGIN_MAX_ATTEMPTS + 1):
            last_login_result = login_with_credentials(session, credential)
            log(
                f"credential login attempt {attempt}/{K_EMAIL_LOGIN_MAX_ATTEMPTS}: "
                f"{last_login_result}"
            )
            if not last_login_result.get("ok"):
                if attempt == K_EMAIL_LOGIN_MAX_ATTEMPTS:
                    raise RuntimeError(f"credential login failed: {last_login_result}")
                continue

            logged_in = wait_until(
                login_completed,
                timeout_sec=K_EMAIL_LOGIN_SETTLE_TIMEOUT_SEC,
                interval_sec=0.5,
            )
            if logged_in:
                break

            workspace_prompt = find_workspace_login_button(session)
            if workspace_prompt.get("ok"):
                log(
                    f"workspace SSO prompt still visible after email login attempt {attempt}: "
                    f"{workspace_prompt}"
                )
            else:
                log(
                    f"email login attempt {attempt} did not redirect yet; "
                    f"url={current_url(session)}"
                )

        if not logged_in:
            current = current_url(session)
            if _is_alphakey_host(current):
                raise RuntimeError(
                    f"alphakey redirect blocked after credential retries: url={current}, "
                    "automation is configured not to enter Alphakey"
                )
            if workspace_prompt is not None and workspace_prompt.get("ok"):
                raise RuntimeError(
                    "workspace SSO prompt detected after email login retries; "
                    f"automation will not click it because it leads to Alphakey: {workspace_prompt}"
                )
            raise RuntimeError(
                "credential login retries exhausted without redirect: "
                f"url={current}, excerpt={visible_page_excerpt(session)}"
            )

    if current_url(session) != destination_url:
        log("navigate to destination page")
        session.go(destination_url)
        current = current_url(session)
        if _is_alphakey_host(current):
            raise RuntimeError(
                f"alphakey redirect blocked on destination navigation: url={current}, "
                "automation is configured not to enter Alphakey"
            )

    ready = wait_until(
        lambda: ready_check(session),
        timeout_sec=20.0,
        interval_sec=0.3,
    )
    if not ready:
        raise RuntimeError(
            f"destination page not ready: url={current_url(session)}, excerpt={visible_page_excerpt(session)}"
        )

    log(f"final url after login: {current_url(session)}")
