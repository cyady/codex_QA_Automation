from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class JobPaths:
    job_id: str
    root: Path
    source_dir: Path
    artifacts_dir: Path
    preview_dir: Path
    logs_dir: Path
    state_file: Path


def build_job_paths(base_dir: Path, job_id: str) -> JobPaths:
    root = base_dir / job_id
    return JobPaths(
        job_id=job_id,
        root=root,
        source_dir=root / "source",
        artifacts_dir=root / "artifacts",
        preview_dir=root / "preview",
        logs_dir=root / "logs",
        state_file=root / "state.json",
    )


def ensure_job_workspace(base_dir: Path, job_id: str) -> JobPaths:
    paths = build_job_paths(base_dir, job_id)
    for directory in (
        paths.root,
        paths.source_dir,
        paths.artifacts_dir,
        paths.preview_dir,
        paths.logs_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)
    return paths


def write_job_state(paths: JobPaths, payload: dict) -> Path:
    paths.state_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return paths.state_file


def read_job_state(paths: JobPaths) -> dict:
    if not paths.state_file.exists():
        return {}
    return json.loads(paths.state_file.read_text(encoding="utf-8"))


def describe_job_paths(paths: JobPaths) -> dict:
    raw = asdict(paths)
    return {key: str(value) if isinstance(value, Path) else value for key, value in raw.items()}
