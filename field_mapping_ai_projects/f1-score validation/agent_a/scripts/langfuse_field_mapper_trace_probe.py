#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from langfuse_dataset_poc import _api_request, _langfuse_auth_headers, _load_env

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Probe Langfuse traces/observations/scores for field-mapper tagged runs.'
    )
    parser.add_argument('--tag', default='field-mapper', help='Trace tag to filter on')
    parser.add_argument('--limit', type=int, default=5, help='Number of traces to fetch')
    parser.add_argument('--include-observations', action='store_true', help='Fetch observations for each trace')
    parser.add_argument('--dump-json', default=None, help='Optional JSON output path')
    return parser.parse_args()


def _get(path: str, headers: dict[str, str]) -> dict[str, Any]:
    return _api_request(headers=headers, method='GET', path=path)


def main() -> None:
    args = parse_args()
    _load_env()
    headers = _langfuse_auth_headers()

    traces = _get(f'/api/public/traces?limit={args.limit}&tags={args.tag}', headers)
    data = traces.get('data', [])

    summary: list[dict[str, Any]] = []
    for trace in data:
        row: dict[str, Any] = {
            'id': trace.get('id'),
            'name': trace.get('name'),
            'tags': trace.get('tags'),
            'timestamp': trace.get('timestamp'),
            'userId': trace.get('userId'),
            'sessionId': trace.get('sessionId'),
            'environment': trace.get('environment'),
            'input_type': type(trace.get('input')).__name__,
            'output_keys': sorted((trace.get('output') or {}).keys()) if isinstance(trace.get('output'), dict) else [],
            'metadata_keys': sorted((trace.get('metadata') or {}).keys()) if isinstance(trace.get('metadata'), dict) else [],
        }
        if args.include_observations:
            obs = _get(f"/api/public/observations?traceId={trace.get('id')}&limit=50", headers)
            row['observations'] = [
                {
                    'id': o.get('id'),
                    'name': o.get('name'),
                    'type': o.get('type'),
                    'level': o.get('level'),
                    'providedModelName': o.get('providedModelName'),
                }
                for o in obs.get('data', [])
            ]
        summary.append(row)

    print(json.dumps({'count': len(summary), 'traces': summary}, ensure_ascii=False, indent=2))

    if args.dump_json:
        out_path = Path(args.dump_json)
        if not out_path.is_absolute():
            out_path = PROJECT_ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps({'count': len(summary), 'traces': summary}, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Wrote summary to {out_path}')


if __name__ == '__main__':
    main()
