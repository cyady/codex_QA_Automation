#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from urllib import error, request

URL = "https://api.recatch.cc/ai-agent/fields/map"


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def post(token: str, summary: str, record_id: int, timeout: int = 60) -> tuple[int, str]:
    payload = {
        "summary": summary,
        "entity_type": "deal",
        "record_id": record_id,
        "date": now_iso(),
    }
    req = request.Request(
        URL,
        method="POST",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
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
        return int(e.code), e.read().decode("utf-8", errors="replace")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--memo", required=True)
    ap.add_argument("--record-id", type=int, default=566094)
    ap.add_argument("--n", type=int, default=14)
    ap.add_argument("--delay-sec", type=float, default=8.0)
    ap.add_argument("--token", default=None)
    ap.add_argument("--out-dir", default="f1-score validation/agent_a/data_bc/probability_runs")
    ap.add_argument("--p-assumed", type=float, default=0.2)
    ap.add_argument("--e", type=float, default=0.05)
    args = ap.parse_args()

    token = (args.token or os.getenv("RECATCH_FB_TOKEN") or "").strip()
    if not token:
        raise SystemExit("missing token")

    memo_text = Path(args.memo).read_text(encoding="utf-8-sig")
    out_dir = Path(args.out_dir)
    run_id = datetime.now().strftime("prob_%Y%m%d_%H%M%S")
    run_dir = out_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    field_hit = Counter()
    status_hit = Counter()
    runs = []

    for i in range(1, args.n + 1):
        status, text = post(token=token, summary=memo_text, record_id=args.record_id)
        status_hit[status] += 1
        parsed: object
        try:
            parsed = json.loads(text)
        except Exception:
            parsed = {"raw": text}

        field_ids = []
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    fd = item.get("field_definition") or {}
                    fid = fd.get("id")
                    if fid is not None:
                        field_ids.append(str(fid))
            for fid in set(field_ids):
                field_hit[fid] += 1

        run = {
            "run_idx": i,
            "status": status,
            "field_ids": sorted(set(field_ids)),
            "response_len": len(parsed) if isinstance(parsed, list) else None,
        }
        runs.append(run)
        (run_dir / f"run_{i:02d}.json").write_text(
            json.dumps({"status": status, "response": parsed}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[{i}/{args.n}] status={status} unique_fields={len(set(field_ids))}")
        if i < args.n:
            time.sleep(args.delay_sec)

    field_stats = []
    for fid, hits in field_hit.items():
        p_hat = hits / args.n
        miss_prob = (1 - p_hat) ** args.n
        field_stats.append(
            {
                "field_id": fid,
                "hits": hits,
                "n": args.n,
                "p_hat": round(p_hat, 4),
                "miss_prob_after_n": round(miss_prob, 6),
            }
        )
    field_stats.sort(key=lambda x: (-x["p_hat"], x["field_id"]))

    n_required = math.ceil(math.log(args.e) / math.log(1 - args.p_assumed))

    summary = {
        "run_id": run_id,
        "record_id": args.record_id,
        "memo": str(Path(args.memo).resolve()),
        "n": args.n,
        "delay_sec": args.delay_sec,
        "status_counts": dict(status_hit),
        "assumed_p": args.p_assumed,
        "target_e": args.e,
        "n_required_from_assumed_p": n_required,
        "formula": "(1-P)^n <= e",
        "field_stats": field_stats,
        "runs": runs,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "run_dir": str(run_dir), "fields_observed": len(field_stats)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
