from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Sequence

from .runtime import (
    DEFAULT_CLEANUP_PORT,
    classify_failure,
    cleanup_runtime_processes,
    count_completed_in_range,
    ensure_parent,
    is_process_running,
    last_completed_in_range,
    load_completed_parts,
    next_pending_part,
    now_display,
    now_iso,
    resolve_path,
    tail_text,
    write_json_file,
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run recatch-bulk-import with auto cleanup and restart support for the local UI."
    )
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--source-csv", default="")
    parser.add_argument("--csv-dir", required=True)
    parser.add_argument("--file-prefix", default="")
    parser.add_argument("--mapping-file", required=True)
    parser.add_argument("--state-file", required=True)
    parser.add_argument("--status-file", required=True)
    parser.add_argument("--log-file", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--restart-delay-secs", type=float, default=15.0)
    parser.add_argument("--poll-secs", type=float, default=3.0)
    parser.add_argument("--stall-timeout-secs", type=float, default=900.0)
    parser.add_argument("--cleanup-port", type=int, default=DEFAULT_CLEANUP_PORT)
    parser.add_argument("--import-bin", default=".venv/bin/recatch-bulk-import")
    return parser.parse_args(argv)


def log(log_path: Path, message: str) -> None:
    line = f"[{now_display()}] {message}"
    print(line, flush=True)
    ensure_parent(log_path)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def progress_payload(state_path: Path, start: int, end: int) -> dict[str, Any]:
    completed_parts = load_completed_parts(state_path)
    completed_count = count_completed_in_range(completed_parts, start, end)
    next_part = next_pending_part(completed_parts, start, end)
    last_part = last_completed_in_range(completed_parts, start, end)
    total_parts = max(end - start + 1, 0)
    percent = round((completed_count / total_parts) * 100, 2) if total_parts else 0.0
    return {
        "completed_parts": sorted(part for part in completed_parts if start <= part <= end),
        "completed_count": completed_count,
        "last_completed_part": last_part,
        "next_pending_part": next_part,
        "recommended_restart_start": next_part,
        "total_parts": total_parts,
        "percent": percent,
    }


def build_import_command(args: argparse.Namespace, runtime_root: Path, next_start: int) -> list[str]:
    import_bin_path = resolve_path(runtime_root, args.import_bin)
    cmd = [
        str(import_bin_path),
        "--env-file",
        str(resolve_path(runtime_root, args.env_file)),
        "--csv-dir",
        str(resolve_path(runtime_root, args.csv_dir)),
        "--mapping-file",
        str(resolve_path(runtime_root, args.mapping_file)),
        "--state-file",
        str(resolve_path(runtime_root, args.state_file)),
        "--start",
        str(next_start),
        "--end",
        str(args.end),
        "--skip-completed",
        "--no-prompt-mapping",
    ]
    if args.file_prefix.strip():
        cmd.extend(["--file-prefix", args.file_prefix.strip()])
    if args.source_csv.strip():
        cmd.extend(["--source-csv", str(resolve_path(runtime_root, args.source_csv))])
    return cmd


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    runtime_root = resolve_path(Path.cwd(), args.env_file).parent
    log_path = resolve_path(runtime_root, args.log_file)
    state_path = resolve_path(runtime_root, args.state_file)
    status_path = resolve_path(runtime_root, args.status_file)
    mapping_path = resolve_path(runtime_root, args.mapping_file)

    active_proc: subprocess.Popen[str] | None = None
    stop_requested = False
    started_at = now_iso()
    attempt = 0
    last_error = ""
    last_error_at = ""

    def write_status(*, status: str, phase: str, note: str = "") -> None:
        payload = {
            "runner_pid": os.getpid(),
            "import_pid": active_proc.pid if active_proc and active_proc.poll() is None else None,
            "status": status,
            "phase": phase,
            "note": note,
            "attempt": attempt,
            "started_at": started_at,
            "updated_at": now_iso(),
            "env_file": str(resolve_path(runtime_root, args.env_file)),
            "source_csv": str(resolve_path(runtime_root, args.source_csv)) if args.source_csv.strip() else "",
            "csv_dir": str(resolve_path(runtime_root, args.csv_dir)),
            "file_prefix": args.file_prefix,
            "mapping_file": str(mapping_path),
            "state_file": str(state_path),
            "log_file": str(log_path),
            "start": args.start,
            "end": args.end,
            "restart_delay_secs": args.restart_delay_secs,
            "stall_timeout_secs": args.stall_timeout_secs,
            "last_error": last_error,
            "last_error_at": last_error_at,
            "log_tail": tail_text(log_path, 80),
            "progress": progress_payload(state_path, args.start, args.end),
        }
        write_json_file(status_path, payload)

    def handle_signal(signum: int, _frame) -> None:
        nonlocal stop_requested, active_proc, last_error, last_error_at
        stop_requested = True
        last_error = f"stopped by signal {signum}"
        last_error_at = now_iso()
        log(log_path, last_error)
        if active_proc is not None and active_proc.poll() is None:
            active_proc.terminate()
            try:
                active_proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                active_proc.kill()
                active_proc.wait(timeout=15)
        cleanup_runtime_processes(
            cleanup_port=args.cleanup_port,
            log_func=lambda message: log(log_path, message),
            protected_pids={os.getpid(), os.getppid()},
        )
        write_status(status="stopped", phase="stopped", note=last_error)
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    log(log_path, f"ui runner started start={args.start} end={args.end} mapping={mapping_path}")
    write_status(status="starting", phase="starting", note="runner booted")

    while True:
        progress = progress_payload(state_path, args.start, args.end)
        next_start = progress["next_pending_part"]
        if next_start is None:
            log(log_path, "all requested parts completed")
            write_status(status="completed", phase="completed", note="all requested parts completed")
            return 0

        attempt += 1
        write_status(status="running", phase="cleanup", note=f"attempt {attempt} cleanup")
        cleanup_runtime_processes(
            cleanup_port=args.cleanup_port,
            log_func=lambda message: log(log_path, message),
            protected_pids={os.getpid(), os.getppid()},
        )
        if stop_requested:
            write_status(status="stopped", phase="stopped", note="stop requested before launch")
            return 130

        cmd = build_import_command(args, runtime_root, next_start)
        last_error = ""
        log(log_path, f"launching import attempt={attempt} next_start={next_start} command={' '.join(cmd)}")
        write_status(status="running", phase="launching", note=f"launching from part {next_start}")

        try:
            with log_path.open("a", encoding="utf-8") as import_log:
                active_proc = subprocess.Popen(
                    cmd,
                    cwd=runtime_root,
                    stdout=import_log,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
        except FileNotFoundError as exc:
            last_error = str(exc)
            last_error_at = now_iso()
            log(log_path, f"failed to launch import command: {exc}")
            write_status(status="failed", phase="failed", note=last_error)
            return 1

        last_progress_count = progress["completed_count"]
        last_progress_at = time.time()
        write_status(status="running", phase="importing", note=f"import running from part {next_start}")

        while active_proc.poll() is None:
            if stop_requested:
                break
            current_progress = progress_payload(state_path, args.start, args.end)
            if current_progress["completed_count"] != last_progress_count:
                last_progress_count = current_progress["completed_count"]
                last_progress_at = time.time()
                log(
                    log_path,
                    (
                        "progress "
                        f"completed={current_progress['completed_count']}/{current_progress['total_parts']} "
                        f"last_completed={current_progress['last_completed_part']}"
                    ),
                )
                write_status(
                    status="running",
                    phase="importing",
                    note=f"completed {current_progress['completed_count']} parts",
                )

            if time.time() - last_progress_at >= args.stall_timeout_secs:
                last_error = f"no progress for {args.stall_timeout_secs:.0f}s"
                last_error_at = now_iso()
                log(log_path, last_error)
                active_proc.terminate()
                try:
                    active_proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    active_proc.kill()
                    active_proc.wait(timeout=15)
                break

            time.sleep(args.poll_secs)

        exit_code = active_proc.returncode if active_proc is not None else 1
        active_proc = None
        current_progress = progress_payload(state_path, args.start, args.end)
        if current_progress["next_pending_part"] is None:
            log(log_path, "all requested parts completed")
            write_status(status="completed", phase="completed", note="all requested parts completed")
            return 0

        log_excerpt = tail_text(log_path, 120)
        if not last_error or exit_code != 0:
            recoverable, failure_key = classify_failure(log_excerpt)
            last_error = failure_key if failure_key != "unknown" else f"import exited with code {exit_code}"
            last_error_at = now_iso()
        else:
            recoverable, _ = classify_failure(log_excerpt)

        log(
            log_path,
            (
                f"attempt {attempt} ended exit_code={exit_code} "
                f"recoverable={recoverable} next_pending={current_progress['next_pending_part']}"
            ),
        )

        if stop_requested:
            write_status(status="stopped", phase="stopped", note="stop requested")
            return 130

        if not recoverable:
            write_status(status="failed", phase="failed", note=last_error)
            return 1

        write_status(
            status="retrying",
            phase="retry_wait",
            note=(
                f"recoverable failure detected. restart recommended: "
                f"{current_progress['next_pending_part']}..{args.end}"
            ),
        )
        log(
            log_path,
            (
                f"sleeping {args.restart_delay_secs:.0f}s before retry. "
                f"recommended restart range={current_progress['next_pending_part']}..{args.end}"
            ),
        )
        time.sleep(args.restart_delay_secs)


if __name__ == "__main__":
    raise SystemExit(main())
