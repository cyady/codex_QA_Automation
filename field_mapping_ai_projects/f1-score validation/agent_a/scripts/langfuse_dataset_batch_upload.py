#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from langfuse_dataset_poc import PROJECT_ROOT, _load_env, upload_dataset_item_for_decision


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch upload reviewed F1-score decision files to a Langfuse dataset."
    )
    parser.add_argument("--start", type=int, default=1, help="Start memo index (inclusive)")
    parser.add_argument("--end", type=int, default=29, help="End memo index (inclusive)")
    parser.add_argument(
        "--decision-dir",
        default="qa_review_ui/data/decisions/new_build_model",
        help="Directory containing M-W*.json files",
    )
    parser.add_argument(
        "--memo-dir",
        default="agent_a/data_bc",
        help="Directory containing memo_w*.txt files",
    )
    parser.add_argument(
        "--dataset-name",
        default=None,
        help="Override dataset name. Defaults to LANGFUSE_DATASET_NAME or PoC default.",
    )
    parser.add_argument(
        "--dataset-description",
        default=None,
        help="Override dataset description",
    )
    parser.add_argument(
        "--build-version",
        default=None,
        help="Override build version metadata",
    )
    parser.add_argument(
        "--deal-id",
        type=int,
        default=None,
        help="Override deal_id metadata",
    )
    parser.add_argument(
        "--sleep-sec",
        type=float,
        default=0.0,
        help="Optional sleep between uploads",
    )
    parser.add_argument(
        "--stop-on-fail",
        action="store_true",
        help="Stop immediately on first failure",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve payloads without sending to Langfuse",
    )
    parser.add_argument(
        "--summary-json",
        default=None,
        help="Optional path to save the batch summary JSON",
    )
    return parser.parse_args()


def main() -> None:
    _load_env()
    args = _parse_args()

    success: list[dict] = []
    failed: list[dict] = []
    missing: list[str] = []

    for idx in range(args.start, args.end + 1):
        decision_key = f"M-W{idx}"
        try:
            result = upload_dataset_item_for_decision(
                decision_key=decision_key,
                decision_dir=args.decision_dir,
                memo_dir=args.memo_dir,
                dataset_name=args.dataset_name or None,
                dataset_description=args.dataset_description or None,
                build_version=args.build_version or None,
                deal_id=args.deal_id or None,
                dry_run=args.dry_run,
            )
            success.append(result)
            print(f"[OK] {decision_key} -> {result['item_id']}")
        except FileNotFoundError as exc:
            message = str(exc)
            missing.append(decision_key)
            failed.append({"decision_key": decision_key, "error": message, "type": "missing"})
            print(f"[MISS] {decision_key} -> {message}")
            if args.stop_on_fail:
                break
        except Exception as exc:
            message = str(exc)
            failed.append({"decision_key": decision_key, "error": message, "type": "error"})
            print(f"[FAIL] {decision_key} -> {message}")
            if args.stop_on_fail:
                break

        if args.sleep_sec > 0:
            time.sleep(args.sleep_sec)

    summary = {
        "ok": len(success),
        "fail": len(failed),
        "missing": missing,
        "start": args.start,
        "end": args.end,
        "dry_run": args.dry_run,
        "uploaded_keys": [item["decision_key"] for item in success],
        "failed_items": failed,
    }

    if args.summary_json:
        summary_path = Path(args.summary_json)
        if not summary_path.is_absolute():
            summary_path = PROJECT_ROOT / summary_path
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
