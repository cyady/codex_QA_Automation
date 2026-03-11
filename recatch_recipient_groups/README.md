# recatch_recipient_groups

Re:catch QA automation package for recipient groups.

This package is separate from `recatch_bulk_import` on purpose. It provides:

- a reusable login/auth module for Re:catch
- exact-count recipient-group plan generation for `QA_DYN_0000001 ~ QA_DYN_0500000`
- static group creation automation
- dynamic group creation automation
- JSON plan execution for future reuse

Current UI automation scope:

- supported field: `리드/딜 > 제목`
- supported operators:
  - `equals`
  - `not_equals`
  - `contains`
  - `not_contains`
  - `starts_with`
  - `ends_with`
  - `is_empty`
  - `is_not_empty`

## Install

```bash
pip install -e recatch_recipient_groups
```

## Environment

Copy `.env.example` and `credentials/recatch_login.example.txt` as needed.

## Plan Format

`apply-plan` expects JSON like this:

```json
{
  "groups": [
    {
      "name": "QA_DYN_STATIC_100000",
      "kind": "static",
      "expected_count": 100000,
      "filter_rules": [
        {"field": "title", "operator": "starts_with", "value": "QA_DYN_00"},
        {"field": "title", "operator": "starts_with", "value": "QA_DYN_0100000"}
      ]
    }
  ]
}
```

## Commands

Print the exact-count plan:

```bash
recatch-recipient-groups plan-exact-groups
```

Write the plan to a file:

```bash
recatch-recipient-groups plan-exact-groups --output exact-plan.json
```

Create the default static and dynamic groups:

```bash
recatch-recipient-groups create-exact-groups
```

Apply a custom JSON plan:

```bash
recatch-recipient-groups apply-plan --plan-file exact-plan.json
```

## Notes

- The exact-count generator uses OR-ed title prefixes.
- For the intended QA dataset, it intentionally covers from `0000000` internally so the prefix set stays small. `QA_DYN_0000000` does not need to exist.
- Dynamic groups may show updated counts only after the detail page or list page refreshes.
- Static groups use the recipient picker modal and click `필터된 결과 전체 추가 (...)` after the filter rules are applied.
