import json
from pathlib import Path

from recatch_recipient_groups.plans import (
    FilterRule,
    GroupKind,
    build_exact_group_specs,
    load_group_specs,
    plan_to_dict,
)


def test_filter_rule_rejects_unsupported_field() -> None:
    try:
        FilterRule(field="company", operator="starts_with", value="QA")
    except ValueError as exc:
        assert "unsupported field" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_build_exact_group_specs_names_and_counts() -> None:
    specs = build_exact_group_specs(
        counts=(100000,),
        kinds=(GroupKind.STATIC, GroupKind.DYNAMIC),
    )
    assert [spec.name for spec in specs] == [
        "QA_DYN_STATIC_100000",
        "QA_DYN_DYNAMIC_100000",
    ]
    assert specs[0].expected_count == 100000
    assert specs[0].filter_rules[0].value == "QA_DYN_00"


def test_write_and_load_plan_round_trip(tmp_path: Path) -> None:
    specs = build_exact_group_specs(counts=(150000,), kinds=(GroupKind.STATIC,))
    payload = plan_to_dict(specs)
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    loaded = load_group_specs(plan_path)
    assert len(loaded) == 1
    assert loaded[0].name == "QA_DYN_STATIC_150000"
    assert loaded[0].filter_rules[-1].value == "QA_DYN_0150000"
