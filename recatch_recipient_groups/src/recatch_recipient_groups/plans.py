from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterable

from .prefixes import build_exact_size_title_prefixes


DEFAULT_COUNTS = (
    100000,
    150000,
    200000,
    230000,
    250000,
    300000,
    350000,
    400000,
    450000,
    500000,
)
TITLE_OPERATORS = {
    "equals",
    "not_equals",
    "contains",
    "not_contains",
    "starts_with",
    "ends_with",
    "is_empty",
    "is_not_empty",
}
VALUE_REQUIRED_OPERATORS = TITLE_OPERATORS - {"is_empty", "is_not_empty"}


class GroupKind(str, Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"


@dataclass(frozen=True)
class FilterRule:
    field: str
    operator: str
    value: str | None = None

    def __post_init__(self) -> None:
        if self.field != "title":
            raise ValueError(f"unsupported field: {self.field}")
        if self.operator not in TITLE_OPERATORS:
            raise ValueError(f"unsupported operator: {self.operator}")
        if self.operator in VALUE_REQUIRED_OPERATORS and not self.value:
            raise ValueError(f"operator requires value: {self.operator}")
        if self.operator not in VALUE_REQUIRED_OPERATORS and self.value not in (None, ""):
            raise ValueError(f"operator does not accept value: {self.operator}")

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "field": self.field,
            "operator": self.operator,
        }
        if self.value is not None:
            payload["value"] = self.value
        return payload


@dataclass(frozen=True)
class GroupSpec:
    name: str
    kind: GroupKind
    filter_rules: tuple[FilterRule, ...]
    expected_count: int | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("group name must not be blank")
        if not self.filter_rules:
            raise ValueError("group must have at least one filter rule")

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "name": self.name,
            "kind": self.kind.value,
            "filter_rules": [rule.to_dict() for rule in self.filter_rules],
        }
        if self.expected_count is not None:
            payload["expected_count"] = self.expected_count
        return payload


def normalize_group_kinds(values: Iterable[str]) -> tuple[GroupKind, ...]:
    kinds: list[GroupKind] = []
    for value in values:
        normalized = value.strip().lower()
        if not normalized:
            continue
        kinds.append(GroupKind(normalized))
    if not kinds:
        raise ValueError("at least one group kind is required")
    return tuple(dict.fromkeys(kinds))


def build_exact_group_specs(
    *,
    counts: Iterable[int] = DEFAULT_COUNTS,
    kinds: Iterable[GroupKind] = (GroupKind.STATIC, GroupKind.DYNAMIC),
    title_prefix: str = "QA_DYN_",
    number_width: int = 7,
    name_prefix: str = "QA_DYN",
) -> list[GroupSpec]:
    specs: list[GroupSpec] = []
    normalized_kinds = tuple(kinds)
    for count in counts:
        prefixes = build_exact_size_title_prefixes(
            count=count,
            title_prefix=title_prefix,
            number_width=number_width,
        )
        rules = tuple(
            FilterRule(field="title", operator="starts_with", value=prefix)
            for prefix in prefixes
        )
        for kind in normalized_kinds:
            specs.append(
                GroupSpec(
                    name=f"{name_prefix}_{kind.value.upper()}_{count}",
                    kind=kind,
                    filter_rules=rules,
                    expected_count=count,
                )
            )
    return specs


def plan_to_dict(specs: Iterable[GroupSpec]) -> dict[str, Any]:
    return {"groups": [spec.to_dict() for spec in specs]}


def write_plan(path: Path, specs: Iterable[GroupSpec]) -> Path:
    payload = plan_to_dict(specs)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_group_specs(path: Path) -> list[GroupSpec]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_groups = payload["groups"] if isinstance(payload, dict) else payload
    specs: list[GroupSpec] = []
    for raw_group in raw_groups:
        raw_rules = raw_group.get("filter_rules", [])
        rules = tuple(
            FilterRule(
                field=str(raw_rule.get("field", "title")),
                operator=str(raw_rule["operator"]),
                value=raw_rule.get("value"),
            )
            for raw_rule in raw_rules
        )
        specs.append(
            GroupSpec(
                name=str(raw_group["name"]),
                kind=GroupKind(str(raw_group["kind"]).lower()),
                filter_rules=rules,
                expected_count=raw_group.get("expected_count"),
            )
        )
    return specs
