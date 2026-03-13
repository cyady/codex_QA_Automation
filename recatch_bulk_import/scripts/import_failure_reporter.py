#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence


TS_RE = re.compile(r"^\[(?P<ts>[^\]]+)\]\s(?P<msg>.*)$")
START_RE = re.compile(r"starting import from part=(?P<part>\d+)")
FAILED_RE = re.compile(r"bulk import failed:\s*(?P<reason>.*)$")
DONE_RE = re.compile(r"\[part\s+\d+/\d+\]\s+done:.*\(part\s+(?P<part>\d+)\)")
EXIT_RE = re.compile(r"import process exited exit_code=(?P<code>-?\d+)")
NEXT_RE = re.compile(r"next pending part=(?P<part>\d+)")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch import feedback logs and emit a rolling failure report."
    )
    parser.add_argument("--log-file", required=True)
    parser.add_argument("--state-file", required=False, default="")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--poll-secs", type=float, default=30.0)
    return parser.parse_args(argv)


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_ts_line(line: str) -> tuple[str | None, str]:
    match = TS_RE.match(line.rstrip())
    if not match:
        return None, line.rstrip()
    return match.group("ts"), match.group("msg")


def load_completed_parts(state_path: Path | None) -> list[int]:
    if state_path is None or not state_path.exists():
        return []
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return [int(part) for part in payload.get("completed_parts", [])]


def parse_incidents(log_text: str) -> dict[str, Any]:
    incidents: list[dict[str, Any]] = []
    current_part_start: int | None = None
    last_completed_part: int | None = None
    current_incident: dict[str, Any] | None = None

    for raw_line in log_text.splitlines():
        ts, msg = parse_ts_line(raw_line)
        if not msg:
            continue

        start_match = START_RE.search(msg)
        if start_match:
            current_part_start = int(start_match.group("part"))

        done_match = DONE_RE.search(msg)
        if done_match:
            last_completed_part = int(done_match.group("part"))

        failed_match = FAILED_RE.search(msg)
        if failed_match:
            if current_incident:
                incidents.append(current_incident)
            current_incident = {
                "failed_at": ts,
                "reason": failed_match.group("reason"),
                "started_from_part": current_part_start,
                "last_completed_part": last_completed_part,
                "screenshot": None,
                "current_url": None,
                "page_excerpt": None,
                "browser_closed": False,
                "exit_code": None,
                "next_pending_part": None,
            }
            continue

        if current_incident is None:
            continue

        if msg.startswith("error screenshot:"):
            current_incident["screenshot"] = msg.split(":", 1)[1].strip()
        elif msg.startswith("current url:"):
            current_incident["current_url"] = msg.split(":", 1)[1].strip()
        elif msg.startswith("page excerpt:"):
            excerpt_text = msg.split(":", 1)[1].strip()
            try:
                current_incident["page_excerpt"] = ast.literal_eval(excerpt_text)
            except (SyntaxError, ValueError):
                current_incident["page_excerpt"] = excerpt_text
        elif msg == "browser closed":
            current_incident["browser_closed"] = True
        else:
            exit_match = EXIT_RE.search(msg)
            if exit_match:
                current_incident["exit_code"] = int(exit_match.group("code"))
            next_match = NEXT_RE.search(msg)
            if next_match:
                current_incident["next_pending_part"] = int(next_match.group("part"))
                incidents.append(current_incident)
                current_incident = None

    if current_incident:
        incidents.append(current_incident)

    return {
        "generated_at": now(),
        "incident_count": len(incidents),
        "incidents": incidents,
    }


def write_report_json(report: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report_md(report: dict[str, Any], output_path: Path, completed_parts: list[int]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Import Failure Report")
    lines.append("")
    lines.append(f"- Generated: `{report['generated_at']}`")
    lines.append(f"- Incident count: `{report['incident_count']}`")
    if completed_parts:
        lines.append(f"- Completed parts: `{completed_parts[0]}`..`{completed_parts[-1]}` (`{len(completed_parts)}` parts)")
    else:
        lines.append("- Completed parts: none")
    lines.append("")

    if not report["incidents"]:
        lines.append("No incidents recorded.")
    else:
        for idx, incident in enumerate(report["incidents"], start=1):
            lines.append(f"## Incident {idx}")
            lines.append(f"- Failed at: `{incident.get('failed_at')}`")
            lines.append(f"- Reason: `{incident.get('reason')}`")
            if incident.get("started_from_part") is not None:
                lines.append(f"- Started from part: `{incident['started_from_part']}`")
            if incident.get("last_completed_part") is not None:
                lines.append(f"- Last completed part: `{incident['last_completed_part']}`")
            if incident.get("next_pending_part") is not None:
                lines.append(f"- Next pending part: `{incident['next_pending_part']}`")
            if incident.get("exit_code") is not None:
                lines.append(f"- Exit code: `{incident['exit_code']}`")
            lines.append(f"- Browser closed: `{incident.get('browser_closed', False)}`")
            if incident.get("current_url"):
                lines.append(f"- URL: `{incident['current_url']}`")
            if incident.get("screenshot"):
                lines.append(f"- Screenshot: `{incident['screenshot']}`")
            excerpt = incident.get("page_excerpt")
            if excerpt:
                if isinstance(excerpt, list):
                    excerpt_text = " | ".join(str(item) for item in excerpt[:10])
                else:
                    excerpt_text = str(excerpt)
                lines.append(f"- Excerpt: `{excerpt_text}`")
            lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    log_path = Path(args.log_file).resolve()
    state_path = Path(args.state_file).resolve() if args.state_file else None
    output_json = Path(args.output_json).resolve()
    output_md = Path(args.output_md).resolve()
    running = True

    def handle_signal(signum: int, _frame) -> None:
        nonlocal running
        running = False
        print(f"[{now()}] reporter stopping signal={signum}", flush=True)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while running:
        text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
        report = parse_incidents(text)
        completed_parts = load_completed_parts(state_path)
        write_report_json(report, output_json)
        write_report_md(report, output_md, completed_parts)
        time.sleep(args.poll_secs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
