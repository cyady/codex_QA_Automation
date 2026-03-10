#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, UTC
from pathlib import Path
from urllib import error, request

API_URL = "https://api.recatch.cc/ai-agent/fields/map"


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def post(token: str, payload: dict, timeout: int) -> tuple[int, str]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        API_URL,
        method="POST",
        data=body,
        headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"Bearer {token}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "expires": "0",
            "origin": "https://business-canvas.recatch.cc",
            "pragma": "no-cache",
            "referer": "https://business-canvas.recatch.cc/",
            "user-agent": "Mozilla/5.0",
            "x-locale": "Asia/Seoul",
            "x-recatch-request": "true",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return int(resp.status), resp.read().decode("utf-8", errors="replace")
    except error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        return int(e.code), detail


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="injection_cases.jsonl")
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("--delay-sec", type=float, default=10.0)
    ap.add_argument("--record-id", type=int, default=566094)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--max-retries", type=int, default=2)
    ap.add_argument("--token", default=None)
    args = ap.parse_args()

    token = (args.token or os.getenv("RECATCH_FB_TOKEN") or "").strip()
    if not token:
        raise SystemExit("missing token: set --token or RECATCH_FB_TOKEN")

    root = Path(__file__).resolve().parent
    cases_path = (root / args.cases).resolve()
    out_dir = (root / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    run_id = datetime.now().strftime("inj_%Y%m%d_%H%M%S")
    run_dir = out_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    cases = []
    for line in cases_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s:
            continue
        cases.append(json.loads(s))

    summary = []
    ok = fail = 0

    for idx, case in enumerate(cases, 1):
        cid = case["case_id"]
        tech = case["technique"]
        prompt = case["prompt"]
        payload = {
            "summary": prompt,
            "entity_type": "deal",
            "record_id": args.record_id,
            "date": now_iso(),
        }

        attempt = 0
        final_status = None
        final_text = ""

        while attempt <= args.max_retries:
            attempt += 1
            status, text = post(token=token, payload=payload, timeout=args.timeout)
            final_status, final_text = status, text
            if status in (200, 201):
                break
            if status in (429, 500, 502, 503, 504) and attempt <= args.max_retries:
                time.sleep(min(args.delay_sec * attempt, 40))
                continue
            break

        out_file = run_dir / f"{idx:03d}_{cid}_{tech}.json"
        parsed = None
        try:
            parsed = json.loads(final_text)
        except Exception:
            parsed = {"raw": final_text}
        out_file.write_text(
            json.dumps(
                {
                    "case": case,
                    "payload": payload,
                    "status": final_status,
                    "attempt": attempt,
                    "response": parsed,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        row = {
            "idx": idx,
            "case_id": cid,
            "technique": tech,
            "status": final_status,
            "attempt": attempt,
            "response_file": str(out_file.relative_to(out_dir)),
        }
        summary.append(row)

        if final_status in (200, 201):
            ok += 1
            print(f"[OK] {idx}/{len(cases)} {cid} {tech} status={final_status}")
        else:
            fail += 1
            print(f"[FAIL] {idx}/{len(cases)} {cid} {tech} status={final_status}")

        if idx < len(cases):
            time.sleep(args.delay_sec)

    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {
        "run_id": run_id,
        "cases": len(cases),
        "ok": ok,
        "fail": fail,
        "delay_sec": args.delay_sec,
        "record_id": args.record_id,
        "run_dir": str(run_dir),
    }
    (run_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
