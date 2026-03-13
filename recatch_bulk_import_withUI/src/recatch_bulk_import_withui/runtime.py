from __future__ import annotations

import csv
import json
import os
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CLEANUP_PORT = 9515
KNOWN_HEADER_DEFAULTS: dict[str, tuple[str, str]] = {
    "lead:deal_name": ("제목", "제목"),
    "contact:name": ("이름", "이름"),
    "contact:email": ("이메일", "이메일"),
    "company:name": ("회사명", "회사명"),
}


def now_display() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_compact() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


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


def load_env_file(env_path: Path, *, override: bool = False) -> dict[str, str]:
    values = parse_env_file(env_path)
    for key, value in values.items():
        if override or key not in os.environ:
            os.environ[key] = value
    return values


def resolve_path(runtime_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (runtime_root / candidate).resolve()


def resolve_optional_path(runtime_root: Path, raw_path: str | None) -> Path | None:
    if raw_path is None:
        return None
    normalized = raw_path.strip()
    if not normalized:
        return None
    return resolve_path(runtime_root, normalized)


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def sanitize_token(raw_value: str) -> str:
    sanitized = []
    for ch in raw_value.strip():
        if ch.isalnum() or ch in {"-", "_"}:
            sanitized.append(ch)
        else:
            sanitized.append("_")
    token = "".join(sanitized).strip("_")
    return token or "job"


def read_csv_headers(csv_path: Path) -> list[str]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        headers = next(reader, None)
    if not headers:
        raise ValueError(f"CSV headers not found: {csv_path}")
    return [str(header).strip() for header in headers]


def discover_existing_parts(csv_dir: Path, file_prefix: str) -> list[tuple[int, Path]]:
    parts: list[tuple[int, Path]] = []
    for csv_path in sorted(csv_dir.glob(f"{file_prefix}*.csv")):
        suffix = csv_path.stem[len(file_prefix) :]
        if not suffix.isdigit():
            continue
        parts.append((int(suffix), csv_path.resolve()))
    return sorted(parts, key=lambda item: item[0])


def preview_headers(
    *,
    source_csv: Path | None,
    csv_dir: Path,
    file_prefix: str,
) -> dict[str, Any]:
    if source_csv is not None:
        headers = read_csv_headers(source_csv)
        return {
            "headers": headers,
            "source": str(source_csv),
            "mode": "source_csv",
            "part_count": None,
            "first_part": None,
            "last_part": None,
        }

    parts = discover_existing_parts(csv_dir, file_prefix)
    if not parts:
        raise FileNotFoundError(
            f"No split CSV files found in {csv_dir} with prefix {file_prefix!r}"
        )
    headers = read_csv_headers(parts[0][1])
    return {
        "headers": headers,
        "source": str(parts[0][1]),
        "mode": "split_files",
        "part_count": len(parts),
        "first_part": parts[0][0],
        "last_part": parts[-1][0],
    }


def load_completed_parts(state_path: Path) -> set[int]:
    if not state_path.exists():
        return set()
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    raw_parts = payload.get("completed_parts", [])
    completed_parts: set[int] = set()
    for part in raw_parts:
        try:
            completed_parts.add(int(part))
        except (TypeError, ValueError):
            continue
    return completed_parts


def next_pending_part(completed_parts: set[int], start: int, end: int) -> int | None:
    for part in range(start, end + 1):
        if part not in completed_parts:
            return part
    return None


def count_completed_in_range(completed_parts: set[int], start: int, end: int) -> int:
    return sum(1 for part in completed_parts if start <= part <= end)


def last_completed_in_range(completed_parts: set[int], start: int, end: int) -> int | None:
    eligible = [part for part in completed_parts if start <= part <= end]
    return max(eligible) if eligible else None


def tail_text(path: Path, line_limit: int = 120) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-line_limit:])


def write_mapping_spec(mapping_path: Path, rows: list[dict[str, str]]) -> Path:
    payload = {
        "columns": [
            {
                "csv_header": row["csv_header"],
                "query": row["query"],
                "option_text": row["option_text"],
            }
            for row in rows
        ]
    }
    ensure_parent(mapping_path)
    mapping_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return mapping_path


def read_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_json_file(path: Path, payload: dict[str, Any]) -> Path:
    ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def is_process_running(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def run_capture(*cmd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(cmd),
        check=False,
        text=True,
        capture_output=True,
    )


def find_listening_pids(port: int) -> set[int]:
    result = run_capture("lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-t")
    pids: set[int] = set()
    for raw_line in result.stdout.splitlines():
        raw_line = raw_line.strip()
        if raw_line.isdigit():
            pids.add(int(raw_line))
    return pids


def find_processes_by_pattern(pattern: str) -> set[int]:
    result = run_capture("pgrep", "-f", pattern)
    pids: set[int] = set()
    for raw_line in result.stdout.splitlines():
        raw_line = raw_line.strip()
        if raw_line.isdigit():
            pids.add(int(raw_line))
    return pids


def describe_pid(pid: int) -> str:
    result = run_capture("ps", "-p", str(pid), "-o", "pid=,ppid=,command=")
    line = result.stdout.strip()
    return line or f"pid={pid}"


def terminate_pid(pid: int, grace_sec: float = 5.0) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.time() + grace_sec
    while time.time() < deadline:
        if not is_process_running(pid):
            return
        time.sleep(0.2)
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        return


def cleanup_runtime_processes(
    *,
    cleanup_port: int,
    log_func,
    protected_pids: set[int] | None = None,
) -> list[str]:
    protected = protected_pids or set()
    target_pids = set()
    target_pids |= find_listening_pids(cleanup_port)
    target_pids |= find_processes_by_pattern(r"vibium serve")
    target_pids |= find_processes_by_pattern(r"chromedriver")
    target_pids = {pid for pid in target_pids if pid not in protected and pid > 1}

    killed: list[str] = []
    for pid in sorted(target_pids):
        description = describe_pid(pid)
        log_func(f"cleanup: terminating {description}")
        terminate_pid(pid)
        killed.append(description)

    if not killed:
        log_func("cleanup: no stale vibium/chromedriver processes found")
    return killed


def classify_failure(log_excerpt: str) -> tuple[bool, str]:
    lowered = log_excerpt.lower()
    recoverable_needles = [
        "failed to listen on port 9515",
        "vibium failed to start",
        "did not return to leads page after",
        "browser closed",
        "import page not ready",
        "leads page is not ready",
        "not logged in after credential login",
        "upload success text not found",
        "validation step failed",
        "mapping page not ready",
        "mapping selects not ready",
    ]
    unrecoverable_needles = [
        "env file not found",
        "--base-url or recatch_base_url is required",
        "no csv files found",
        "missing csv part",
        "end exceeds available parts",
        "mapping file has invalid item",
        "mapping entry is incomplete",
        "mapping value must",
        "credential file load failed",
        "csv headers not found",
        "file not found",
    ]

    for needle in unrecoverable_needles:
        if needle in lowered:
            return False, needle
    for needle in recoverable_needles:
        if needle in lowered:
            return True, needle
    return False, "unknown"
