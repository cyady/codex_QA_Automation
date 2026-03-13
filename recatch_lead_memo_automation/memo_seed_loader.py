from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


NOTE_COLUMN_CANDIDATES = (
    "text",
    "notes",
    "note",
    "memo",
    "comment",
    "comments",
    "메모",
    "비고",
)

DEFAULT_RENDER_FIELDS = (
    "제목",
    "회사명",
    "매출 부서",
    "이관용 담당자",
    "담당자",
    "성명",
    "직함",
    "부서",
    "이메일",
    "마감일",
    "단계",
    "금액",
    "매출 유형",
    "Vendor",
    "Create Date",
    "Deal ID",
    "제품명",
    "회차",
    "BU",
    "Status Category",
)


def normalize_header(value: str) -> str:
    return " ".join((value or "").strip().lower().replace("_", " ").split())


def compact_text(value: str, max_len: int = 80) -> str:
    cleaned = " ".join((value or "").split())
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 1].rstrip() + "…"


def normalize_note_body(value: str, max_len: int = 4500) -> str:
    text = (value or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    cleaned = "\n".join(lines).strip()
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 1].rstrip() + "…"


@dataclass(frozen=True)
class MemoSeedRecord:
    row_number: int
    source_name: str
    values: dict[str, str]
    memo_source_column: str | None


def find_note_column(fieldnames: list[str]) -> str | None:
    normalized_map = {
        normalize_header(fieldname): fieldname
        for fieldname in fieldnames
        if fieldname is not None
    }
    for candidate in NOTE_COLUMN_CANDIDATES:
        match = normalized_map.get(normalize_header(candidate))
        if match:
            return match
    return None


def render_note_text(record: MemoSeedRecord, note_index: int, run_tag: str) -> str:
    token = f"[{run_tag}-{note_index:04d}]"

    if record.memo_source_column:
        raw_note = normalize_note_body(record.values.get(record.memo_source_column, ""))
        if raw_note:
            return f"{token}\n{raw_note}"

    parts: list[str] = []
    seen_keys: set[str] = set()
    for key in DEFAULT_RENDER_FIELDS:
        if key in seen_keys:
            continue
        seen_keys.add(key)
        value = compact_text(record.values.get(key, ""))
        if value:
            parts.append(f"{key}={value}")
        if len(parts) >= 7:
            break

    if not parts:
        for key, value in record.values.items():
            if not key.strip():
                continue
            compact = compact_text(value)
            if compact:
                parts.append(f"{key}={compact}")
            if len(parts) >= 7:
                break

    summary = " | ".join(parts) if parts else "빈 행"
    return f"{token} {summary}"


def load_memo_seed_records(
    csv_path: Path,
    *,
    start_row: int = 1,
    limit: int = 0,
) -> list[MemoSeedRecord]:
    if start_row < 1:
        raise ValueError("start_row must be >= 1")
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = [fieldname or "" for fieldname in (reader.fieldnames or [])]
        memo_source_column = find_note_column(fieldnames)

        records: list[MemoSeedRecord] = []
        for row_number, row in enumerate(reader, start=1):
            if row_number < start_row:
                continue

            cleaned = {
                (key or "").strip(): (value or "").strip()
                for key, value in row.items()
                if key is not None
            }
            if not any(cleaned.values()):
                continue

            records.append(
                MemoSeedRecord(
                    row_number=row_number,
                    source_name=csv_path.name,
                    values=cleaned,
                    memo_source_column=memo_source_column,
                )
            )
            if limit > 0 and len(records) >= limit:
                break

    return records
