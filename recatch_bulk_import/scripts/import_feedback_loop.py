#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Sequence


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Wait for a delete job to finish, then run recatch-bulk-import with "
            "state-based restart on interruption or stall."
        )
    )
    parser.add_argument("--delete-pattern", required=True)
    parser.add_argument("--import-bin", default=".venv/bin/recatch-bulk-import")
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--state-file", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--poll-secs", type=float, default=30.0)
    parser.add_argument("--stall-timeout-secs", type=float, default=900.0)
    parser.add_argument("--restart-delay-secs", type=float, default=10.0)
    parser.add_argument("--log-file", required=True)
    return parser.parse_args(argv)


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(log_path: Path, message: str) -> None:
    line = f"[{now()}] {message}"
    print(line, flush=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def delete_is_running(pattern: str) -> bool:
    result = subprocess.run(
        ["pgrep", "-f", pattern],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def load_completed_parts(state_path: Path) -> set[int]:
    if not state_path.exists():
        return set()
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    raw_parts = payload.get("completed_parts", [])
    return {int(part) for part in raw_parts}


def next_pending_part(completed_parts: set[int], start: int, end: int) -> int | None:
    for part in range(start, end + 1):
        if part not in completed_parts:
            return part
    return None


def terminate_process(proc: subprocess.Popen[str], log_path: Path) -> None:
    if proc.poll() is not None:
        return
    log(log_path, f"terminating stuck import pid={proc.pid}")
    proc.terminate()
    try:
        proc.wait(timeout=15)
        return
    except subprocess.TimeoutExpired:
        pass
    log(log_path, f"killing stuck import pid={proc.pid}")
    proc.kill()
    proc.wait(timeout=15)


def build_import_command(
    import_bin: str,
    env_file: str,
    state_file: str,
    next_start: int,
    end: int,
) -> list[str]:
    return [
        import_bin,
        "--env-file",
        env_file,
        "--state-file",
        state_file,
        "--start",
        str(next_start),
        "--end",
        str(end),
        "--skip-completed",
    ]


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    log_path = Path(args.log_file).resolve()
    state_path = Path(args.state_file).resolve()
    import_bin = str(Path(args.import_bin).resolve())
    env_file = str(Path(args.env_file).resolve())
    import_root = str(Path(env_file).resolve().parent)

    active_proc: subprocess.Popen[str] | None = None

    def handle_signal(signum: int, _frame) -> None:
        nonlocal active_proc
        log(log_path, f"received signal={signum}, shutting down supervisor")
        if active_proc is not None:
            terminate_process(active_proc, log_path)
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    log(
        log_path,
        (
            f"supervisor started delete_pattern={args.delete_pattern!r} "
            f"start={args.start} end={args.end} state_file={state_path}"
        ),
    )

    while delete_is_running(args.delete_pattern):
        log(log_path, "delete job still running; waiting before import start")
        time.sleep(args.poll_secs)

    while True:
        completed_parts = load_completed_parts(state_path)
        next_start = next_pending_part(completed_parts, args.start, args.end)
        if next_start is None:
            log(log_path, f"all requested parts completed count={len(completed_parts)}")
            return 0

        cmd = build_import_command(import_bin, env_file, str(state_path), next_start, args.end)
        log(log_path, f"starting import from part={next_start} command={' '.join(cmd)}")
        with log_path.open("a", encoding="utf-8") as import_log:
            active_proc = subprocess.Popen(
                cmd,
                cwd=import_root,
                stdout=import_log,
                stderr=subprocess.STDOUT,
                text=True,
            )

            last_progress_at = time.time()
            last_completed_parts = completed_parts

            while True:
                current_completed_parts = load_completed_parts(state_path)
                if current_completed_parts != last_completed_parts:
                    added = sorted(current_completed_parts - last_completed_parts)
                    last_progress_at = time.time()
                    last_completed_parts = current_completed_parts
                    if added:
                        preview = ",".join(str(part) for part in added[:10])
                        suffix = "..." if len(added) > 10 else ""
                        log(
                            log_path,
                            (
                                f"progress completed_count={len(current_completed_parts)} "
                                f"last_added={preview}{suffix}"
                            ),
                        )

                if active_proc.poll() is not None:
                    exit_code = active_proc.returncode
                    log(log_path, f"import process exited exit_code={exit_code}")
                    break

                if time.time() - last_progress_at >= args.stall_timeout_secs:
                    log(
                        log_path,
                        (
                            f"no state progress for {args.stall_timeout_secs:.0f}s; "
                            "restarting import"
                        ),
                    )
                    terminate_process(active_proc, log_path)
                    break

                time.sleep(args.poll_secs)

        active_proc = None
        completed_parts = load_completed_parts(state_path)
        next_start = next_pending_part(completed_parts, args.start, args.end)
        if next_start is None:
            log(log_path, f"all requested parts completed count={len(completed_parts)}")
            return 0

        log(
            log_path,
            (
                f"import incomplete; next pending part={next_start}. "
                f"sleeping {args.restart_delay_secs:.0f}s before retry"
            ),
        )
        time.sleep(args.restart_delay_secs)


if __name__ == "__main__":
    raise SystemExit(main())
