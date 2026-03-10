#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib import error, request


DEFAULT_URL = "https://api.recatch.cc/ai-agent/fields/map"


def _load_payload(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError(f"payload file is empty: {path}")
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("payload root must be a JSON object")
    return payload


def _post_json(url: str, token: str, payload: dict) -> tuple[int, dict[str, str], str]:
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
        with request.urlopen(req, timeout=60) as resp:
            status = getattr(resp, "status", 200)
            headers = dict(resp.headers.items())
            text = resp.read().decode("utf-8", errors="replace")
            return status, headers, text
    except error.HTTPError as e:
        text = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {text}") from e


def main() -> None:
    p = argparse.ArgumentParser(
        description="Call Recatch ai-agent fields map API and save response as JSON file."
    )
    p.add_argument("--payload", required=True, help="Request body JSON file path")
    p.add_argument("--output", required=True, help="Output JSON file path")
    p.add_argument("--url", default=DEFAULT_URL, help=f"API URL (default: {DEFAULT_URL})")
    p.add_argument(
        "--token-env",
        default="RECATCH_FB_TOKEN",
        help="Environment variable name containing bearer token",
    )
    p.add_argument(
        "--token",
        default=None,
        help="Bearer token value. If omitted, reads from --token-env",
    )
    args = p.parse_args()

    token = (args.token or os.getenv(args.token_env) or "").strip()
    if not token:
        print(
            f"missing token: set --token or export {args.token_env}",
            file=sys.stderr,
        )
        sys.exit(2)

    payload = _load_payload(Path(args.payload))
    status, headers, text = _post_json(args.url, token, payload)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Save pretty JSON when possible; fallback to raw text.
    try:
        parsed = json.loads(text)
        out_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        is_json = True
    except json.JSONDecodeError:
        out_path.write_text(text, encoding="utf-8")
        is_json = False

    print(
        json.dumps(
            {
                "ok": True,
                "status": status,
                "output": str(out_path),
                "content_type": headers.get("Content-Type"),
                "saved_as_json": is_json,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
