from __future__ import annotations

import argparse
import json
from typing import Sequence

from .tool_catalog import TOOL_CATALOG


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Utility entrypoint for the Re:catch import operator MCP workspace."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list-tools", help="list copied execution tools and future MCP targets")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list-tools":
        print(json.dumps(TOOL_CATALOG, ensure_ascii=False, indent=2))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
