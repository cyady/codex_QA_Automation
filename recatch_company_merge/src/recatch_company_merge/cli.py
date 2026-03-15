from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Sequence
from urllib.parse import quote, urlencode, urlparse

import vibium

from .auth import LoginCredential, ensure_recatch_login, parse_credential_file
from .browser import build_default_url, build_login_url, normalize_base_url
from .merge import is_company_page_ready, merge_company_name


LOG_FILE_PATH: Path | None = None


def env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "y"}


def init_log_file(log_dir: Path) -> Path:
    global LOG_FILE_PATH
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE_PATH = log_dir / f"company-merge-{ts}.log"
    return LOG_FILE_PATH


def log(message: str) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"
    try:
        print(line)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        safe = line.encode(enc, errors="replace").decode(enc, errors="replace")
        print(safe)
    if LOG_FILE_PATH:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(line + "\n")


def print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def resolve_input_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (Path.cwd() / path).resolve()


def load_credential(credential_file: str) -> LoginCredential:
    return parse_credential_file(resolve_input_path(credential_file))


def build_companies_url(base_url: str, team_slug: str) -> str:
    query = urlencode({"teamSlug": team_slug}, quote_via=quote)
    return build_default_url(base_url, f"/companies?{query}")


def build_login_url_for_destination(base_url: str, destination_url: str) -> str:
    parsed = urlparse(destination_url)
    redirect_path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
    return build_login_url(base_url, redirect_path)


def launch_vibium_session(headless: bool):
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


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Re:catch company duplicate merge automation."
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv(
            "RECATCH_BASE_URL",
            "https://recatch-nextjs-bczu3ipum-business-canvas-front-team.vercel.app",
        ),
    )
    parser.add_argument(
        "--credential-file",
        default=os.getenv("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt"),
    )
    parser.add_argument("--team-slug", default=os.getenv("RECATCH_TEAM_SLUG", "becan"))
    parser.add_argument("--log-dir", default="logs")
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

    subparsers = parser.add_subparsers(dest="command", required=True)

    merge_parser = subparsers.add_parser(
        "merge-name",
        help="search and merge duplicate companies by visible company name",
    )
    merge_parser.add_argument("--company-name", required=True)
    merge_parser.add_argument("--select-count", type=int, default=2)
    merge_parser.add_argument("--survivor-index", type=int, default=1)
    merge_parser.add_argument(
        "--preview-only",
        action=argparse.BooleanOptionalAction,
        default=False,
    )

    return parser.parse_args(argv)


def run_browser_action(
    args: argparse.Namespace,
    *,
    destination_url: str,
    ready_check,
    action,
) -> int:
    credential = load_credential(args.credential_file)
    browser_handle = None
    session = None

    try:
        init_log_file(resolve_input_path(args.log_dir))
        log(f"log file: {LOG_FILE_PATH}")
        log(f"destination url: {destination_url}")
        browser_handle, session = launch_vibium_session(headless=args.headless)
        ensure_recatch_login(
            session=session,
            login_url=build_login_url_for_destination(args.base_url, destination_url),
            destination_url=destination_url,
            credential=credential,
            ready_check=ready_check,
            log=log,
        )
        payload = action(session)
        print_json(payload)
        return 0
    except KeyboardInterrupt:
        log("interrupted by user")
        return 130
    except Exception as exc:
        log(f"company merge automation failed: {exc}")
        return 1
    finally:
        if session is None or browser_handle is None:
            return
        if args.keep_open:
            log("browser kept open")
        else:
            close_vibium_session(browser_handle, session)
            log("browser closed")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    base_url = normalize_base_url(args.base_url)
    companies_url = build_companies_url(base_url, args.team_slug)

    if args.command == "merge-name":
        return run_browser_action(
            args,
            destination_url=companies_url,
            ready_check=is_company_page_ready,
            action=lambda session: merge_company_name(
                session=session,
                company_name=args.company_name,
                select_count=args.select_count,
                survivor_index=args.survivor_index,
                preview_only=args.preview_only,
                log=log,
            ),
        )

    raise RuntimeError(f"unknown command: {args.command}")
