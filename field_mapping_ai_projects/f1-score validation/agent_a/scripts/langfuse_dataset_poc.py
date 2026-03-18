#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import ssl
from datetime import datetime, UTC
from pathlib import Path
from typing import Any
from urllib import error, parse, request

import certifi
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_NAME = "evaluation/QA_F1-score_dataset"
DECISION_KEY_RE = re.compile(r"^M-W(\d+)$")


def _load_env() -> None:
    for name in (".env", ".env.langfuse", ".env.langfuse.local"):
        path = PROJECT_ROOT / name
        if path.exists():
            load_dotenv(path, override=False)


def _env_path(name: str, default_rel: str) -> Path:
    value = (os.getenv(name) or default_rel).strip()
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def _iso_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Minimal Langfuse dataset PoC for reviewed F1-score validation items."
    )
    parser.add_argument("--decision-key", default="M-W1", help="Decision key like M-W1")
    parser.add_argument(
        "--decision-file",
        default=None,
        help="Decision JSON path. If omitted, inferred from --decision-key and --decision-dir.",
    )
    parser.add_argument(
        "--decision-dir",
        default=os.getenv("LANGFUSE_DEFAULT_DECISION_DIR", "qa_review_ui/data/decisions/new_build_model"),
        help="Directory containing reviewed decision JSON files",
    )
    parser.add_argument(
        "--memo-dir",
        default=os.getenv("LANGFUSE_DEFAULT_MEMO_DIR", "agent_a/data_bc"),
        help="Directory containing memo_w*.txt files",
    )
    parser.add_argument(
        "--dataset-name",
        default=os.getenv("LANGFUSE_DATASET_NAME", DEFAULT_DATASET_NAME),
        help="Target Langfuse dataset name",
    )
    parser.add_argument(
        "--dataset-description",
        default=os.getenv(
            "LANGFUSE_DATASET_DESCRIPTION",
            "Reviewed memo-to-field mapping gold labels for field-mapping AI",
        ),
        help="Dataset description used on create",
    )
    parser.add_argument(
        "--build-version",
        default=os.getenv("LANGFUSE_DEFAULT_BUILD_VERSION", "new_build_model"),
        help="Build version label stored in metadata",
    )
    parser.add_argument(
        "--deal-id",
        type=int,
        default=int(os.getenv("LANGFUSE_DEFAULT_DEAL_ID", "561187")),
        help="Deal id stored in metadata/input",
    )
    parser.add_argument(
        "--item-id",
        default=None,
        help="Optional global dataset item id. Defaults to qa-f1:<build-version>:<decision-key>",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the dataset payload without calling Langfuse",
    )
    return parser.parse_args()


def _decision_key_to_index(decision_key: str) -> int:
    match = DECISION_KEY_RE.match(decision_key)
    if not match:
        raise ValueError(f"unsupported decision key format: {decision_key}")
    return int(match.group(1))


def _resolve_decision_file(args: argparse.Namespace) -> Path:
    if args.decision_file:
        path = Path(args.decision_file)
        return path if path.is_absolute() else PROJECT_ROOT / path
    return _env_path("LANGFUSE_DEFAULT_DECISION_DIR", args.decision_dir) / f"{args.decision_key}.json"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_payloads(
    *,
    decision_key: str,
    decision: dict[str, Any],
    memo_text: str,
    memo_path: Path,
    decision_path: Path,
    build_version: str,
    deal_id: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    input_payload = {
        "memo_id": decision["memo_id"],
        "decision_key": decision_key,
        "memo_text": memo_text,
        "deal_id": deal_id,
        "build_version": build_version,
    }
    expected_output = {
        "memo_id": decision["memo_id"],
        "updated_at": decision.get("updated_at"),
        "model_decisions": decision.get("model_decisions", []),
        "fn_decisions": decision.get("fn_decisions", []),
    }
    metadata = {
        "source": "f1-score-validation",
        "build_version": build_version,
        "deal_id": deal_id,
        "memo_path": str(memo_path.relative_to(PROJECT_ROOT)),
        "decision_path": str(decision_path.relative_to(PROJECT_ROOT)),
        "uploaded_at": _iso_now(),
    }
    return input_payload, expected_output, metadata


def _build_dataset_schemas() -> tuple[dict[str, Any], dict[str, Any]]:
    input_schema = {
        "type": "object",
        "properties": {
            "memo_id": {"type": "string"},
            "decision_key": {"type": "string"},
            "memo_text": {"type": "string"},
            "deal_id": {"type": "integer"},
            "build_version": {"type": "string"},
        },
        "required": ["memo_id", "decision_key", "memo_text", "deal_id", "build_version"],
    }
    expected_output_schema = {
        "type": "object",
        "properties": {
            "memo_id": {"type": "string"},
            "updated_at": {"type": ["string", "null"]},
            "model_decisions": {"type": "array", "items": {"type": "object"}},
            "fn_decisions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["memo_id", "model_decisions", "fn_decisions"],
    }
    return input_schema, expected_output_schema


def _langfuse_auth_headers() -> dict[str, str]:
    host = (os.getenv("LANGFUSE_HOST") or "").strip()
    public_key = (os.getenv("LANGFUSE_PUBLIC_KEY") or "").strip()
    secret_key = (os.getenv("LANGFUSE_SECRET_KEY") or "").strip()
    missing = [
        name
        for name, value in (
            ("LANGFUSE_HOST", host),
            ("LANGFUSE_PUBLIC_KEY", public_key),
            ("LANGFUSE_SECRET_KEY", secret_key),
        )
        if not value
    ]
    if missing:
        raise SystemExit(f"missing Langfuse env vars: {', '.join(missing)}")
    basic = base64.b64encode(f"{public_key}:{secret_key}".encode("utf-8")).decode("ascii")
    return {
        "host": host.rstrip("/"),
        "Authorization": f"Basic {basic}",
        "X-Langfuse-Public-Key": public_key,
        "X-Langfuse-Sdk-Name": "field-mapping-ai-f1-poc",
        "X-Langfuse-Sdk-Version": "0.1.0",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _api_request(
    *,
    headers: dict[str, str],
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url=f"{headers['host']}/{path.lstrip('/')}",
        method=method,
        data=body,
        headers={k: v for k, v in headers.items() if k != "host"},
    )
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        with request.urlopen(req, timeout=30, context=ssl_context) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Langfuse API {method} {path} failed with {exc.code}: {detail}") from exc


def _dataset_exists(headers: dict[str, str], dataset_name: str) -> bool:
    encoded_name = parse.quote(dataset_name, safe="")
    try:
        _api_request(headers=headers, method="GET", path=f"api/public/v2/datasets/{encoded_name}")
        return True
    except RuntimeError as exc:
        if "failed with 404" in str(exc):
            return False
        raise


def _ensure_dataset(headers: dict[str, str], dataset_name: str, dataset_description: str) -> None:
    input_schema, expected_output_schema = _build_dataset_schemas()
    if _dataset_exists(headers, dataset_name):
        return
    _api_request(
        headers=headers,
        method="POST",
        path="api/public/v2/datasets",
        payload={
            "name": dataset_name,
            "description": dataset_description,
            "metadata": {"source": "f1-score-validation"},
            "inputSchema": input_schema,
            "expectedOutputSchema": expected_output_schema,
        },
    )


def upload_dataset_item_for_decision(
    *,
    decision_key: str,
    decision_file: str | Path | None = None,
    decision_dir: str | None = None,
    memo_dir: str | None = None,
    dataset_name: str | None = None,
    dataset_description: str | None = None,
    build_version: str | None = None,
    deal_id: int | None = None,
    item_id: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    decision_dir = decision_dir or os.getenv(
        "LANGFUSE_DEFAULT_DECISION_DIR", "qa_review_ui/data/decisions/new_build_model"
    )
    memo_dir = memo_dir or os.getenv("LANGFUSE_DEFAULT_MEMO_DIR", "agent_a/data_bc")
    dataset_name = dataset_name or os.getenv("LANGFUSE_DATASET_NAME", DEFAULT_DATASET_NAME)
    dataset_description = dataset_description or os.getenv(
        "LANGFUSE_DATASET_DESCRIPTION",
        "Reviewed memo-to-field mapping gold labels for field-mapping AI",
    )
    build_version = build_version or os.getenv("LANGFUSE_DEFAULT_BUILD_VERSION", "new_build_model")
    deal_id = deal_id or int(os.getenv("LANGFUSE_DEFAULT_DEAL_ID", "561187"))

    class _Args:
        pass

    args = _Args()
    args.decision_key = decision_key
    args.decision_file = str(decision_file) if decision_file is not None else None
    args.decision_dir = decision_dir
    args.memo_dir = memo_dir
    args.dataset_name = dataset_name
    args.dataset_description = dataset_description
    args.build_version = build_version
    args.deal_id = deal_id
    args.item_id = item_id

    decision_path = _resolve_decision_file(args)
    if not decision_path.exists():
        raise FileNotFoundError(f"decision file not found: {decision_path}")

    decision = _load_json(decision_path)
    resolved_decision_key = decision.get("memo_id") or decision_key
    index = _decision_key_to_index(resolved_decision_key)
    memo_dir_path = _env_path("LANGFUSE_DEFAULT_MEMO_DIR", memo_dir)
    memo_path = memo_dir_path / f"memo_w{index}.txt"
    if not memo_path.exists():
        raise FileNotFoundError(f"memo file not found: {memo_path}")

    memo_text = memo_path.read_text(encoding="utf-8")
    input_payload, expected_output, metadata = _build_payloads(
        decision_key=resolved_decision_key,
        decision=decision,
        memo_text=memo_text,
        memo_path=memo_path,
        decision_path=decision_path,
        build_version=build_version,
        deal_id=deal_id,
    )

    resolved_item_id = item_id or f"qa-f1:{build_version}:{resolved_decision_key}"
    result = {
        "dataset_name": dataset_name,
        "item_id": resolved_item_id,
        "decision_key": resolved_decision_key,
        "input": input_payload,
        "expected_output": expected_output,
        "metadata": metadata,
        "memo_path": str(memo_path),
        "decision_path": str(decision_path),
    }

    if dry_run:
        return result

    headers = _langfuse_auth_headers()
    _ensure_dataset(headers, dataset_name, dataset_description)
    item = _api_request(
        headers=headers,
        method="POST",
        path="api/public/dataset-items",
        payload={
            "datasetName": dataset_name,
            "id": resolved_item_id,
            "input": input_payload,
            "expectedOutput": expected_output,
            "metadata": metadata,
            "sourceTraceId": (os.getenv("LANGFUSE_SOURCE_TRACE_ID") or None),
            "sourceObservationId": (os.getenv("LANGFUSE_SOURCE_OBSERVATION_ID") or None),
        },
    )
    return {
        "ok": True,
        "dataset_name": dataset_name,
        "item_id": item.get("id", resolved_item_id),
        "decision_key": resolved_decision_key,
        "memo_path": str(memo_path),
        "decision_path": str(decision_path),
    }


def main() -> None:
    _load_env()
    args = _parse_args()
    result = upload_dataset_item_for_decision(
        decision_key=args.decision_key,
        decision_file=args.decision_file,
        decision_dir=args.decision_dir,
        memo_dir=args.memo_dir,
        dataset_name=args.dataset_name,
        dataset_description=args.dataset_description,
        build_version=args.build_version,
        deal_id=args.deal_id,
        item_id=args.item_id,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
