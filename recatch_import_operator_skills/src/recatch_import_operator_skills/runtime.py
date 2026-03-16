from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parse_env_file(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def load_env_file(raw_path: str | None) -> Path | None:
    candidate: Path | None = None
    if raw_path:
        candidate = resolve_path(Path.cwd(), raw_path)
        if not candidate.exists():
            raise FileNotFoundError(f"env file not found: {candidate}")
    else:
        env_override = os.getenv("RECATCH_ENV_FILE", "").strip()
        if env_override:
            candidate = resolve_path(Path.cwd(), env_override)
            if not candidate.exists():
                raise FileNotFoundError(f"env file not found: {candidate}")
        else:
            default_env = (PROJECT_ROOT / ".env").resolve()
            if default_env.exists():
                candidate = default_env

    if candidate is None:
        return None

    for key, value in parse_env_file(candidate).items():
        os.environ.setdefault(key, value)
    return candidate


def resolve_path(base_dir: Path, raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (base_dir / candidate).resolve()


def env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return int(raw)


def env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return float(raw)


def env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "y"}


def sanitize_token(raw_value: str) -> str:
    sanitized = []
    for ch in raw_value.strip():
        if ch.isalnum() or ch in {"-", "_"}:
            sanitized.append(ch)
        else:
            sanitized.append("_")
    token = "".join(sanitized).strip("_")
    return token or "job"
