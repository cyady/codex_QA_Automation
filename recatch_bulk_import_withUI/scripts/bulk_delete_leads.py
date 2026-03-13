#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import os
import ssl
import socket
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request


DEFAULT_URL = "https://api.crackapp.co/sales-entity/lead/bulk?version=20260305"
DEFAULT_ORIGIN = "https://recatch-nextjs-k5c67vi45-business-canvas-front-team.vercel.app"
DEFAULT_REFERER = f"{DEFAULT_ORIGIN}/"
TOKEN_ENV = "RECATCH_BULK_DELETE_BEARER_TOKEN"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Delete Re:catch leads in adaptive bulk batches.",
    )
    parser.add_argument("--start-id", type=int, required=True)
    parser.add_argument("--end-id", type=int, required=True)
    parser.add_argument("--start-batch-size", type=int, default=1000)
    parser.add_argument("--max-batch-size", type=int, default=2000)
    parser.add_argument("--batch-step", type=int, default=250)
    parser.add_argument("--min-batch-size", type=int, default=100)
    parser.add_argument("--slow-threshold-secs", type=float, default=60.0)
    parser.add_argument("--request-timeout-secs", type=float, default=90.0)
    parser.add_argument("--sleep-secs", type=float, default=0.5)
    parser.add_argument("--lock-retry-secs", type=float, default=30.0)
    parser.add_argument("--lock-retry-limit", type=int, default=20)
    parser.add_argument("--url", default=os.environ.get("RECATCH_BULK_DELETE_URL", DEFAULT_URL))
    parser.add_argument("--origin", default=os.environ.get("RECATCH_BULK_DELETE_ORIGIN", DEFAULT_ORIGIN))
    parser.add_argument("--referer", default=os.environ.get("RECATCH_BULK_DELETE_REFERER", DEFAULT_REFERER))
    parser.add_argument("--token-env", default=TOKEN_ENV)
    parser.add_argument("--descending", action="store_true", help="Delete from end-id down to start-id.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--log-file",
        default=str(
            Path("logs")
            / f"lead-bulk-delete-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        ),
    )
    return parser.parse_args()


def configure_logging(log_file: str) -> logging.Logger:
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("bulk_delete")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def build_headers(token: str, origin: str, referer: str) -> dict[str, str]:
    return {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "expires": "0",
        "origin": origin,
        "pragma": "no-cache",
        "referer": referer,
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        ),
        "x-locale": "Asia/Seoul",
        "x-recatch-request": "true",
    }


def build_payload(first_id: int, last_id: int, descending: bool) -> list[dict[str, Any]]:
    if descending:
        ids = range(last_id, first_id - 1, -1)
    else:
        ids = range(first_id, last_id + 1)
    return [{"id": lead_id, "method": "DELETE"} for lead_id in ids]


def send_delete_request(
    *,
    url: str,
    headers: dict[str, str],
    payload: list[dict[str, Any]],
    timeout_secs: float,
    insecure: bool,
) -> tuple[int, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method="POST")
    context = ssl._create_unverified_context() if insecure else None
    with request.urlopen(req, timeout=timeout_secs, context=context) as resp:
        raw = resp.read()
        if not raw:
            return resp.status, None
        try:
            return resp.status, json.loads(raw)
        except json.JSONDecodeError:
            return resp.status, raw.decode("utf-8", errors="replace")


def truncate(value: Any, limit: int = 400) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=True)
    if len(text) <= limit:
        return text
    return f"{text[:limit]}...<truncated>"


def summarize_response(value: Any) -> str:
    if isinstance(value, list):
        status_counts: dict[str, int] = {}
        for item in value:
            status = (
                item.get("result", {}).get("status", "UNKNOWN")
                if isinstance(item, dict)
                else "UNKNOWN"
            )
            status_counts[status] = status_counts.get(status, 0) + 1
        return json.dumps({"items": len(value), "status_counts": status_counts}, ensure_ascii=True)
    return truncate(value)


def main() -> int:
    args = parse_args()
    logger = configure_logging(args.log_file)

    if args.start_id > args.end_id:
        logger.error("start-id must be <= end-id")
        return 2

    token = os.environ.get(args.token_env)
    if not token and not args.dry_run:
        logger.error("missing bearer token env: %s", args.token_env)
        return 2

    headers = build_headers(token or "dry-run-token", args.origin, args.referer)
    batch_size = args.start_batch_size
    frozen_batch_size: int | None = None
    current_id = args.start_id
    total_deleted = 0
    total_ids = args.end_id - args.start_id + 1
    lock_retries = 0

    logger.info(
        "starting bulk delete start_id=%s end_id=%s total_ids=%s start_batch_size=%s max_batch_size=%s slow_threshold_secs=%s dry_run=%s log_file=%s",
        args.start_id,
        args.end_id,
        total_ids,
        args.start_batch_size,
        args.max_batch_size,
        args.slow_threshold_secs,
        args.dry_run,
        args.log_file,
    )

    while current_id <= args.end_id:
        last_id = min(args.end_id, current_id + batch_size - 1)
        payload = build_payload(current_id, last_id, args.descending)
        count = last_id - current_id + 1
        logger.info(
            "batch start_id=%s end_id=%s count=%s batch_size=%s frozen_batch_size=%s",
            current_id,
            last_id,
            count,
            batch_size,
            frozen_batch_size,
        )

        if args.dry_run:
            logger.info("dry-run payload_preview=%s", truncate(payload[:3] + payload[-3:]))
            total_deleted += count
            current_id = last_id + 1
            continue

        started_at = time.monotonic()
        try:
            status, response_body = send_delete_request(
                url=args.url,
                headers=headers,
                payload=payload,
                timeout_secs=args.request_timeout_secs,
                insecure=args.insecure,
            )
            elapsed = time.monotonic() - started_at
        except error.HTTPError as exc:
            elapsed = time.monotonic() - started_at
            raw_body = exc.read().decode("utf-8", errors="replace")
            is_lock_conflict = exc.code == 409 and "locked" in raw_body.lower()
            logger.error(
                "http error status=%s elapsed_secs=%.2f start_id=%s end_id=%s batch_size=%s body=%s",
                exc.code,
                elapsed,
                current_id,
                last_id,
                batch_size,
                truncate(raw_body),
            )
            if is_lock_conflict:
                lock_retries += 1
                if args.lock_retry_limit > 0 and lock_retries > args.lock_retry_limit:
                    logger.error(
                        "lock retry limit exceeded lock_retries=%s limit=%s",
                        lock_retries,
                        args.lock_retry_limit,
                    )
                    return 1
                logger.warning(
                    "resource locked; retrying same batch after %.1f seconds lock_retries=%s",
                    args.lock_retry_secs,
                    lock_retries,
                )
                time.sleep(args.lock_retry_secs)
                continue
            if exc.code in {408, 413, 429, 500, 502, 503, 504} and batch_size > args.min_batch_size:
                next_batch_size = max(args.min_batch_size, batch_size // 2)
                logger.warning(
                    "retrying smaller batch after http error old_batch_size=%s new_batch_size=%s",
                    batch_size,
                    next_batch_size,
                )
                batch_size = next_batch_size
                frozen_batch_size = batch_size
                time.sleep(args.sleep_secs)
                continue
            return 1
        except (error.URLError, TimeoutError, socket.timeout) as exc:
            elapsed = time.monotonic() - started_at
            logger.error(
                "request error elapsed_secs=%.2f start_id=%s end_id=%s batch_size=%s error=%s",
                elapsed,
                current_id,
                last_id,
                batch_size,
                exc,
            )
            if batch_size > args.min_batch_size:
                next_batch_size = max(args.min_batch_size, batch_size // 2)
                logger.warning(
                    "retrying smaller batch after request error old_batch_size=%s new_batch_size=%s",
                    batch_size,
                    next_batch_size,
                )
                batch_size = next_batch_size
                frozen_batch_size = batch_size
                time.sleep(args.sleep_secs)
                continue
            return 1

        logger.info(
            "batch success status=%s elapsed_secs=%.2f start_id=%s end_id=%s count=%s response_summary=%s",
            status,
            elapsed,
            current_id,
            last_id,
            count,
            summarize_response(response_body),
        )

        lock_retries = 0
        total_deleted += count
        current_id = last_id + 1

        if frozen_batch_size is None and elapsed >= args.slow_threshold_secs:
            frozen_batch_size = batch_size
            logger.info(
                "freezing batch size at %s because elapsed_secs=%.2f exceeded threshold=%.2f",
                batch_size,
                elapsed,
                args.slow_threshold_secs,
            )
        elif frozen_batch_size is None and batch_size < args.max_batch_size:
            batch_size = min(args.max_batch_size, batch_size + args.batch_step)
            logger.info("increasing batch size to %s", batch_size)
        elif frozen_batch_size is not None:
            batch_size = frozen_batch_size

        time.sleep(args.sleep_secs)

    logger.info("completed bulk delete deleted=%s total_ids=%s", total_deleted, total_ids)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
