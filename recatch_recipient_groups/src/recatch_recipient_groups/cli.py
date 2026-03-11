from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Sequence

import vibium

from .auth import LoginCredential, ensure_recatch_login, parse_credential_file
from .browser import build_login_url, build_segments_path, build_segments_url, normalize_base_url
from .plans import (
    DEFAULT_COUNTS,
    GroupKind,
    build_exact_group_specs,
    load_group_specs,
    normalize_group_kinds,
    plan_to_dict,
    write_plan,
)
from .segments import create_groups_from_specs


LOG_FILE_PATH: Path | None = None


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


def init_log_file(log_dir: Path) -> Path:
    global LOG_FILE_PATH
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE_PATH = log_dir / f"recipient-groups-{ts}.log"
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


def parse_counts(raw: str) -> tuple[int, ...]:
    values = [chunk.strip() for chunk in raw.split(",")]
    counts = tuple(int(value) for value in values if value)
    if not counts:
        raise ValueError("at least one count is required")
    return counts


def parse_kinds(raw: str) -> tuple[GroupKind, ...]:
    return normalize_group_kinds(chunk.strip() for chunk in raw.split(","))


def resolve_optional_input_path(raw_path: str | None) -> Path | None:
    if not raw_path:
        return None
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (Path.cwd() / path).resolve()


def build_specs_from_args(args: argparse.Namespace):
    counts = parse_counts(args.counts)
    kinds = parse_kinds(args.kinds)
    return build_exact_group_specs(
        counts=counts,
        kinds=kinds,
        title_prefix=args.title_prefix,
        number_width=args.number_width,
        name_prefix=args.name_prefix,
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument("--env-file")
    bootstrap_args, _ = bootstrap.parse_known_args(argv)
    loaded_env_file = load_env_file(bootstrap_args.env_file)

    parser = argparse.ArgumentParser(
        description="Re:catch recipient-group automation with reusable login."
    )
    parser.add_argument("--env-file", default=str(loaded_env_file) if loaded_env_file else None)
    parser.add_argument("--base-url", default=os.getenv("RECATCH_BASE_URL", ""))
    parser.add_argument("--team-slug", default=os.getenv("RECATCH_TEAM_SLUG", ""))
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
        "--verification-delay-sec",
        type=float,
        default=env_float("RECATCH_VERIFICATION_DELAY_SEC", 1.5),
    )
    parser.add_argument("--log-dir", default="logs")

    subparsers = parser.add_subparsers(dest="command", required=True)

    exact_help = {
        "counts": ",".join(str(value) for value in DEFAULT_COUNTS),
        "kinds": "static,dynamic",
        "title_prefix": "QA_DYN_",
        "name_prefix": "QA_DYN",
    }

    plan_parser = subparsers.add_parser("plan-exact-groups", help="print or write exact-count group plan")
    plan_parser.add_argument("--counts", default=exact_help["counts"])
    plan_parser.add_argument("--kinds", default=exact_help["kinds"])
    plan_parser.add_argument("--title-prefix", default=exact_help["title_prefix"])
    plan_parser.add_argument("--name-prefix", default=exact_help["name_prefix"])
    plan_parser.add_argument("--number-width", type=int, default=7)
    plan_parser.add_argument("--output")

    create_exact_parser = subparsers.add_parser("create-exact-groups", help="create exact-count groups")
    create_exact_parser.add_argument("--counts", default=exact_help["counts"])
    create_exact_parser.add_argument("--kinds", default=exact_help["kinds"])
    create_exact_parser.add_argument("--title-prefix", default=exact_help["title_prefix"])
    create_exact_parser.add_argument("--name-prefix", default=exact_help["name_prefix"])
    create_exact_parser.add_argument("--number-width", type=int, default=7)

    apply_plan_parser = subparsers.add_parser("apply-plan", help="apply a JSON group plan")
    apply_plan_parser.add_argument("--plan-file", required=True)

    args = parser.parse_args(argv)
    args.loaded_env_file = loaded_env_file

    if args.command in {"create-exact-groups", "apply-plan"} and not args.base_url:
        parser.error("--base-url or RECATCH_BASE_URL is required")

    return args


def print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def load_credential(raw_path: str | None) -> LoginCredential | None:
    credential_path = resolve_optional_input_path(raw_path)
    if credential_path is None:
        return None
    return parse_credential_file(credential_path)


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


def run_browser_plan(
    args: argparse.Namespace,
    specs,
) -> int:
    base_url = normalize_base_url(args.base_url)
    segments_url = build_segments_url(base_url, args.team_slug)
    login_url = build_login_url(base_url, args.team_slug, build_segments_path(args.team_slug))
    credential: LoginCredential | None = None
    browser_handle = None
    session = None

    try:
        init_log_file(Path(args.log_dir).resolve())
        log(f"log file: {LOG_FILE_PATH}")
        log(f"base url: {base_url}")
        log(f"team slug: {args.team_slug}")
        log(f"segments url: {segments_url}")
        log(f"login url: {login_url}")
        log(f"group count: {len(specs)}")

        if args.credential_file:
            try:
                credential = load_credential(args.credential_file)
                log(f"credential file loaded: {args.credential_file}")
            except Exception as exc:
                if not args.manual_login_fallback:
                    raise RuntimeError(f"credential file load failed: {exc}") from exc
                log(f"credential file load failed, manual fallback enabled: {exc}")

        browser_handle, session = launch_vibium_session(headless=args.headless)

        ensure_recatch_login(
            session=session,
            login_url=login_url,
            destination_url=segments_url,
            credential=credential,
            manual_login_fallback=args.manual_login_fallback,
            log=log,
        )

        results = create_groups_from_specs(
            session=session,
            segments_url=segments_url,
            specs=list(specs),
            verification_delay_sec=args.verification_delay_sec,
            log=log,
        )
        print_json({"results": results})
        return 0
    except KeyboardInterrupt:
        log("interrupted by user")
        return 130
    except Exception as exc:
        log(f"recipient-group automation failed: {exc}")
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

    if args.command == "plan-exact-groups":
        specs = build_specs_from_args(args)
        payload = plan_to_dict(specs)
        if args.output:
            output_path = Path(args.output).expanduser()
            if not output_path.is_absolute():
                output_path = (Path.cwd() / output_path).resolve()
            write_plan(output_path, specs)
            log(f"plan file written: {output_path}")
        print_json(payload)
        return 0

    if args.command == "create-exact-groups":
        specs = build_specs_from_args(args)
        return run_browser_plan(args, specs)

    if args.command == "apply-plan":
        plan_path = Path(args.plan_file).expanduser()
        if not plan_path.is_absolute():
            plan_path = (Path.cwd() / plan_path).resolve()
        specs = load_group_specs(plan_path)
        return run_browser_plan(args, specs)

    raise RuntimeError(f"unknown command: {args.command}")
