#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, UTC
from pathlib import Path
from urllib import error, request


DEFAULT_URL = "https://api.recatch.cc/ai-agent/fields/map"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _post(url: str, token: str, payload: dict, timeout: int) -> str:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url,
        method="POST",
        data=body,
        headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"Bearer {token}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "expires": "0",
            "pragma": "no-cache",
            "Origin": "https://business-canvas.recatch.cc",
            "Referer": "https://business-canvas.recatch.cc/",
            "User-Agent": "Mozilla/5.0",
            "x-locale": "Asia/Seoul",
            "x-recatch-request": "true",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e


def _save_json_or_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        parsed = json.loads(text)
        path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    except json.JSONDecodeError:
        path.write_text(text, encoding="utf-8")


def _run_one(
    i: int,
    memo_dir: Path,
    out_dir: Path,
    url: str,
    token: str,
    timeout: int,
    retries: int,
    sleep_sec: float,
    record_id: int | None,
    skip_existing_non_empty: bool,
) -> tuple[bool, str]:
    memo_path = memo_dir / f"memo_w{i}.txt"
    out_path = out_dir / f"bc{i}_model_output.json"
    if not memo_path.exists():
        return False, f"missing memo: {memo_path}"
    if skip_existing_non_empty and out_path.exists() and out_path.stat().st_size > 0:
        return True, f"skip(existing): {out_path}"

    summary = memo_path.read_text(encoding="utf-8")
    payload = {
        "date": _now_iso(),
        "entity_type": "deal",
        "summary": summary,
    }
    if record_id is not None:
        payload["record_id"] = int(record_id)

    last_err = ""
    for attempt in range(1, retries + 2):
        try:
            text = _post(url=url, token=token, payload=payload, timeout=timeout)
            _save_json_or_text(out_path, text)
            return True, str(out_path)
        except Exception as e:
            last_err = f"attempt={attempt} error={e}"
            if attempt < retries + 1:
                time.sleep(min(2 * attempt, 5))
    return False, f"failed {memo_path.name}: {last_err}"


def main() -> None:
    p = argparse.ArgumentParser(description="Fetch model outputs in bulk for memo_w*.txt files.")
    p.add_argument("--memo-dir", default="data_bc", help="Directory containing memo_w*.txt")
    p.add_argument("--output-dir", default="model_output", help="Directory for bc*_model_output.json")
    p.add_argument("--start", type=int, default=3, help="Start index (inclusive)")
    p.add_argument("--end", type=int, default=547, help="End index (inclusive)")
    p.add_argument("--url", default=DEFAULT_URL, help=f"API URL (default: {DEFAULT_URL})")
    p.add_argument("--token-env", default="RECATCH_FB_TOKEN", help="Bearer token env var name")
    p.add_argument("--token", default=None, help="Bearer token; overrides --token-env")
    p.add_argument("--timeout", type=int, default=90, help="HTTP timeout seconds")
    p.add_argument("--retries", type=int, default=1, help="Retry count per file")
    p.add_argument("--sleep-sec", type=float, default=0.7, help="Sleep seconds between requests")
    p.add_argument("--record-id", type=int, default=566094, help="Deal record_id to include in payload")
    p.add_argument(
        "--skip-existing-non-empty",
        action="store_true",
        help="Skip output files that already exist and are non-empty",
    )
    p.add_argument(
        "--stop-on-fail",
        action="store_true",
        help="Stop immediately when a request fails",
    )
    args = p.parse_args()

    token = (args.token or os.getenv(args.token_env) or "").strip()
    if not token:
        raise SystemExit(f"missing token: set --token or export {args.token_env}")

    memo_dir = Path(args.memo_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ok = 0
    fail = 0
    failures: list[str] = []

    for i in range(args.start, args.end + 1):
        success, msg = _run_one(
            i=i,
            memo_dir=memo_dir,
            out_dir=out_dir,
            url=args.url,
            token=token,
            timeout=args.timeout,
            retries=args.retries,
            sleep_sec=args.sleep_sec,
            record_id=args.record_id,
            skip_existing_non_empty=args.skip_existing_non_empty,
        )
        if success:
            ok += 1
            print(f"[OK] {i} -> {msg}")
        else:
            fail += 1
            failures.append(msg)
            print(f"[FAIL] {i} -> {msg}")
            if args.stop_on_fail:
                break
        if args.sleep_sec > 0:
            time.sleep(args.sleep_sec)

    print(
        json.dumps(
            {
                "ok": ok,
                "fail": fail,
                "start": args.start,
                "end": args.end,
                "output_dir": str(out_dir),
            },
            ensure_ascii=False,
        )
    )
    if failures:
        fail_log = out_dir / "bc_fetch_failures.log"
        fail_log.write_text("\n".join(failures) + "\n", encoding="utf-8")
        print(f"failure_log={fail_log}")


if __name__ == "__main__":
    main()
