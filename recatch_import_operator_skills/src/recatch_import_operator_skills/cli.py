from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Callable, Sequence
from urllib.parse import quote, urlencode, urlparse

import vibium

from .auth import LoginCredential, ensure_recatch_login, parse_credential_file
from .browser import build_default_url, build_login_url, current_url, normalize_base_url, visible_page_excerpt
from .company_merge import is_company_page_ready, merge_company_name
from .deal_fields import create_fields, is_data_fields_page_ready, load_field_specs
from .deal_import_inspect import inspect_import_page
from .deal_import_run import import_csv_file, is_import_page_ready
from .deal_layout import is_layout_page_ready, verify_fields_in_layout
from .job_state import describe_job_paths, ensure_job_workspace
from .runtime import (
    PROJECT_ROOT,
    env_flag,
    env_float,
    env_int,
    load_env_file,
    parse_env_file,
    resolve_path,
)
from .source_ops import (
    build_transform_plan,
    ensure_operator_job,
    inspect_source_csv,
    persist_inspection_artifacts,
    persist_split_artifacts,
    persist_transform_plan_artifacts,
    split_source_csv,
)
from .tool_catalog import TOOL_CATALOG


LOG_FILE_PATH: Path | None = None
SCREENSHOT_DIR: Path | None = None


def print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def runtime_root(env_file: Path | None) -> Path:
    if env_file is not None:
        return env_file.parent.resolve()
    return Path.cwd().resolve()


def resolve_runtime_path(env_file: Path | None, raw_path: str) -> Path:
    return resolve_path(runtime_root(env_file), raw_path)


def sanitize_step_name(step_name: str) -> str:
    parts = []
    for ch in step_name:
        if ch.isalnum() or ch in {"-", "_"}:
            parts.append(ch)
        else:
            parts.append("_")
    return "".join(parts).strip("_") or "step"


def init_log_file(log_dir: Path) -> Path:
    global LOG_FILE_PATH
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE_PATH = log_dir / f"operator-{ts}.log"
    return LOG_FILE_PATH


def init_screenshot_dir(screenshot_dir: Path) -> Path:
    global SCREENSHOT_DIR
    SCREENSHOT_DIR = screenshot_dir.resolve()
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    return SCREENSHOT_DIR


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


def save_screenshot(session, step_name: str) -> str | None:
    if SCREENSHOT_DIR is None:
        return None
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = SCREENSHOT_DIR / f"shot-{ts}-{sanitize_step_name(step_name)}.png"
    data = session.screenshot()
    with open(file_path, "wb") as file:
        file.write(data)
    return str(file_path.resolve())


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


def build_companies_url(base_url: str, team_slug: str) -> str:
    if team_slug.strip():
        query = urlencode({"teamSlug": team_slug}, quote_via=quote)
        return build_default_url(base_url, f"/companies?{query}")
    return build_default_url(base_url, "/companies")


def build_login_url_for_destination(base_url: str, destination_url: str) -> str:
    parsed = urlparse(destination_url)
    redirect_path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
    return build_login_url(base_url, redirect_path)


def load_credential(credential_file: str, env_file: Path | None) -> LoginCredential:
    return parse_credential_file(resolve_runtime_path(env_file, credential_file))


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


def build_parser(loaded_env_file: Path | None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Operator workspace for large Re:catch deal imports."
    )
    parser.add_argument("--env-file", default=str(loaded_env_file) if loaded_env_file else None)
    parser.add_argument("--base-url", default=os.getenv("RECATCH_BASE_URL", "https://test.recatch.cc"))
    parser.add_argument("--team-slug", default=os.getenv("RECATCH_TEAM_SLUG", ""))
    parser.add_argument(
        "--credential-file",
        default=os.getenv("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt"),
    )
    parser.add_argument("--record-type-id", type=int, default=env_int("RECATCH_RECORD_TYPE_ID", 0) or None)
    parser.add_argument("--record-type-title", default=os.getenv("RECATCH_RECORD_TYPE_TITLE", ""))
    parser.add_argument("--log-dir", default=os.getenv("RECATCH_LOG_DIR", "logs"))
    parser.add_argument("--screenshot-dir", default=os.getenv("RECATCH_SCREENSHOT_DIR", "screenshots"))
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

    subparsers.add_parser("list-tools", help="list reusable operator tools")
    subparsers.add_parser("doctor", help="check env and credential setup")

    inspect_parser = subparsers.add_parser("inspect-source", help="inspect a source CSV and write summary artifacts")
    add_source_args(inspect_parser)

    plan_parser = subparsers.add_parser(
        "build-transform-plan",
        help="build mapping and candidate field artifacts from a source CSV",
    )
    add_source_args(plan_parser)

    split_parser = subparsers.add_parser("split-source", help="split a source CSV into 1000-row chunks")
    add_source_args(split_parser)
    split_parser.add_argument(
        "--output-dir",
        default=os.getenv("RECATCH_OUTPUT_DIR", ""),
        help="directory for chunk files; defaults to jobs/<job_id>/source/parts",
    )
    split_parser.add_argument(
        "--file-prefix",
        default=os.getenv("RECATCH_FILE_PREFIX", ""),
        help="prefix before the 3-digit part number; blank means auto-detect from source filename",
    )

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
    import_csv_parser.add_argument(
        "--csv-file",
        default=os.getenv("RECATCH_SOURCE_CSV", ""),
        help="csv file to upload; defaults to RECATCH_SOURCE_CSV",
    )
    import_csv_parser.add_argument(
        "--preview-only",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    import_csv_parser.add_argument(
        "--upload-timeout-sec",
        type=float,
        default=env_float("RECATCH_UPLOAD_TIMEOUT_SEC", 60.0),
    )

    batch_parser = subparsers.add_parser(
        "batch-import",
        help="upload every split CSV part from a split manifest with resumable state",
    )
    batch_parser.add_argument(
        "--job-dir",
        default=os.getenv("RECATCH_JOB_DIR", "jobs"),
        help="directory that stores per-job artifacts",
    )
    batch_parser.add_argument(
        "--job-id",
        default=os.getenv("RECATCH_JOB_ID", ""),
        help="job id that owns split-manifest.json and batch state",
    )
    batch_parser.add_argument(
        "--manifest-file",
        default=os.getenv("RECATCH_SPLIT_MANIFEST_FILE", ""),
        help="explicit split-manifest.json path; overrides job-dir/job-id lookup",
    )
    batch_parser.add_argument(
        "--state-file",
        default=os.getenv("RECATCH_BATCH_STATE_FILE", ""),
        help="explicit batch state file path; defaults to jobs/<job_id>/artifacts/batch-import-state.json",
    )
    batch_parser.add_argument(
        "--start-part",
        type=int,
        default=env_int("RECATCH_START_PART", 1),
        help="first part number to upload",
    )
    batch_parser.add_argument(
        "--end-part",
        type=int,
        default=env_int("RECATCH_END_PART", 0),
        help="last part number to upload; 0 means the final part in the manifest",
    )
    batch_parser.add_argument(
        "--skip-completed",
        action=argparse.BooleanOptionalAction,
        default=env_flag("RECATCH_SKIP_COMPLETED", True),
        help="skip part numbers already recorded in the batch state file",
    )
    batch_parser.add_argument(
        "--preview-only",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="run validation/preview for each part without final upload",
    )
    batch_parser.add_argument(
        "--delay-between-parts",
        type=float,
        default=env_float("RECATCH_DELAY_BETWEEN_PARTS", 0.0),
        help="sleep between parts after a successful run",
    )
    batch_parser.add_argument(
        "--upload-timeout-sec",
        type=float,
        default=env_float("RECATCH_UPLOAD_TIMEOUT_SEC", 60.0),
    )

    merge_parser = subparsers.add_parser(
        "merge-company",
        help="search and merge duplicate companies by visible company name",
    )
    merge_parser.add_argument("--company-name", required=True)
    merge_parser.add_argument("--select-count", type=int, default=2)
    merge_parser.add_argument("--survivor-index", type=int, default=1)
    merge_parser.add_argument(
        "--preview-only",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="open the merge modal and stop before the final merge unless explicitly disabled",
    )
    return parser


def add_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--source-csv",
        default=os.getenv("RECATCH_SOURCE_CSV", ""),
        help="source CSV file to analyze or split",
    )
    parser.add_argument(
        "--job-dir",
        default=os.getenv("RECATCH_JOB_DIR", "jobs"),
        help="directory that stores per-job artifacts",
    )
    parser.add_argument(
        "--job-id",
        default=os.getenv("RECATCH_JOB_ID", ""),
        help="optional stable job id; blank means auto-generate from the file name",
    )
    parser.add_argument(
        "--rows-per-part",
        type=int,
        default=env_int("RECATCH_MAX_ROWS_PER_IMPORT", 1000),
        help="max rows per import chunk; Re:catch bulk import max is 1000",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument("--env-file")
    bootstrap_args, _ = bootstrap.parse_known_args(argv)
    loaded_env_file = load_env_file(bootstrap_args.env_file)

    parser = build_parser(loaded_env_file)
    args = parser.parse_args(argv)
    args.loaded_env_file = loaded_env_file

    if args.command in {"inspect-source", "build-transform-plan", "split-source"}:
        if not args.source_csv:
            parser.error("--source-csv or RECATCH_SOURCE_CSV is required")
        if args.rows_per_part < 1:
            parser.error("--rows-per-part must be >= 1")

    if args.command in {"create-fields", "verify-layout", "inspect-import", "import-csv", "batch-import"}:
        if args.record_type_id is None:
            parser.error("--record-type-id or RECATCH_RECORD_TYPE_ID is required")

    if args.command in {"inspect-import", "import-csv", "batch-import"} and not args.record_type_title:
        parser.error("--record-type-title or RECATCH_RECORD_TYPE_TITLE is required")

    if args.command == "import-csv" and not args.csv_file:
        parser.error("--csv-file or RECATCH_SOURCE_CSV is required")
    if args.command == "batch-import":
        if args.start_part < 1:
            parser.error("--start-part must be >= 1")
        if args.end_part < 0:
            parser.error("--end-part must be >= 0")
        if args.delay_between_parts < 0:
            parser.error("--delay-between-parts must be >= 0")
        if not args.manifest_file and not args.job_id:
            parser.error("--job-id or --manifest-file is required for batch-import")

    return args


def run_doctor(args: argparse.Namespace) -> int:
    env_file = args.loaded_env_file
    payload: dict[str, object] = {
        "ok": True,
        "projectRoot": str(PROJECT_ROOT),
        "envFile": str(env_file) if env_file else None,
        "runtimeRoot": str(runtime_root(env_file)),
        "requiredEnvKeys": [
            "RECATCH_BASE_URL",
            "RECATCH_RECORD_TYPE_ID",
            "RECATCH_RECORD_TYPE_TITLE",
            "RECATCH_CREDENTIAL_FILE",
        ],
    }

    env_values = parse_env_file(env_file) if env_file and env_file.exists() else {}
    missing_keys = [
        key
        for key in payload["requiredEnvKeys"]  # type: ignore[index]
        if not env_values.get(key, "").strip()
    ]
    credential_raw = env_values.get("RECATCH_CREDENTIAL_FILE", "credentials/recatch_login.txt")
    credential_path = resolve_runtime_path(env_file, credential_raw)

    payload["envValues"] = {
        "RECATCH_BASE_URL": env_values.get("RECATCH_BASE_URL", ""),
        "RECATCH_RECORD_TYPE_ID": env_values.get("RECATCH_RECORD_TYPE_ID", ""),
        "RECATCH_RECORD_TYPE_TITLE": env_values.get("RECATCH_RECORD_TYPE_TITLE", ""),
        "RECATCH_CREDENTIAL_FILE": credential_raw,
    }
    payload["missingEnvKeys"] = missing_keys
    payload["credentialFile"] = str(credential_path)
    payload["credentialFileExists"] = credential_path.exists()

    if credential_path.exists():
        try:
            credential = parse_credential_file(credential_path)
            payload["credentialSummary"] = {
                "email": credential.email,
                "passwordConfigured": bool(credential.password),
            }
        except Exception as exc:
            payload["ok"] = False
            payload["credentialError"] = str(exc)
    else:
        payload["ok"] = False

    if missing_keys:
        payload["ok"] = False

    print_json(payload)
    return 0 if payload["ok"] else 1


def run_inspect_source(args: argparse.Namespace) -> int:
    source_csv_path = resolve_runtime_path(args.loaded_env_file, args.source_csv)
    job_dir = resolve_runtime_path(args.loaded_env_file, args.job_dir)
    paths = ensure_operator_job(job_dir, source_csv_path, args.job_id or None)
    payload = inspect_source_csv(
        source_csv_path,
        sample_rows=3,
        rows_per_part=args.rows_per_part,
    )
    payload["job"] = persist_inspection_artifacts(paths, payload)
    payload["jobPaths"] = {
        "root": str(paths.root),
        "artifacts": str(paths.artifacts_dir),
        "state": str(paths.state_file),
    }
    print_json(payload)
    return 0


def run_build_transform_plan(args: argparse.Namespace) -> int:
    source_csv_path = resolve_runtime_path(args.loaded_env_file, args.source_csv)
    job_dir = resolve_runtime_path(args.loaded_env_file, args.job_dir)
    paths = ensure_operator_job(job_dir, source_csv_path, args.job_id or None)
    payload = build_transform_plan(
        source_csv_path,
        rows_per_part=args.rows_per_part,
    )
    payload["job"] = persist_transform_plan_artifacts(paths, payload)
    payload["jobPaths"] = {
        "root": str(paths.root),
        "artifacts": str(paths.artifacts_dir),
        "state": str(paths.state_file),
    }
    print_json(payload)
    return 0


def run_split_source(args: argparse.Namespace) -> int:
    source_csv_path = resolve_runtime_path(args.loaded_env_file, args.source_csv)
    job_dir = resolve_runtime_path(args.loaded_env_file, args.job_dir)
    paths = ensure_operator_job(job_dir, source_csv_path, args.job_id or None)

    output_dir = (
        resolve_runtime_path(args.loaded_env_file, args.output_dir)
        if args.output_dir
        else (paths.source_dir / "parts").resolve()
    )
    payload = split_source_csv(
        source_csv_path,
        output_dir,
        rows_per_part=args.rows_per_part,
        file_prefix=args.file_prefix or None,
    )
    payload["job"] = persist_split_artifacts(paths, payload)
    payload["jobPaths"] = {
        "root": str(paths.root),
        "source": str(paths.source_dir),
        "artifacts": str(paths.artifacts_dir),
        "state": str(paths.state_file),
    }
    print_json(payload)
    return 0


def derive_job_paths_from_manifest(args: argparse.Namespace, manifest_path: Path):
    if args.job_id:
        job_dir = resolve_runtime_path(args.loaded_env_file, args.job_dir)
        return ensure_job_workspace(job_dir, args.job_id)

    if manifest_path.parent.name == "artifacts" and manifest_path.parents[1].exists():
        job_root = manifest_path.parents[1]
        job_dir = job_root.parent
        return ensure_job_workspace(job_dir, job_root.name)

    job_dir = resolve_runtime_path(args.loaded_env_file, args.job_dir)
    derived_job_id = f"batch-{manifest_path.stem}"
    return ensure_job_workspace(job_dir, derived_job_id)


def resolve_batch_manifest_path(args: argparse.Namespace):
    if args.manifest_file:
        manifest_path = resolve_runtime_path(args.loaded_env_file, args.manifest_file)
        job_paths = derive_job_paths_from_manifest(args, manifest_path)
        return manifest_path, job_paths

    job_dir = resolve_runtime_path(args.loaded_env_file, args.job_dir)
    job_paths = ensure_job_workspace(job_dir, args.job_id)
    manifest_path = job_paths.artifacts_dir / "split-manifest.json"
    return manifest_path.resolve(), job_paths


def load_split_manifest(manifest_path: Path) -> dict[str, object]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("parts"), list):
        raise ValueError(f"invalid split manifest: {manifest_path}")
    return payload


def resolve_batch_state_path(args: argparse.Namespace, job_paths) -> Path:
    if args.state_file:
        return resolve_runtime_path(args.loaded_env_file, args.state_file)
    return (job_paths.artifacts_dir / "batch-import-state.json").resolve()


def load_completed_parts(state_path: Path) -> set[int]:
    if not state_path.exists():
        return set()
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    raw_parts = payload.get("completedParts", [])
    if not isinstance(raw_parts, list):
        return set()
    completed = set()
    for item in raw_parts:
        try:
            completed.add(int(item))
        except (TypeError, ValueError):
            continue
    return completed


def write_batch_state(
    *,
    state_path: Path,
    job_paths,
    manifest_path: Path,
    import_url: str,
    preview_only: bool,
    selected_parts: Sequence[int],
    completed_parts: set[int],
) -> Path:
    payload = {
        "operation": "batch-import",
        "manifestPath": str(manifest_path),
        "importUrl": import_url,
        "previewOnly": preview_only,
        "selectedParts": list(selected_parts),
        "completedParts": sorted(completed_parts),
        "jobPaths": describe_job_paths(job_paths),
        "updatedAt": dt.datetime.now().isoformat(timespec="seconds"),
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return state_path


def select_manifest_parts(manifest_payload: dict[str, object], start_part: int, end_part: int) -> list[tuple[int, Path]]:
    raw_parts = manifest_payload.get("parts")
    if not isinstance(raw_parts, list) or not raw_parts:
        raise ValueError("split manifest has no parts")

    parts: list[tuple[int, Path]] = []
    for item in raw_parts:
        if not isinstance(item, dict):
            continue
        try:
            part_number = int(item["partNumber"])
            file_path = Path(str(item["file"])).resolve()
        except (KeyError, TypeError, ValueError):
            continue
        parts.append((part_number, file_path))

    if not parts:
        raise ValueError("split manifest has no valid part entries")

    parts.sort(key=lambda item: item[0])
    last_part = parts[-1][0]
    actual_end = last_part if end_part == 0 else end_part
    selected = [item for item in parts if start_part <= item[0] <= actual_end]
    if not selected:
        raise ValueError(f"no parts selected from manifest for range {start_part}..{actual_end}")
    return selected


def run_browser_action(
    args: argparse.Namespace,
    *,
    destination_url: str,
    ready_check: Callable[[object], bool],
    action: Callable[[object], dict[str, object]],
) -> int:
    credential = load_credential(args.credential_file, args.loaded_env_file)
    browser_handle = None
    session = None

    try:
        init_log_file(resolve_runtime_path(args.loaded_env_file, args.log_dir))
        init_screenshot_dir(resolve_runtime_path(args.loaded_env_file, args.screenshot_dir))
        log(f"log file: {LOG_FILE_PATH}")
        log(f"screenshot dir: {SCREENSHOT_DIR}")
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
        screenshot = save_screenshot(session, f"{args.command}-success")
        if screenshot:
            payload["screenshot"] = screenshot
        print_json(payload)
        return 0
    except KeyboardInterrupt:
        log("interrupted by user")
        return 130
    except Exception as exc:
        log(f"operator browser action failed: {exc}")
        if session is not None:
            screenshot = save_screenshot(session, f"{args.command}-error")
            if screenshot:
                log(f"error screenshot: {screenshot}")
            log(f"current url: {current_url(session)}")
            log(f"page excerpt: {visible_page_excerpt(session)}")
        return 1
    finally:
        if session is not None and browser_handle is not None:
            if args.keep_open:
                log("browser kept open")
            else:
                close_vibium_session(browser_handle, session)
                log("browser closed")


def run_batch_import(args: argparse.Namespace, base_url: str) -> int:
    manifest_path, job_paths = resolve_batch_manifest_path(args)
    if not manifest_path.exists():
        raise FileNotFoundError(f"split manifest not found: {manifest_path}")

    manifest_payload = load_split_manifest(manifest_path)
    part_jobs = select_manifest_parts(manifest_payload, args.start_part, args.end_part)
    selected_part_numbers = [part_number for part_number, _ in part_jobs]
    state_path = resolve_batch_state_path(args, job_paths)
    completed_parts = load_completed_parts(state_path) if args.skip_completed else set()
    import_url = build_import_url(base_url, args.record_type_id, args.record_type_title)

    def action(session):
        processed_results: list[dict[str, object]] = []
        skipped_parts: list[int] = []
        total_jobs = len(part_jobs)
        for index, (part_number, csv_path) in enumerate(part_jobs, start=1):
            part_label = f"part {index}/{total_jobs}"
            if args.skip_completed and part_number in completed_parts:
                log(f"[{part_label}] skipped by state file: {csv_path.name}")
                skipped_parts.append(part_number)
                continue

            log(f"[{part_label}] start: {csv_path.name} (part {part_number:03d})")
            result = import_csv_file(
                session=session,
                import_url=import_url,
                csv_path=csv_path,
                log=log,
                preview_only=args.preview_only,
                upload_timeout_sec=args.upload_timeout_sec,
            )
            result["partNumber"] = part_number
            result["csvFile"] = str(csv_path)
            processed_results.append(result)
            completed_parts.add(part_number)
            write_batch_state(
                state_path=state_path,
                job_paths=job_paths,
                manifest_path=manifest_path,
                import_url=import_url,
                preview_only=args.preview_only,
                selected_parts=selected_part_numbers,
                completed_parts=completed_parts,
            )
            log(f"[{part_label}] done: ok={result.get('ok')}, previewOnly={result.get('previewOnly', False)}")

            if args.delay_between_parts > 0 and index != total_jobs:
                time.sleep(args.delay_between_parts)

        return {
            "ok": True,
            "jobId": job_paths.job_id,
            "manifest": str(manifest_path),
            "stateFile": str(state_path),
            "previewOnly": args.preview_only,
            "selectedParts": selected_part_numbers,
            "completedParts": sorted(completed_parts),
            "skippedParts": skipped_parts,
            "processedResults": processed_results,
            "jobPaths": describe_job_paths(job_paths),
        }

    return run_browser_action(
        args,
        destination_url=import_url,
        ready_check=is_import_page_ready,
        action=action,
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    base_url = normalize_base_url(args.base_url)

    if args.command == "list-tools":
        print_json(TOOL_CATALOG)
        return 0
    if args.command == "doctor":
        return run_doctor(args)
    if args.command == "inspect-source":
        return run_inspect_source(args)
    if args.command == "build-transform-plan":
        return run_build_transform_plan(args)
    if args.command == "split-source":
        return run_split_source(args)

    if args.command == "create-fields":
        spec_path = resolve_runtime_path(args.loaded_env_file, args.spec_file)
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
        spec_path = resolve_runtime_path(args.loaded_env_file, args.spec_file)
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
        csv_path = resolve_runtime_path(args.loaded_env_file, args.csv_file)
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

    if args.command == "batch-import":
        return run_batch_import(args, base_url)

    if args.command == "merge-company":
        companies_url = build_companies_url(base_url, args.team_slug)
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
