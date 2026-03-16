from __future__ import annotations

import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILL_DIR = REPO_ROOT / "codex_skill" / "recatch-import-operator"
TARGET_SKILL_DIR = Path.home() / ".codex" / "skills" / "recatch-import-operator"


def main() -> int:
    if not SOURCE_SKILL_DIR.exists():
        raise FileNotFoundError(f"skill source not found: {SOURCE_SKILL_DIR}")

    TARGET_SKILL_DIR.parent.mkdir(parents=True, exist_ok=True)
    if TARGET_SKILL_DIR.exists():
        shutil.rmtree(TARGET_SKILL_DIR)
    shutil.copytree(SOURCE_SKILL_DIR, TARGET_SKILL_DIR)

    print(f"installed skill: {TARGET_SKILL_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
