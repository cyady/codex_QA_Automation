from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from .runtime import (
    KNOWN_HEADER_DEFAULTS,
    PROJECT_ROOT,
    ensure_parent,
    is_process_running,
    now_compact,
    now_iso,
    parse_env_file,
    preview_headers,
    read_json_file,
    resolve_path,
    sanitize_token,
    tail_text,
    write_mapping_spec,
)

APP_ROOT = PROJECT_ROOT
UI_LOG_DIR = APP_ROOT / "logs" / "ui"
UI_MAPPING_DIR = APP_ROOT / "mappings" / "ui"
AGENTATION_DIR = UI_LOG_DIR / "agentation"
ACTIVE_STATUS_FILE = UI_LOG_DIR / "active-job-status.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Launch the local Re:catch bulk import UI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8877)
    return parser.parse_args()


def default_env_file() -> Path:
    for candidate in [
        APP_ROOT / ".env.test_dev",
        APP_ROOT / ".env.test",
        APP_ROOT / ".env",
        APP_ROOT / ".env.example",
    ]:
        if candidate.exists():
            return candidate
    return APP_ROOT / ".env.example"


def load_env_defaults(env_file: Path) -> dict[str, Any]:
    values = parse_env_file(env_file) if env_file.exists() else {}
    return {
        "env_file": str(env_file),
        "base_url": values.get("RECATCH_BASE_URL", ""),
        "source_csv": values.get("RECATCH_SOURCE_CSV", ""),
        "csv_dir": values.get("RECATCH_CSV_DIR", "data/csv_split"),
        "file_prefix": values.get("RECATCH_FILE_PREFIX", ""),
        "start": int(values.get("RECATCH_START", "1") or "1"),
        "end": int(values.get("RECATCH_END", "0") or "0"),
        "split_size": int(values.get("RECATCH_SPLIT_SIZE", "1000") or "1000"),
        "headless": values.get("RECATCH_HEADLESS", "false").lower() in {"1", "true", "yes", "on"},
        "manual_login_fallback": values.get("RECATCH_MANUAL_LOGIN_FALLBACK", "false").lower() in {"1", "true", "yes", "on"},
        "configured_state_file": values.get("RECATCH_STATE_FILE", ""),
        "configured_log_dir": values.get("RECATCH_LOG_DIR", "logs"),
        "configured_screenshot_dir": values.get("RECATCH_SCREENSHOT_DIR", "screenshots"),
    }


def runtime_root_from_env(env_file: Path) -> Path:
    return env_file.resolve().parent


def resolve_runtime_input(env_file: Path, raw_path: str | None) -> Path | None:
    if raw_path is None:
        return None
    normalized = raw_path.strip()
    if not normalized:
        return None
    return resolve_path(runtime_root_from_env(env_file), normalized)


def build_job_paths(
    *,
    env_file: Path,
    source_csv: str,
    file_prefix: str,
    start: int,
    end: int,
) -> dict[str, Path]:
    env_token = sanitize_token(env_file.stem)
    source_token = sanitize_token(Path(source_csv).stem) if source_csv.strip() else sanitize_token(file_prefix.rstrip("_"))
    job_token = f"{env_token}-{source_token}-{start}-{end}"
    timestamp = now_compact()
    return {
        "status_file": ACTIVE_STATUS_FILE,
        "state_file": UI_LOG_DIR / f"{job_token}.state.json",
        "log_file": UI_LOG_DIR / f"{timestamp}-{job_token}.log",
        "mapping_file": UI_MAPPING_DIR / f"{job_token}.mapping.json",
    }


def active_status_payload() -> dict[str, Any]:
    payload = read_json_file(ACTIVE_STATUS_FILE)
    if not payload:
        return {
            "status": "idle",
            "phase": "idle",
            "runner_alive": False,
            "progress": {
                "completed_count": 0,
                "total_parts": 0,
                "percent": 0.0,
                "last_completed_part": None,
                "next_pending_part": None,
                "recommended_restart_start": None,
                "completed_parts": [],
            },
            "log_tail": "",
        }

    runner_pid = payload.get("runner_pid")
    payload["runner_alive"] = is_process_running(runner_pid)
    log_file = payload.get("log_file")
    if log_file:
        payload["log_tail"] = tail_text(Path(log_file), 120)
    return payload


def write_agentation_record(prefix: str, payload: dict[str, Any]) -> Path:
    AGENTATION_DIR.mkdir(parents=True, exist_ok=True)
    output_path = AGENTATION_DIR / f"{now_compact()}-{prefix}.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    latest_path = AGENTATION_DIR / f"latest-{prefix}.json"
    latest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def validate_mapping_rows(headers: list[str], raw_rows: list[dict[str, Any]]) -> tuple[list[dict[str, str]], list[str]]:
    row_by_header = {
        str(item.get("csv_header", "")).strip(): item
        for item in raw_rows
        if str(item.get("csv_header", "")).strip()
    }
    normalized_rows: list[dict[str, str]] = []
    errors: list[str] = []

    for header in headers:
        item = row_by_header.get(header, {})
        skip = bool(item.get("skip"))
        query = str(item.get("query", "")).strip()
        option_text = str(item.get("option_text", "")).strip()
        if skip:
            continue
        if not query or not option_text:
            errors.append(f"필드 매핑 누락: {header}")
            continue
        normalized_rows.append(
            {
                "csv_header": header,
                "query": query,
                "option_text": option_text,
            }
        )

    if not normalized_rows and not errors:
        errors.append("최소 1개 이상의 필드 매핑이 필요합니다.")
    return normalized_rows, errors


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    @app.get("/")
    def index() -> str:
        defaults = load_env_defaults(default_env_file())
        status = active_status_payload()
        return render_template(
            "index.html",
            defaults=defaults,
            known_header_defaults=KNOWN_HEADER_DEFAULTS,
            status=status,
        )

    @app.get("/journey-test")
    def journey_test() -> str:
        return render_template("journey_test.html")

    @app.get("/api/status")
    def api_status():
        return jsonify(active_status_payload())

    @app.post("/api/headers")
    def api_headers():
        payload = request.get_json(force=True)
        env_file = resolve_runtime_input(default_env_file(), payload.get("env_file")) or default_env_file()
        if not env_file.exists():
            return jsonify({"ok": False, "error": f"env file not found: {env_file}"}), 400

        source_csv = resolve_runtime_input(env_file, payload.get("source_csv"))
        csv_dir = resolve_runtime_input(env_file, payload.get("csv_dir"))
        file_prefix = str(payload.get("file_prefix", "")).strip()
        if csv_dir is None:
            return jsonify({"ok": False, "error": "split CSV directory is required"}), 400
        if source_csv is not None and not source_csv.exists():
            return jsonify({"ok": False, "error": f"source CSV not found: {source_csv}"}), 400
        if source_csv is None and not file_prefix:
            return jsonify({"ok": False, "error": "file prefix is required when source CSV is empty"}), 400

        try:
            preview = preview_headers(source_csv=source_csv, csv_dir=csv_dir, file_prefix=file_prefix)
        except Exception as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400

        preview["default_mappings"] = {
            header: {
                "query": KNOWN_HEADER_DEFAULTS.get(header, ("", ""))[0],
                "option_text": KNOWN_HEADER_DEFAULTS.get(header, ("", ""))[1],
            }
            for header in preview["headers"]
        }
        preview["split_output_dir"] = str(csv_dir)
        preview["ok"] = True
        return jsonify(preview)

    @app.post("/api/start")
    def api_start():
        existing = active_status_payload()
        if existing.get("runner_alive"):
            return jsonify({"ok": False, "error": "이미 실행 중인 작업이 있습니다."}), 409

        payload = request.get_json(force=True)
        env_file = resolve_runtime_input(default_env_file(), payload.get("env_file")) or default_env_file()
        if not env_file.exists():
            return jsonify({"ok": False, "error": f"env file not found: {env_file}"}), 400

        try:
            start = int(payload.get("start", 1))
            end = int(payload.get("end", 0))
        except (TypeError, ValueError):
            return jsonify({"ok": False, "error": "start/end must be numbers"}), 400
        if start < 1:
            return jsonify({"ok": False, "error": "start must be >= 1"}), 400
        if end != 0 and end < start:
            return jsonify({"ok": False, "error": "end must be 0 or >= start"}), 400

        source_csv_raw = str(payload.get("source_csv", "")).strip()
        csv_dir_raw = str(payload.get("csv_dir", "")).strip()
        file_prefix = str(payload.get("file_prefix", "")).strip()
        source_csv = resolve_runtime_input(env_file, source_csv_raw)
        csv_dir = resolve_runtime_input(env_file, csv_dir_raw)
        if csv_dir is None:
            return jsonify({"ok": False, "error": "split CSV directory is required"}), 400
        if source_csv is not None and not source_csv.exists():
            return jsonify({"ok": False, "error": f"source CSV not found: {source_csv}"}), 400
        if source_csv is None and not file_prefix:
            return jsonify({"ok": False, "error": "file prefix is required when source CSV is empty"}), 400

        try:
            preview = preview_headers(source_csv=source_csv, csv_dir=csv_dir, file_prefix=file_prefix)
        except Exception as exc:
            return jsonify({"ok": False, "error": str(exc)}), 400

        effective_end = end
        if effective_end == 0:
            if preview["mode"] == "split_files":
                effective_end = int(preview["last_part"])
            else:
                return jsonify(
                    {
                        "ok": False,
                        "error": "원본 CSV 모드에서는 end=0 자동 감지를 지원하지 않습니다. 마지막 파트 번호를 입력하세요.",
                    }
                ), 400
        if effective_end < start:
            return jsonify({"ok": False, "error": "종료 파트는 시작 파트보다 작을 수 없습니다."}), 400
        if preview["mode"] == "split_files":
            first_part = int(preview["first_part"])
            last_part = int(preview["last_part"])
            if start < first_part or start > last_part:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": f"시작 파트는 감지된 범위 {first_part}~{last_part} 안에 있어야 합니다.",
                        }
                    ),
                    400,
                )
            if effective_end > last_part:
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": f"종료 파트는 감지된 마지막 파트 {last_part} 이하여야 합니다.",
                        }
                    ),
                    400,
                )

        raw_rows = payload.get("mapping_rows") or []
        mapping_rows, errors = validate_mapping_rows(preview["headers"], list(raw_rows))
        if errors:
            return jsonify({"ok": False, "error": "\n".join(errors)}), 400

        job_paths = build_job_paths(
            env_file=env_file,
            source_csv=source_csv_raw,
            file_prefix=file_prefix,
            start=start,
            end=effective_end,
        )
        if bool(payload.get("reset_state")) and job_paths["state_file"].exists():
            job_paths["state_file"].unlink()

        write_mapping_spec(job_paths["mapping_file"], mapping_rows)
        ensure_parent(job_paths["log_file"])
        ensure_parent(job_paths["status_file"])

        command = [
            sys.executable,
            "-m",
            "recatch_bulk_import_withui.runner",
            "--env-file",
            str(env_file),
            "--csv-dir",
            csv_dir_raw,
            "--file-prefix",
            file_prefix,
            "--mapping-file",
            str(job_paths["mapping_file"]),
            "--state-file",
            str(job_paths["state_file"]),
            "--status-file",
            str(job_paths["status_file"]),
            "--log-file",
            str(job_paths["log_file"]),
            "--start",
            str(start),
            "--end",
            str(effective_end),
        ]
        if source_csv_raw:
            command.extend(["--source-csv", source_csv_raw])

        subprocess.Popen(
            command,
            cwd=APP_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            text=True,
        )
        time.sleep(0.8)
        status = active_status_payload()
        status["ok"] = True
        status["message"] = "작업을 시작했습니다. 브라우저 탭을 닫아도 runner는 계속 동작합니다."
        return jsonify(status)

    @app.post("/api/stop")
    def api_stop():
        status = active_status_payload()
        runner_pid = status.get("runner_pid")
        if not runner_pid or not is_process_running(runner_pid):
            return jsonify({"ok": False, "error": "실행 중인 runner가 없습니다."}), 400
        os.kill(runner_pid, signal.SIGTERM)
        return jsonify({"ok": True, "message": f"runner {runner_pid} 종료 신호를 보냈습니다."})

    @app.post("/api/agentation/session")
    def api_agentation_session():
        payload = request.get_json(force=True) or {}
        payload["received_at"] = now_iso()
        output_path = write_agentation_record("session", payload)
        return jsonify({"ok": True, "path": str(output_path)})

    @app.post("/api/agentation/submit")
    def api_agentation_submit():
        payload = request.get_json(force=True) or {}
        payload["received_at"] = now_iso()
        output_path = write_agentation_record("submit", payload)
        return jsonify({"ok": True, "path": str(output_path)})

    return app


def main() -> int:
    args = parse_args()
    UI_LOG_DIR.mkdir(parents=True, exist_ok=True)
    UI_MAPPING_DIR.mkdir(parents=True, exist_ok=True)
    app = create_app()
    print(f"Re:catch Bulk Import UI running at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
