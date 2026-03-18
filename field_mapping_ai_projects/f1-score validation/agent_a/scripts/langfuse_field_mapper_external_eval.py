#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

import certifi

from langfuse_dataset_poc import PROJECT_ROOT, _api_request, _langfuse_auth_headers, _load_env
from langfuse_score_attach import attach_trace_scores, delete_trace_scores

TRACE_TAG_DEFAULT = 'field-mapper'
EMBED_MODEL_DEFAULT = 'intfloat/multilingual-e5-large-instruct'
EMBED_API_URL_TEMPLATE = (
    'https://router.huggingface.co/hf-inference/models/{model}/pipeline/feature-extraction'
)
MAPPED_QUERY_TASK = (
    'Given a CRM field mapping candidate from a meeting note, retrieve the most semantically '
    'matching CRM field definition.'
)
NOTE_CHUNK_QUERY_TASK = (
    'Given a sentence or paragraph from a meeting note, retrieve the CRM field definition whose '
    'business purpose best matches the text.'
)
MEETING_NOTE_MARKER = '## Meeting Note'
FIELD_SCHEMA_MARKER = '## Field Schema'
CURRENT_DATE_MARKER = 'Current Date'
TOKEN_RE = re.compile(r'[0-9A-Za-z가-힣_]+')
ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ISO_DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}')
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
URL_RE = re.compile(r'^https?://', re.IGNORECASE)
PHONE_DIGIT_RE = re.compile(r'\d')
CHUNK_NUMBER_RE = re.compile(r'\d')
CHUNK_DATE_RE = re.compile(r'(\d{4}[./-]\d{1,2}[./-]\d{1,2})|(\d{1,2}월\s*\d{1,2}일)|오늘|내일|다음 달|이번 달')
CHUNK_EMAIL_RE = re.compile(r'[^@\s]+@[^@\s]+\.[^@\s]+')
CHUNK_URL_RE = re.compile(r'https?://', re.IGNORECASE)
CHUNK_PHONE_RE = re.compile(r'\d{2,4}[- ]?\d{3,4}[- ]?\d{4}')

TYPE_FAMILY_MAP = {
    'text': 'free_text',
    'textarea': 'free_text',
    'currency': 'numeric',
    'number': 'numeric',
    'date': 'temporal',
    'date-time': 'temporal',
    'select': 'enum',
    'multi-select': 'enum',
    'checkbox': 'enum',
    'many-to-one': 'relation',
    'user': 'relation',
    'email': 'contact_or_identifier',
    'phone-number': 'contact_or_identifier',
    'url': 'contact_or_identifier',
    'name': 'contact_or_identifier',
}


@dataclass
class EvalThresholds:
    tp_score_min: float
    tp_margin_min: float
    fp_mapped_score_max: float
    fp_alt_gap_min: float
    fn_score_min: float
    fn_margin_min: float
    hitl_score_min: float


@dataclass
class RankedField:
    field_id: str
    label: str
    type: str
    type_family: str
    cosine_score: float
    lexical_overlap: float
    hybrid_score: float


@dataclass
class EvalEntry:
    bucket: str
    source: str
    field_id: str
    field_label: str
    field_type: str
    type_family: str
    score: float
    cosine_score: float
    lexical_overlap: float
    margin: float
    reason: str
    matched_field_id: str | None
    query_preview: str


class HFEmbeddingClient:
    def __init__(self, *, model_id: str, api_token: str, batch_size: int = 16):
        self.model_id = model_id
        self.api_token = api_token
        self.batch_size = batch_size
        self._cache: dict[str, list[float]] = {}

    def embed_texts(self, texts: list[str], *, task: str | None) -> list[list[float]]:
        cache_keys = [self._cache_key(text, task=task) for text in texts]
        missing_indices = [idx for idx, key in enumerate(cache_keys) if key not in self._cache]

        if missing_indices:
            prepared = [self._prepare_query_text(texts[idx], task=task) for idx in missing_indices]
            for start in range(0, len(prepared), self.batch_size):
                batch = prepared[start : start + self.batch_size]
                batch_embeddings = self._call_feature_extraction(batch)
                for local_idx, embedding in enumerate(batch_embeddings):
                    original_idx = missing_indices[start + local_idx]
                    self._cache[cache_keys[original_idx]] = embedding

        return [self._cache[key] for key in cache_keys]

    def _cache_key(self, text: str, *, task: str | None) -> str:
        return f'{task or "document"}::{text}'

    def _prepare_query_text(self, text: str, *, task: str | None) -> str:
        if task:
            return f'Instruct: {task}\nQuery: {text}'
        return text

    def _call_feature_extraction(self, texts: list[str]) -> list[list[float]]:
        payload = {
            'inputs': texts,
            'normalize': True,
            'truncate': True,
            'truncation_direction': 'right',
        }
        req = request.Request(
            url=EMBED_API_URL_TEMPLATE.format(model=self.model_id),
            method='POST',
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {self.api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        )
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        try:
            with request.urlopen(req, timeout=60, context=ssl_context) as resp:
                raw = resp.read().decode('utf-8')
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='replace')
            raise RuntimeError(
                f'Hugging Face feature-extraction failed with {exc.code}: {detail}'
            ) from exc

        parsed = json.loads(raw)
        if not isinstance(parsed, list) or not parsed:
            raise RuntimeError(f'unexpected embedding response shape: {type(parsed).__name__}')
        if isinstance(parsed[0], (float, int)):
            return [parsed]
        return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Run external evaluation on live Langfuse field-mapper traces and attach scores.'
    )
    parser.add_argument('--tag', default=TRACE_TAG_DEFAULT, help='Trace tag to fetch')
    parser.add_argument('--limit', type=int, default=3, help='Number of recent traces to evaluate')
    parser.add_argument(
        '--trace-id',
        action='append',
        default=[],
        help='Specific trace id(s) to evaluate. If set, --limit is ignored.',
    )
    parser.add_argument(
        '--summary-json',
        default=None,
        help='Optional JSON output path for the evaluation summary',
    )
    parser.add_argument(
        '--sleep-sec',
        type=float,
        default=0.0,
        help='Optional sleep between traces',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Evaluate and print payloads without attaching scores',
    )
    parser.add_argument(
        '--skip-existing',
        action='store_true',
        help='Skip traces that already have fm_est.f1_per attached',
    )
    parser.add_argument(
        '--overwrite-existing',
        action='store_true',
        help='Delete existing fm_* scores on the trace before attaching new ones',
    )
    parser.add_argument(
        '--max-chunks',
        type=int,
        default=int(os.getenv('FM_MAX_NOTE_CHUNKS', '40')),
        help='Maximum memo chunks used for FN/HITL candidate discovery',
    )
    parser.add_argument(
        '--hf-model-id',
        default=os.getenv('FM_EMBED_MODEL_ID', EMBED_MODEL_DEFAULT),
        help='Hugging Face embedding model id',
    )
    return parser.parse_args()


def _thresholds_from_env() -> EvalThresholds:
    return EvalThresholds(
        tp_score_min=float(os.getenv('FM_TP_SCORE_MIN', '84')),
        tp_margin_min=float(os.getenv('FM_TP_MARGIN_MIN', '5')),
        fp_mapped_score_max=float(os.getenv('FM_FP_MAPPED_SCORE_MAX', '72')),
        fp_alt_gap_min=float(os.getenv('FM_FP_ALT_GAP_MIN', '8')),
        fn_score_min=float(os.getenv('FM_FN_SCORE_MIN', '86')),
        fn_margin_min=float(os.getenv('FM_FN_MARGIN_MIN', '6')),
        hitl_score_min=float(os.getenv('FM_HITL_SCORE_MIN', '78')),
    )


def _require_hf_token() -> str:
    token = (os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACEHUB_API_TOKEN') or '').strip()
    if not token:
        raise SystemExit('missing HF_TOKEN (or HUGGINGFACEHUB_API_TOKEN) for embedding inference')
    return token


def _get(path: str, headers: dict[str, str]) -> dict[str, Any]:
    return _api_request(headers=headers, method='GET', path=path)


def _fetch_trace(headers: dict[str, str], trace_id: str) -> dict[str, Any]:
    return _get(f'/api/public/traces/{trace_id}', headers)


def _fetch_traces(headers: dict[str, str], *, tag: str, limit: int) -> list[dict[str, Any]]:
    payload = _get(f'/api/public/traces?limit={limit}&tags={tag}', headers)
    return payload.get('data', [])


def _flatten_text_parts(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            parts.extend(_flatten_text_parts(item))
        return parts
    if isinstance(value, dict):
        if isinstance(value.get('text'), str):
            return [value['text']]
        if 'content' in value:
            return _flatten_text_parts(value['content'])
    return []


def _extract_trace_text(trace: dict[str, Any]) -> str:
    return '\n'.join(_flatten_text_parts(trace.get('input')))


def _extract_meeting_note_and_schema(trace: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    text = _extract_trace_text(trace)
    meeting_idx = text.find(MEETING_NOTE_MARKER)
    schema_idx = text.find(FIELD_SCHEMA_MARKER)
    if meeting_idx == -1 or schema_idx == -1:
        raise ValueError('trace input does not contain expected Meeting Note / Field Schema markers')

    meeting_note = text[meeting_idx + len(MEETING_NOTE_MARKER) : schema_idx].strip()
    schema_start = text.find('[', schema_idx)
    if schema_start == -1:
        raise ValueError('field schema JSON array start was not found')
    depth = 0
    in_string = False
    escaped = False
    schema_end = -1
    for idx in range(schema_start, len(text)):
        ch = text[idx]
        if in_string:
            if escaped:
                escaped = False
            elif ch == '\\\\':
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                schema_end = idx + 1
                break
    if schema_end == -1:
        raise ValueError('field schema JSON array end was not found')
    schema_text = text[schema_start:schema_end]
    schema = json.loads(schema_text)
    if not isinstance(schema, list):
        raise ValueError('field schema is not a list')
    return meeting_note, schema


def _field_type_family(field_type: str) -> str:
    return TYPE_FAMILY_MAP.get(field_type, 'other')


def _option_labels(field: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    for option in field.get('options') or []:
        label = (option.get('label') or '').strip()
        caption = (option.get('caption') or '').strip()
        if label:
            labels.append(label)
        if caption:
            labels.append(caption)
    return labels


def _build_field_blob(field: dict[str, Any]) -> str:
    parts = [
        f"Field label: {(field.get('label') or '').strip()}",
        f"Field type: {(field.get('type') or '').strip()}",
        f"Field type family: {_field_type_family((field.get('type') or '').strip())}",
    ]
    description = (field.get('description') or '').strip()
    caption = (field.get('caption') or '').strip()
    if description:
        parts.append(f'Description: {description}')
    if caption:
        parts.append(f'Caption: {caption}')
    option_labels = _option_labels(field)
    if option_labels:
        parts.append('Options: ' + ' | '.join(option_labels))
    return '\n'.join(parts)


def _normalize_tokens(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def _lexical_overlap_ratio(query: str, document: str) -> float:
    query_tokens = set(_normalize_tokens(query))
    if not query_tokens:
        return 0.0
    doc_tokens = set(_normalize_tokens(document))
    return len(query_tokens & doc_tokens) / len(query_tokens)


def _dot_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right)) * 100.0


def _option_value_to_label(field: dict[str, Any], value: Any) -> str | None:
    for option in field.get('options') or []:
        if option.get('value') == value:
            return option.get('label') or str(value)
    return None


def _format_value_for_query(field: dict[str, Any], value: Any) -> str:
    field_type = (field.get('type') or '').strip()
    if field_type == 'select':
        return _option_value_to_label(field, value) or str(value)
    if field_type == 'multi-select' and isinstance(value, list):
        labels = [_option_value_to_label(field, item) or str(item) for item in value]
        return ', '.join(labels)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _is_numeric_like(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        stripped = value.strip().replace(',', '')
        return bool(stripped) and stripped.replace('.', '', 1).isdigit()
    return False


def _type_compatible_for_value(field: dict[str, Any], value: Any) -> bool:
    field_type = (field.get('type') or '').strip()
    if field_type in {'text', 'textarea', 'name'}:
        return isinstance(value, str) and bool(value.strip())
    if field_type in {'currency', 'number'}:
        return _is_numeric_like(value)
    if field_type == 'date':
        return isinstance(value, str) and bool(ISO_DATE_RE.match(value.strip()))
    if field_type == 'date-time':
        return isinstance(value, str) and bool(ISO_DATETIME_RE.match(value.strip()))
    if field_type == 'checkbox':
        return isinstance(value, bool)
    if field_type == 'select':
        return any(option.get('value') == value for option in field.get('options') or [])
    if field_type == 'multi-select':
        return isinstance(value, list) and all(
            any(option.get('value') == item for option in field.get('options') or []) for item in value
        )
    if field_type == 'email':
        return isinstance(value, str) and bool(EMAIL_RE.match(value.strip()))
    if field_type == 'url':
        return isinstance(value, str) and bool(URL_RE.match(value.strip()))
    if field_type == 'phone-number':
        digits = PHONE_DIGIT_RE.findall(str(value))
        return len(digits) >= 8
    if field_type in {'many-to-one', 'user'}:
        return value is not None and str(value).strip() != ''
    return True


def _chunk_text_compatible(field: dict[str, Any], chunk: str) -> bool:
    field_type = (field.get('type') or '').strip()
    if field_type in {'currency', 'number'}:
        return bool(CHUNK_NUMBER_RE.search(chunk))
    if field_type in {'date', 'date-time'}:
        return bool(CHUNK_DATE_RE.search(chunk))
    if field_type == 'email':
        return bool(CHUNK_EMAIL_RE.search(chunk))
    if field_type == 'url':
        return bool(CHUNK_URL_RE.search(chunk))
    if field_type == 'phone-number':
        return bool(CHUNK_PHONE_RE.search(chunk))
    return True


def _split_meeting_note_chunks(note_text: str, *, max_chunks: int) -> list[str]:
    raw_lines = [line.strip() for line in note_text.splitlines()]
    chunks: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if not current:
            return
        text = ' '.join(part for part in current if part).strip()
        if text:
            chunks.append(text)
        current.clear()

    for line in raw_lines:
        if not line:
            flush()
            continue
        if line.startswith('■'):
            flush()
            current.append(line)
            continue
        if line.startswith(('-', '•', '◦')):
            flush()
            current.append(line.lstrip('-•◦ ').strip())
            continue
        current.append(line)

    flush()

    deduped: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        normalized = re.sub(r'\s+', ' ', chunk).strip()
        if len(normalized) < 12:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
        if len(deduped) >= max_chunks:
            break
    return deduped


def _rank_fields_for_queries(
    *,
    embedder: HFEmbeddingClient,
    queries: list[str],
    fields: list[dict[str, Any]],
    query_task: str,
) -> list[list[RankedField]]:
    field_blobs = [_build_field_blob(field) for field in fields]
    doc_embeddings = embedder.embed_texts(field_blobs, task=None)
    query_embeddings = embedder.embed_texts(queries, task=query_task)

    results: list[list[RankedField]] = []
    for query_text, query_embedding in zip(queries, query_embeddings):
        ranked: list[RankedField] = []
        for field, field_blob, doc_embedding in zip(fields, field_blobs, doc_embeddings):
            cosine_score = _dot_similarity(query_embedding, doc_embedding)
            lexical_overlap = _lexical_overlap_ratio(query_text, field_blob)
            hybrid_score = cosine_score + (lexical_overlap * 5.0)
            ranked.append(
                RankedField(
                    field_id=str(field.get('id')),
                    label=(field.get('label') or '').strip(),
                    type=(field.get('type') or '').strip(),
                    type_family=_field_type_family((field.get('type') or '').strip()),
                    cosine_score=cosine_score,
                    lexical_overlap=lexical_overlap,
                    hybrid_score=hybrid_score,
                )
            )
        ranked.sort(key=lambda item: (-item.hybrid_score, item.field_id))
        results.append(ranked)
    return results


def _mapping_query_text(field: dict[str, Any], mapping: dict[str, Any]) -> str:
    value_text = _format_value_for_query(field, mapping.get('extracted_value'))
    reasoning = str(mapping.get('reasoning') or '').strip()
    lines = [f'Extracted value: {value_text}']
    if reasoning:
        lines.append(f'Reasoning: {reasoning}')
    return '\n'.join(lines)


def _find_field(fields_by_id: dict[str, dict[str, Any]], field_id: Any) -> dict[str, Any] | None:
    return fields_by_id.get(str(field_id))


def _top_margin(ranked: list[RankedField]) -> float:
    if not ranked:
        return 0.0
    if len(ranked) == 1:
        return ranked[0].hybrid_score
    return ranked[0].hybrid_score - ranked[1].hybrid_score


def _preview(text: str, max_len: int = 120) -> str:
    compact = re.sub(r'\s+', ' ', text).strip()
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 3] + '...'


def _classify_mapped_outputs(
    *,
    mappings: list[dict[str, Any]],
    fields: list[dict[str, Any]],
    ranked_results: list[list[RankedField]],
    thresholds: EvalThresholds,
) -> list[EvalEntry]:
    fields_by_id = {str(field.get('id')): field for field in fields}
    entries: list[EvalEntry] = []

    for mapping, ranked in zip(mappings, ranked_results):
        mapped_field_id = str(mapping.get('field_id'))
        mapped_field = _find_field(fields_by_id, mapped_field_id)
        if not mapped_field:
            entries.append(
                EvalEntry(
                    bucket='HITL',
                    source='mapped_output',
                    field_id=mapped_field_id,
                    field_label=mapped_field_id,
                    field_type='unknown',
                    type_family='other',
                    score=0.0,
                    cosine_score=0.0,
                    lexical_overlap=0.0,
                    margin=0.0,
                    reason='field id not found in schema',
                    matched_field_id=None,
                    query_preview=_preview(json.dumps(mapping, ensure_ascii=False)),
                )
            )
            continue

        score_by_field = {item.field_id: item for item in ranked}
        mapped_rank = score_by_field.get(mapped_field_id)
        best_rank = ranked[0]
        margin = _top_margin(ranked)
        compatible = _type_compatible_for_value(mapped_field, mapping.get('extracted_value'))
        query_preview = _preview(_mapping_query_text(mapped_field, mapping))
        mapped_score = mapped_rank.hybrid_score if mapped_rank else 0.0
        mapped_cosine = mapped_rank.cosine_score if mapped_rank else 0.0
        mapped_lexical = mapped_rank.lexical_overlap if mapped_rank else 0.0

        if (
            best_rank.field_id == mapped_field_id
            and compatible
            and mapped_score >= thresholds.tp_score_min
            and margin >= thresholds.tp_margin_min
        ):
            bucket = 'TP'
            reason = 'top1 matched mapped field with strong score and margin'
        elif (
            best_rank.field_id != mapped_field_id
            and mapped_score <= thresholds.fp_mapped_score_max
            and (best_rank.hybrid_score - mapped_score) >= thresholds.fp_alt_gap_min
        ):
            bucket = 'FP'
            reason = (
                f'alternative field {best_rank.field_id} outranked mapped field by '
                f'{best_rank.hybrid_score - mapped_score:.2f}'
            )
        else:
            bucket = 'HITL'
            reason = 'ambiguous mapped output; threshold or type confidence not strong enough'

        if not compatible and bucket == 'TP':
            bucket = 'HITL'
            reason = 'mapped field value type was not compatible'

        entries.append(
            EvalEntry(
                bucket=bucket,
                source='mapped_output',
                field_id=mapped_field_id,
                field_label=(mapped_field.get('label') or mapped_field_id).strip(),
                field_type=(mapped_field.get('type') or '').strip(),
                type_family=_field_type_family((mapped_field.get('type') or '').strip()),
                score=round(mapped_score, 4),
                cosine_score=round(mapped_cosine, 4),
                lexical_overlap=round(mapped_lexical, 4),
                margin=round(margin, 4),
                reason=reason,
                matched_field_id=best_rank.field_id,
                query_preview=query_preview,
            )
        )

    return entries


def _classify_unmatched_chunks(
    *,
    note_chunks: list[str],
    mapped_field_ids: set[str],
    fields: list[dict[str, Any]],
    ranked_results: list[list[RankedField]],
    thresholds: EvalThresholds,
) -> list[EvalEntry]:
    fields_by_id = {str(field.get('id')): field for field in fields}
    best_by_field: dict[str, EvalEntry] = {}

    for chunk, ranked in zip(note_chunks, ranked_results):
        if not ranked:
            continue
        best_rank = ranked[0]
        margin = _top_margin(ranked)
        if best_rank.field_id in mapped_field_ids:
            continue

        field = _find_field(fields_by_id, best_rank.field_id)
        if not field:
            continue
        if not _chunk_text_compatible(field, chunk):
            continue

        if best_rank.hybrid_score >= thresholds.fn_score_min and margin >= thresholds.fn_margin_min:
            bucket = 'FN'
            reason = 'unmatched note chunk strongly aligned with schema field'
        elif best_rank.hybrid_score >= thresholds.hitl_score_min:
            bucket = 'HITL'
            reason = 'unmatched note chunk looked relevant but confidence was not decisive'
        else:
            continue

        entry = EvalEntry(
            bucket=bucket,
            source='input_chunk',
            field_id=best_rank.field_id,
            field_label=best_rank.label,
            field_type=best_rank.type,
            type_family=best_rank.type_family,
            score=round(best_rank.hybrid_score, 4),
            cosine_score=round(best_rank.cosine_score, 4),
            lexical_overlap=round(best_rank.lexical_overlap, 4),
            margin=round(margin, 4),
            reason=reason,
            matched_field_id=best_rank.field_id,
            query_preview=_preview(chunk),
        )

        previous = best_by_field.get(best_rank.field_id)
        if previous is None or entry.score > previous.score or (
            entry.bucket == 'FN' and previous.bucket != 'FN'
        ):
            best_by_field[best_rank.field_id] = entry

    return sorted(best_by_field.values(), key=lambda item: (-item.score, item.field_id))


def _coerce_structured_output(output: Any) -> list[dict[str, Any]]:
    if isinstance(output, dict):
        structured = output.get('structuredResponse')
        if isinstance(structured, dict):
            field_mappings = structured.get('field_mappings') or structured.get('fieldMappings') or []
            if isinstance(field_mappings, list):
                return [item for item in field_mappings if isinstance(item, dict)]
    return []


def _format_bucket_comment(entries: list[EvalEntry], *, max_items: int = 12) -> str:
    if not entries:
        return '-'
    labels = [f'{entry.field_id}({entry.field_label})' for entry in entries[:max_items]]
    if len(entries) > max_items:
        labels.append(f'+{len(entries) - max_items} more')
    return ', '.join(labels)


def _fixed_comment_template(entries: list[EvalEntry]) -> str:
    grouped = {
        bucket: [entry for entry in entries if entry.bucket == bucket]
        for bucket in ('TP', 'FP', 'FN', 'HITL')
    }
    parts = []
    for bucket in ('TP', 'FP', 'FN', 'HITL'):
        bucket_entries = grouped[bucket]
        parts.append(f'{bucket}[{len(bucket_entries)}]: {_format_bucket_comment(bucket_entries)}')
    return ' | '.join(parts)


def _bucket_entries(entries: list[EvalEntry], bucket: str) -> list[EvalEntry]:
    return [entry for entry in entries if entry.bucket == bucket]


def _score_comments(entries: list[EvalEntry], scores: dict[str, float]) -> dict[str, str]:
    tp_entries = _bucket_entries(entries, 'TP')
    fp_entries = _bucket_entries(entries, 'FP')
    fn_entries = _bucket_entries(entries, 'FN')
    hitl_entries = _bucket_entries(entries, 'HITL')
    total = int(scores.get('fm_N', 0.0))

    tp_comment = (
        f"TP {scores.get('fm_est.tp_count', 0.0):.2f}% "
        f"({len(tp_entries)}/{total}) | {_format_bucket_comment(tp_entries, max_items=6)}"
    )
    fp_comment = (
        f"FP {scores.get('fm_est.fp_count', 0.0):.2f}% "
        f"({len(fp_entries)}/{total}) | {_format_bucket_comment(fp_entries, max_items=6)}"
    )
    fn_comment = (
        f"FN {scores.get('fm_est.fn_count', 0.0):.2f}% "
        f"({len(fn_entries)}/{total}) | {_format_bucket_comment(fn_entries, max_items=6)}"
    )
    hitl_comment = (
        f"HITL {scores.get('fm_est.hitl_count', 0.0):.2f}% "
        f"({len(hitl_entries)}/{total}) | {_format_bucket_comment(hitl_entries, max_items=6)}"
    )
    f1_comment = (
        f"F1 {scores.get('fm_est.f1_per', 0.0):.2f} | "
        f"TP {scores.get('fm_est.tp_count', 0.0):.2f} / "
        f"FP {scores.get('fm_est.fp_count', 0.0):.2f} / "
        f"FN {scores.get('fm_est.fn_count', 0.0):.2f}"
    )
    n_comment = (
        f"N={total} | TP {len(tp_entries)} | FP {len(fp_entries)} | "
        f"FN {len(fn_entries)} | HITL {len(hitl_entries)}"
    )
    return {
        'fm_N': n_comment,
        'fm_est.tp_count': tp_comment,
        'fm_est.fp_count': fp_comment,
        'fm_est.fn_count': fn_comment,
        'fm_est.hitl_count': hitl_comment,
        'fm_est.f1_per': f1_comment,
    }


def _round2(value: float) -> float:
    return round(value, 2)


def _compute_score_bundle(entries: list[EvalEntry]) -> dict[str, float]:
    tp = sum(1 for entry in entries if entry.bucket == 'TP')
    fp = sum(1 for entry in entries if entry.bucket == 'FP')
    fn = sum(1 for entry in entries if entry.bucket == 'FN')
    hitl = sum(1 for entry in entries if entry.bucket == 'HITL')
    total = tp + fp + fn + hitl
    if total <= 0:
        return {
            'fm_N': 0.0,
            'fm_est.tp_count': 0.0,
            'fm_est.fp_count': 0.0,
            'fm_est.fn_count': 0.0,
            'fm_est.hitl_count': 0.0,
            'fm_est.f1_per': 0.0,
        }

    tp_per = (tp / total) * 100.0
    fp_per = (fp / total) * 100.0
    fn_per = (fn / total) * 100.0
    hitl_per = (hitl / total) * 100.0
    denom = (2 * tp_per) + fp_per + fn_per
    f1_per = (2 * tp_per / denom) * 100.0 if denom > 0 else 0.0
    return {
        'fm_N': float(total),
        'fm_est.tp_count': _round2(tp_per),
        'fm_est.fp_count': _round2(fp_per),
        'fm_est.fn_count': _round2(fn_per),
        'fm_est.hitl_count': _round2(hitl_per),
        'fm_est.f1_per': _round2(f1_per),
    }


def _schema_hash(fields: list[dict[str, Any]]) -> str:
    payload = json.dumps(fields, ensure_ascii=False, sort_keys=True).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()[:16]


def _evaluation_metadata(
    *,
    trace: dict[str, Any],
    scores: dict[str, float],
    entries: list[EvalEntry],
    thresholds: EvalThresholds,
    embed_model_id: str,
    note_chunks: list[str],
    schema_hash_value: str,
) -> dict[str, Any]:
    grouped = {
        bucket.lower(): [asdict(entry) for entry in entries if entry.bucket == bucket]
        for bucket in ('TP', 'FP', 'FN', 'HITL')
    }
    return {
        'score_version': 'fm-est-v1',
        'trace_name': trace.get('name'),
        'trace_tag_set': trace.get('tags') or [],
        'embed_model': embed_model_id,
        'thresholds': asdict(thresholds),
        'schema_hash': schema_hash_value,
        'memo_chunk_count': len(note_chunks),
        'score_summary': scores,
        'field_breakdown': grouped,
    }


def _evaluate_trace(
    *,
    trace: dict[str, Any],
    embedder: HFEmbeddingClient,
    thresholds: EvalThresholds,
    max_chunks: int,
) -> dict[str, Any]:
    meeting_note, fields = _extract_meeting_note_and_schema(trace)
    mappings = _coerce_structured_output(trace.get('output'))

    mapping_queries: list[str] = []
    fields_by_id = {str(field.get('id')): field for field in fields}
    for mapping in mappings:
        field = _find_field(fields_by_id, mapping.get('field_id'))
        if field:
            mapping_queries.append(_mapping_query_text(field, mapping))
        else:
            mapping_queries.append(json.dumps(mapping, ensure_ascii=False))

    mapped_ranked = _rank_fields_for_queries(
        embedder=embedder,
        queries=mapping_queries,
        fields=fields,
        query_task=MAPPED_QUERY_TASK,
    ) if mapping_queries else []

    mapped_entries = _classify_mapped_outputs(
        mappings=mappings,
        fields=fields,
        ranked_results=mapped_ranked,
        thresholds=thresholds,
    )

    note_chunks = _split_meeting_note_chunks(meeting_note, max_chunks=max_chunks)
    chunk_ranked = _rank_fields_for_queries(
        embedder=embedder,
        queries=note_chunks,
        fields=fields,
        query_task=NOTE_CHUNK_QUERY_TASK,
    ) if note_chunks else []
    fn_entries = _classify_unmatched_chunks(
        note_chunks=note_chunks,
        mapped_field_ids={str(mapping.get('field_id')) for mapping in mappings},
        fields=fields,
        ranked_results=chunk_ranked,
        thresholds=thresholds,
    )

    all_entries = mapped_entries + fn_entries
    scores = _compute_score_bundle(all_entries)
    comment = _fixed_comment_template(all_entries)
    comments_by_score = _score_comments(all_entries, scores)
    metadata = _evaluation_metadata(
        trace=trace,
        scores=scores,
        entries=all_entries,
        thresholds=thresholds,
        embed_model_id=embedder.model_id,
        note_chunks=note_chunks,
        schema_hash_value=_schema_hash(fields),
    )
    return {
        'trace_id': trace.get('id'),
        'environment': trace.get('environment') or os.getenv('LANGFUSE_ENVIRONMENT') or None,
        'meeting_note_preview': _preview(meeting_note, max_len=240),
        'field_count': len(fields),
        'mapped_output_count': len(mappings),
        'memo_chunk_count': len(note_chunks),
        'scores': scores,
        'comment': comment,
        'comments_by_score': comments_by_score,
        'metadata': metadata,
        'entries': [asdict(entry) for entry in all_entries],
    }


def _existing_score_names(trace: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for item in trace.get('scores') or []:
        if isinstance(item, dict):
            name = item.get('name')
            if isinstance(name, str) and name:
                names.add(name)
    return names


def main() -> None:
    _load_env()
    args = parse_args()
    thresholds = _thresholds_from_env()
    hf_token = _require_hf_token()
    headers = _langfuse_auth_headers()
    embedder = HFEmbeddingClient(model_id=args.hf_model_id, api_token=hf_token)

    if args.trace_id:
        traces = [_fetch_trace(headers, trace_id) for trace_id in args.trace_id]
    else:
        traces = _fetch_traces(headers, tag=args.tag, limit=args.limit)

    results: list[dict[str, Any]] = []
    for trace in traces:
        if args.skip_existing and 'fm_est.f1_per' in _existing_score_names(trace):
            print(f"[SKIP] {trace.get('id')} already has fm_est.f1_per")
            continue

        trace_id = str(trace.get('id'))
        print(f'[EVAL] {trace_id}')
        evaluation = _evaluate_trace(
            trace=trace,
            embedder=embedder,
            thresholds=thresholds,
            max_chunks=args.max_chunks,
        )
        deleted_scores = []
        if args.overwrite_existing:
            deleted_scores = delete_trace_scores(
                headers=headers,
                trace_id=trace_id,
                dry_run=args.dry_run,
            )
        attach_result = attach_trace_scores(
            headers=headers,
            trace_id=trace_id,
            environment=evaluation['environment'],
            scores=evaluation['scores'],
            comment=evaluation['comment'],
            comments_by_score=evaluation['comments_by_score'],
            metadata=evaluation['metadata'],
            dry_run=args.dry_run,
        )
        results.append(
            {
                **evaluation,
                'attached': not args.dry_run,
                'deleted_existing_score_count': len(deleted_scores),
                'score_payloads': attach_result,
            }
        )
        print(
            f"[OK] {trace_id} -> N={evaluation['scores']['fm_N']} "
            f"TP={evaluation['scores']['fm_est.tp_count']} "
            f"FP={evaluation['scores']['fm_est.fp_count']} "
            f"FN={evaluation['scores']['fm_est.fn_count']} "
            f"HITL={evaluation['scores']['fm_est.hitl_count']} "
            f"F1={evaluation['scores']['fm_est.f1_per']}"
        )
        if args.sleep_sec > 0:
            time.sleep(args.sleep_sec)

    summary = {
        'trace_count': len(results),
        'dry_run': args.dry_run,
        'scores_attached': 0 if args.dry_run else sum(len(item['score_payloads']) for item in results),
        'results': results,
    }

    if args.summary_json:
        out_path = Path(args.summary_json)
        if not out_path.is_absolute():
            out_path = PROJECT_ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Wrote summary to {out_path}')

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
