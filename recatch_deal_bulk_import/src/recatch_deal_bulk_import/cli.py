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
from .fields import create_fields, is_data_fields_page_ready, load_field_specs
from .import_inspect import inspect_import_page
from .import_run import import_csv_file, is_import_page_ready
from .layout import is_layout_page_ready, verify_fields_in_layout


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
    LOG_FILE_PATH = log_dir / f"deal-bulk-import-{ts}.log"
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


def build_data_fields_url(base_url: str) -> str:
    return build_default_url(base_url, "/settings/objects/deal?tab=data-fields")


def build_layout_url(base_url: str, record_type_id: int) -> str:
    return build_default_url(
        base_url,
        f"/settings/objects/deal/record-types/{record_type_id}/layout?origin=setting_page",
    )


def build_import_url(base_url: str, record_type_id: int, record_type_title: str) -> str:
    query = {
        "recordTypeId": str(record_type_id),
        "recordTypeTitle": record_type_title,
    }
    return build_default_url(base_url, f"/deals/import?{urlencode(query, quote_via=quote)}")


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
        description="Re:catch deal field setup and bulk import automation."
    )
    parser.add_argument("--base-url", default=os.getenv("RECATCH_BASE_URL", "https://test.recatch.cc"))
    parser.add_argument(
        "--credential-file",
        default=os.getenv("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt"),
    )
    parser.add_argument("--record-type-id", type=int, required=True)
    parser.add_argument("--record-type-title", default=os.getenv("RECATCH_RECORD_TYPE_TITLE", ""))
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

    create_fields_parser = subparsers.add_parser("create-fields", help="create deal fields from a JSON spec")
    create_fields_parser.add_argument("--spec-file", required=True)
    create_fields_parser.add_argument(
        "--verify-layout",
        action=argparse.BooleanOptionalAction,
        default=True,
    )

    verify_layout_parser = subparsers.add_parser("verify-layout", help="verify fields exist in the record type layout")
    verify_layout_parser.add_argument("--spec-file", required=True)

    subparsers.add_parser("inspect-import", help="inspect the deal import page requirements")

    import_csv_parser = subparsers.add_parser("import-csv", help="upload a deal CSV and auto-map exact headers")
    import_csv_parser.add_argument("--csv-file", required=True)
    import_csv_parser.add_argument(
        "--preview-only",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    import_csv_parser.add_argument("--upload-timeout-sec", type=float, default=60.0)

    args = parser.parse_args(argv)
    if args.command in {"inspect-import", "import-csv"} and not args.record_type_title:
        parser.error("--record-type-title is required for inspect-import and import-csv")
    return args


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
        log(f"deal bulk import automation failed: {exc}")
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

    if args.command == "create-fields":
        spec_path = resolve_input_path(args.spec_file)
        specs = load_field_specs(spec_path)
        data_fields_url = build_data_fields_url(base_url)
        layout_url = build_layout_url(base_url, args.record_type_id)

        def action(session):
            field_results = create_fields(
                session=session,
                data_fields_url=data_fields_url,
                specs=specs,
                log=log,
            )
            layout_results = (
                verify_fields_in_layout(
                    session=session,
                    layout_url=layout_url,
                    field_names=[spec.name for spec in specs],
                )
                if args.verify_layout
                else []
            )
            return {
                "ok": True,
                "dataFieldsUrl": data_fields_url,
                "layoutUrl": layout_url,
                "results": field_results,
                "layoutVerification": layout_results,
            }

        return run_browser_action(
            args,
            destination_url=data_fields_url,
            ready_check=is_data_fields_page_ready,
            action=action,
        )

    if args.command == "verify-layout":
        spec_path = resolve_input_path(args.spec_file)
        specs = load_field_specs(spec_path)
        layout_url = build_layout_url(base_url, args.record_type_id)

        def action(session):
            return {
                "ok": True,
                "layoutUrl": layout_url,
                "results": verify_fields_in_layout(
                    session=session,
                    layout_url=layout_url,
                    field_names=[spec.name for spec in specs],
                ),
            }

        return run_browser_action(
            args,
            destination_url=layout_url,
            ready_check=is_layout_page_ready,
            action=action,
        )

    if args.command == "inspect-import":
        import_url = build_import_url(base_url, args.record_type_id, args.record_type_title)
        return run_browser_action(
            args,
            destination_url=import_url,
            ready_check=is_import_page_ready,
            action=lambda session: inspect_import_page(session, import_url),
        )

    if args.command == "import-csv":
        csv_path = resolve_input_path(args.csv_file)
        import_url = build_import_url(base_url, args.record_type_id, args.record_type_title)

        def action(session):
            return import_csv_file(
                session=session,
                import_url=import_url,
                csv_path=csv_path,
                log=log,
                preview_only=args.preview_only,
                upload_timeout_sec=args.upload_timeout_sec,
            )

        return run_browser_action(
            args,
            destination_url=import_url,
            ready_check=is_import_page_ready,
            action=action,
        )

    raise RuntimeError(f"unknown command: {args.command}")
