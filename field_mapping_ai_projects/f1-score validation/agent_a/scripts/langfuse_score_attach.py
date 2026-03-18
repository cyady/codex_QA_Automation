#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from langfuse_dataset_poc import _api_request


SCORE_NAMES = (
    'fm_N',
    'fm_est.tp_count',
    'fm_est.fp_count',
    'fm_est.fn_count',
    'fm_est.hitl_count',
    'fm_est.f1_per',
)


def fetch_trace_scores(
    *,
    headers: dict[str, str],
    trace_id: str,
    limit: int = 100,
) -> list[dict[str, Any]]:
    response = _api_request(
        headers=headers,
        method='GET',
        path=f'api/public/scores?traceId={trace_id}&limit={limit}',
    )
    data = response.get('data')
    return data if isinstance(data, list) else []


def delete_trace_scores(
    *,
    headers: dict[str, str],
    trace_id: str,
    score_names: tuple[str, ...] = SCORE_NAMES,
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    existing = fetch_trace_scores(headers=headers, trace_id=trace_id)
    targets = [
        item
        for item in existing
        if item.get('traceId') == trace_id and item.get('name') in score_names
    ]
    if dry_run:
        return targets

    responses: list[dict[str, Any]] = []
    for item in targets:
        score_id = item.get('id')
        if not isinstance(score_id, str) or not score_id:
            continue
        responses.append(
            _api_request(
                headers=headers,
                method='DELETE',
                path=f'api/public/scores/{score_id}',
            )
        )
    return responses


def build_numeric_score_payloads(
    *,
    trace_id: str,
    environment: str | None,
    scores: dict[str, float | int],
    comment: str | None,
    comments_by_score: dict[str, str] | None,
    metadata: dict[str, Any],
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for name in SCORE_NAMES:
        if name not in scores:
            continue
        score_comment = (comments_by_score or {}).get(name, comment)
        payloads.append(
            {
                'traceId': trace_id,
                'name': name,
                'value': float(scores[name]),
                'comment': score_comment,
                'metadata': metadata,
                'environment': environment,
                'dataType': 'NUMERIC',
            }
        )
    return payloads


def attach_trace_scores(
    *,
    headers: dict[str, str],
    trace_id: str,
    environment: str | None,
    scores: dict[str, float | int],
    comment: str | None,
    comments_by_score: dict[str, str] | None = None,
    metadata: dict[str, Any],
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    payloads = build_numeric_score_payloads(
        trace_id=trace_id,
        environment=environment,
        scores=scores,
        comment=comment,
        comments_by_score=comments_by_score,
        metadata=metadata,
    )
    if dry_run:
        return payloads

    responses: list[dict[str, Any]] = []
    for payload in payloads:
        responses.append(
            _api_request(
                headers=headers,
                method='POST',
                path='api/public/scores',
                payload=payload,
            )
        )
    return responses
