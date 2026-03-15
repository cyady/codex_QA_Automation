from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import pytest

from recatch_bulk_import.cli import prepare_part_jobs_and_mappings, read_csv_headers


def write_csv(path: Path, headers: list[str], row: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerow(row)


def make_args(tmp_path: Path, **overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "source_csv": "",
        "csv_dir": str(tmp_path / "csv_split"),
        "file_prefix": "part_",
        "mapping_file": "",
        "prompt_mapping": False,
        "start": 1,
        "end": 0,
        "split_size": 1000,
        "team_slug": "",
        "log_dir": str(tmp_path / "logs"),
        "state_file": "",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_read_csv_headers_rejects_duplicate_headers(tmp_path: Path) -> None:
    csv_path = tmp_path / "duplicate.csv"
    write_csv(csv_path, ["lead:deal_name", "contact:name", "contact:name"], ["a", "b", "c"])

    with pytest.raises(ValueError, match="duplicates"):
        read_csv_headers(csv_path)


def test_prepare_part_jobs_and_mappings_rejects_mismatched_split_headers(tmp_path: Path) -> None:
    csv_dir = tmp_path / "csv_split"
    write_csv(
        csv_dir / "part_001.csv",
        ["lead:deal_name", "contact:name", "contact:email", "company:name"],
        ["deal-1", "tester", "qa@example.com", "qa-company"],
    )
    write_csv(
        csv_dir / "part_002.csv",
        ["lead:deal_name", "contact:name", "contact:email", "custom:extra"],
        ["deal-2", "tester", "qa@example.com", "value"],
    )

    args = make_args(tmp_path)

    with pytest.raises(ValueError, match="headers changed at part 002"):
        prepare_part_jobs_and_mappings(args, "https://test.recatch.cc", tmp_path / "logs")


def test_prepare_part_jobs_and_mappings_supports_large_header_counts(tmp_path: Path) -> None:
    headers = [
        "lead:deal_name",
        "contact:name",
        "contact:email",
        "company:name",
        *[f"custom:text:{index:03d}" for index in range(1, 117)],
    ]
    row = ["deal", "tester", "qa@example.com", "qa-company", *[f"value-{index:03d}" for index in range(1, 117)]]
    source_csv = tmp_path / "source.csv"
    write_csv(source_csv, headers, row)

    mapping_path = tmp_path / "mappings.json"
    mapping_path.write_text(
        json.dumps(
            {
                "columns": [
                    {
                        "csv_header": headers[-1],
                        "query": "텍스트",
                        "option_text": "텍스트 9",
                    }
                ]
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    args = make_args(
        tmp_path,
        source_csv=str(source_csv),
        csv_dir=str(tmp_path / "generated"),
        file_prefix="large_part_",
        mapping_file=str(mapping_path),
    )
    prepared = prepare_part_jobs_and_mappings(args, "https://test.recatch.cc", tmp_path / "logs")

    assert len(prepared["headers"]) == 120
    assert len(prepared["part_jobs"]) == 1
    assert prepared["mappings"][0].select_index == 119
    assert prepared["mappings"][0].name == headers[-1]
