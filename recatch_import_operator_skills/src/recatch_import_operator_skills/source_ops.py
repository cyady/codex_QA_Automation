from __future__ import annotations

import csv
import datetime as dt
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable

from .job_state import JobPaths, describe_job_paths, ensure_job_workspace, write_job_state
from .runtime import sanitize_token


REQUIRED_DEAL_HEADERS = {"제목", "단계"}
LIKELY_NATIVE_HEADERS = {
    "제목",
    "단계",
    "마감일",
    "회사명",
    "성명",
    "직함",
    "부서",
    "이메일",
    "금액",
    "담당자",
}
BOOLEAN_TRUE_VALUES = {"true", "yes", "y", "1", "예", "o", "v"}
BOOLEAN_FALSE_VALUES = {"false", "no", "n", "0", "아니오", "x"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
INTEGER_RE = re.compile(r"^-?\d+$")
DECIMAL_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
DATE_RE = re.compile(r"^\d{4}[./-]\s?\d{1,2}(?:[./-]\s?\d{1,2})?$")
DATE_HEADER_HINTS = ("date", "일", "마감", "생성", "create")
EMAIL_HEADER_HINTS = ("email", "메일")
URL_HEADER_HINTS = ("url", "link", "링크")
CURRENCY_HEADER_HINTS = ("금액", "매출액", "amount", "price")
PERCENTAGE_HEADER_HINTS = ("%", "rate", "ratio", "비율")


def infer_field_type(header: str, samples: Iterable[str]) -> str:
    normalized_header = header.strip().lower()
    non_blank_samples = [value.strip() for value in samples if value and value.strip()]
    if any(token in normalized_header for token in PERCENTAGE_HEADER_HINTS):
        return "percentage"
    if any(token in normalized_header for token in EMAIL_HEADER_HINTS):
        return "email"
    if any(token in normalized_header for token in URL_HEADER_HINTS):
        return "url"
    if any(token in normalized_header for token in DATE_HEADER_HINTS):
        return "date"
    if any(token in normalized_header for token in CURRENCY_HEADER_HINTS):
        return "currency"
    if not non_blank_samples:
        return "text"
    lowered = {value.lower() for value in non_blank_samples}
    if lowered and lowered.issubset(BOOLEAN_TRUE_VALUES | BOOLEAN_FALSE_VALUES):
        return "checkbox"
    if all(EMAIL_RE.match(value) for value in non_blank_samples):
        return "email"
    if all(URL_RE.match(value) for value in non_blank_samples):
        return "url"
    if all(DATE_RE.match(value) for value in non_blank_samples):
        return "date"
    numeric_samples = [value.replace(",", "") for value in non_blank_samples]
    if all(INTEGER_RE.match(value) for value in numeric_samples):
        return "number"
    if all(DECIMAL_RE.match(value) for value in numeric_samples):
        return "number"
    if max(len(value) for value in non_blank_samples) >= 120:
        return "long_text"
    return "text"


def build_default_job_id(source_csv_path: Path) -> str:
    token = sanitize_token(source_csv_path.stem)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{token}-{timestamp}"


def ensure_operator_job(job_dir: Path, source_csv_path: Path, job_id: str | None) -> JobPaths:
    resolved_job_id = job_id or build_default_job_id(source_csv_path)
    return ensure_job_workspace(job_dir, resolved_job_id)


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _row_preview(header: list[str], row: list[str]) -> dict[str, Any]:
    columns = []
    for index, header_name in enumerate(header, start=1):
        value = row[index - 1] if index - 1 < len(row) else ""
        columns.append(
            {
                "index": index,
                "header": header_name.strip(),
                "value": value,
            }
        )
    if len(row) > len(header):
        for index in range(len(header) + 1, len(row) + 1):
            columns.append(
                {
                    "index": index,
                    "header": "",
                    "value": row[index - 1],
                }
            )
    return {"columns": columns}


def inspect_source_csv(
    source_csv_path: Path,
    *,
    sample_rows: int = 3,
    rows_per_part: int = 1000,
) -> dict[str, Any]:
    if rows_per_part < 1:
        raise ValueError(f"rows_per_part must be >= 1: {rows_per_part}")

    header_samples: list[list[str]] = []
    row_previews: list[dict[str, Any]] = []
    inconsistent_rows: list[dict[str, int]] = []

    with source_csv_path.open("r", encoding="utf-8-sig", newline="") as source_file:
        reader = csv.reader(source_file)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"csv file is empty: {source_csv_path}") from exc

        normalized_headers = [value.strip() for value in header]
        if not any(normalized_headers):
            raise ValueError(f"csv header is empty: {source_csv_path}")

        header_samples = [[] for _ in normalized_headers]
        row_count = 0
        for row_number, row in enumerate(reader, start=2):
            if not any(cell.strip() for cell in row):
                continue
            row_count += 1
            if len(row_previews) < sample_rows:
                preview = _row_preview(normalized_headers, row)
                preview["rowNumber"] = row_number
                row_previews.append(preview)
            if len(row) != len(normalized_headers) and len(inconsistent_rows) < 20:
                inconsistent_rows.append(
                    {
                        "rowNumber": row_number,
                        "columnCount": len(row),
                    }
                )
            for index, value in enumerate(row[: len(normalized_headers)]):
                trimmed = value.strip()
                if trimmed and len(header_samples[index]) < 20:
                    header_samples[index].append(trimmed)

    seen: set[str] = set()
    duplicate_headers: list[str] = []
    for header_name in normalized_headers:
        if not header_name:
            continue
        if header_name in seen and header_name not in duplicate_headers:
            duplicate_headers.append(header_name)
        seen.add(header_name)

    blank_headers = [
        {"index": index, "header": header_name}
        for index, header_name in enumerate(normalized_headers, start=1)
        if not header_name
    ]
    part_count = math.ceil(row_count / rows_per_part) if row_count else 0
    estimated_last_part_row_count = row_count % rows_per_part or (rows_per_part if row_count else 0)
    warnings: list[str] = []
    if blank_headers:
        warnings.append(f"blank headers detected at columns {[item['index'] for item in blank_headers]}")
    if duplicate_headers:
        warnings.append(f"duplicate headers detected: {duplicate_headers}")
    if inconsistent_rows:
        warnings.append("some rows do not match the header column count")

    return {
        "ok": True,
        "sourceCsv": str(source_csv_path),
        "fileName": source_csv_path.name,
        "rowCount": row_count,
        "columnCount": len(normalized_headers),
        "rowsPerPart": rows_per_part,
        "recommendedPartCount": part_count,
        "estimatedLastPartRowCount": estimated_last_part_row_count,
        "headers": normalized_headers,
        "blankHeaders": blank_headers,
        "duplicateHeaders": duplicate_headers,
        "sampleRows": row_previews,
        "columnSamples": [
            {
                "index": index,
                "header": header_name,
                "samples": header_samples[index - 1],
            }
            for index, header_name in enumerate(normalized_headers, start=1)
        ],
        "inconsistentRows": inconsistent_rows,
        "warnings": warnings,
    }


def build_transform_plan(
    source_csv_path: Path,
    *,
    rows_per_part: int = 1000,
) -> dict[str, Any]:
    summary = inspect_source_csv(source_csv_path, sample_rows=3, rows_per_part=rows_per_part)
    mapping_template: list[dict[str, Any]] = []
    candidate_fields: list[dict[str, Any]] = []

    for column in summary["columnSamples"]:
        header_name = str(column["header"]).strip()
        column_index = int(column["index"])
        samples = list(column["samples"])
        if not header_name:
            mapping_template.append(
                {
                    "csv_header": "",
                    "column_index": column_index,
                    "query": "",
                    "option_text": "",
                    "skip": True,
                    "reason": "blank_header",
                }
            )
            continue

        mapping_template.append(
            {
                "csv_header": header_name,
                "column_index": column_index,
                "query": header_name,
                "option_text": header_name,
                "skip": False,
                "reason": (
                    "required_deal_header"
                    if header_name in REQUIRED_DEAL_HEADERS
                    else "direct_name_match_candidate"
                ),
            }
        )

        if header_name in LIKELY_NATIVE_HEADERS:
            continue

        candidate_fields.append(
            {
                "name": header_name,
                "field_type": infer_field_type(header_name, samples),
                "description": f"Auto-generated candidate from CSV header '{header_name}'",
                "help_text": "",
                "source_header": header_name,
                "sample_values": samples[:5],
                "confidence": "low",
            }
        )

    warnings = list(summary["warnings"])
    if not REQUIRED_DEAL_HEADERS.issubset(set(summary["headers"])):
        warnings.append("required deal headers '제목' and '단계' must exist before import")

    return {
        "ok": True,
        "sourceCsv": str(source_csv_path),
        "rowsPerPart": rows_per_part,
        "requiredHeaders": sorted(REQUIRED_DEAL_HEADERS),
        "likelyNativeHeaders": sorted(LIKELY_NATIVE_HEADERS),
        "mappingTemplate": mapping_template,
        "candidateFieldSpecs": candidate_fields,
        "warnings": warnings,
        "summary": summary,
    }


def split_source_csv(
    source_csv_path: Path,
    output_dir: Path,
    *,
    rows_per_part: int = 1000,
    file_prefix: str | None = None,
) -> dict[str, Any]:
    if rows_per_part < 1:
        raise ValueError(f"rows_per_part must be >= 1: {rows_per_part}")

    output_dir.mkdir(parents=True, exist_ok=True)
    normalized_prefix = file_prefix or f"{sanitize_token(source_csv_path.stem)}_part_"
    part_paths: list[Path] = []

    with source_csv_path.open("r", encoding="utf-8-sig", newline="") as src_file:
        reader = csv.reader(src_file)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError(f"csv file is empty: {source_csv_path}") from exc

        part_number = 0
        rows: list[list[str]] = []
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            rows.append(row)
            if len(rows) >= rows_per_part:
                part_number += 1
                part_paths.append(_write_split_csv(output_dir, normalized_prefix, part_number, header, rows))
                rows = []

        if rows or part_number == 0:
            part_number += 1
            part_paths.append(_write_split_csv(output_dir, normalized_prefix, part_number, header, rows))

    return {
        "ok": True,
        "sourceCsv": str(source_csv_path),
        "outputDir": str(output_dir),
        "filePrefix": normalized_prefix,
        "rowsPerPart": rows_per_part,
        "parts": [
            {
                "partNumber": index,
                "file": str(path),
            }
            for index, path in enumerate(part_paths, start=1)
        ],
        "partCount": len(part_paths),
    }


def persist_inspection_artifacts(paths: JobPaths, payload: dict[str, Any]) -> dict[str, str]:
    summary_path = write_json(paths.artifacts_dir / "source-summary.json", payload)
    write_job_state(
        paths,
        {
            "operation": "inspect-source",
            "sourceCsv": payload["sourceCsv"],
            "summaryPath": str(summary_path),
            "jobPaths": describe_job_paths(paths),
        },
    )
    return {
        "summary": str(summary_path),
        "state": str(paths.state_file),
    }


def persist_transform_plan_artifacts(paths: JobPaths, payload: dict[str, Any]) -> dict[str, str]:
    plan_path = write_json(paths.artifacts_dir / "transform-plan.json", payload)
    mapping_path = write_json(paths.artifacts_dir / "mapping-template.json", {"columns": payload["mappingTemplate"]})
    field_spec_path = write_json(paths.artifacts_dir / "field-spec-candidates.json", {"fields": payload["candidateFieldSpecs"]})
    write_job_state(
        paths,
        {
            "operation": "build-transform-plan",
            "sourceCsv": payload["sourceCsv"],
            "planPath": str(plan_path),
            "mappingPath": str(mapping_path),
            "fieldSpecPath": str(field_spec_path),
            "jobPaths": describe_job_paths(paths),
        },
    )
    return {
        "plan": str(plan_path),
        "mappingTemplate": str(mapping_path),
        "fieldSpecCandidates": str(field_spec_path),
        "state": str(paths.state_file),
    }


def persist_split_artifacts(paths: JobPaths, payload: dict[str, Any]) -> dict[str, str]:
    manifest_path = write_json(paths.artifacts_dir / "split-manifest.json", payload)
    write_job_state(
        paths,
        {
            "operation": "split-source",
            "sourceCsv": payload["sourceCsv"],
            "manifestPath": str(manifest_path),
            "jobPaths": describe_job_paths(paths),
        },
    )
    return {
        "manifest": str(manifest_path),
        "state": str(paths.state_file),
    }


def _write_split_csv(
    output_dir: Path,
    file_prefix: str,
    part_number: int,
    header: list[str],
    rows: list[list[str]],
) -> Path:
    part_path = output_dir / f"{file_prefix}{part_number:03d}.csv"
    with part_path.open("w", encoding="utf-8", newline="") as dst_file:
        writer = csv.writer(dst_file)
        writer.writerow(header)
        writer.writerows(rows)
    return part_path
