# Re:catch Import Operator MCP Design

## Goal

Build an internal MCP server that can orchestrate:

1. Header analysis
2. Transform plan generation
3. Missing field detection and creation
4. Pipeline and stage validation
5. Preview generation
6. Actual import execution
7. Duplicate company merge

This is not a generic "upload any file" tool.
It is an operator-style MCP with validation and approval points.

## Why MCP Fits

The hard part is not file upload itself.
The hard part is deciding what should happen before upload:

- Which headers map to standard fields
- Which headers must become custom fields
- Which columns must be renamed or transformed
- Whether the target record type and stages are valid
- Whether imported rows will create duplicate companies
- Whether those duplicates are safe to merge

An MCP server is a better fit than a fixed UI because the agent can:

- inspect the source file
- explain the proposed changes
- ask for approval only at risky steps
- keep intermediate artifacts between steps

## Reusable Pieces Already Built

Current modules in this workspace already cover the riskiest browser operations:

- Deal field creation and import:
  - [recatch_deal_bulk_import](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import)
  - [cli.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/cli.py)
  - [fields.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/fields.py)
  - [layout.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/layout.py)
  - [import_inspect.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/import_inspect.py)
  - [import_run.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/import_run.py)

- Company duplicate merge:
  - [recatch_company_merge](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_company_merge)
  - [cli.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_company_merge/src/recatch_company_merge/cli.py)
  - [merge.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_company_merge/src/recatch_company_merge/merge.py)
  - [auth.py](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_company_merge/src/recatch_company_merge/auth.py)

These should become MCP execution adapters, not be rewritten from scratch.

## Proposed Architecture

### 1. MCP Server

One internal server, for example:

- package name: `recatch_import_operator_mcp`
- responsibility: orchestration, policy checks, artifact management

### 2. Execution Adapters

Thin wrappers over existing modules:

- `deal_import_adapter`
- `company_merge_adapter`
- `auth_adapter`

Adapters should expose stable Python functions.
The MCP layer should not depend on CLI subprocesses long term.

### 3. Job Workspace

Every import request creates a job folder:

- `jobs/<job_id>/source/`
- `jobs/<job_id>/artifacts/`
- `jobs/<job_id>/preview/`
- `jobs/<job_id>/logs/`
- `jobs/<job_id>/state.json`

This lets the agent resume safely and inspect what happened.

### 4. Policy Layer

This layer decides whether a step is:

- safe to auto-run
- needs approval
- forbidden in current environment

Examples:

- field creation in `prod`: approval required
- duplicate company merge in `prod`: approval required
- import without preview: forbidden
- merge more than 20 companies in one action: forbidden

## MCP Tool Set

### `inspect_source`

Purpose:
- Read CSV or XLSX headers
- infer target object hints
- detect obviously problematic columns

Input:

```json
{
  "file_path": "C:/data/deals.xlsx",
  "object_type": "deal",
  "record_type_id": 2234
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "headers": ["제목", "회사명", "단계", "금액"],
  "row_count": 312,
  "duplicate_headers": [],
  "empty_headers": [],
  "suspected_standard_fields": ["제목", "회사명", "단계", "금액"],
  "suspected_custom_fields": [],
  "risks": []
}
```

### `build_transform_plan`

Purpose:
- Build the normalized import shape before any mutation

Responsibilities:

- rename columns if needed
- decide standard vs custom target field
- convert date or number formats
- resolve stage column strategy
- identify required new custom fields

Input:

```json
{
  "job_id": "job_20260316_001",
  "record_type_id": 2234,
  "record_type_title": "for_bulk_import_test",
  "pipeline_id": 1422
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "normalized_headers": ["제목", "회사명", "단계", "금액", "매출 부서(원본)"],
  "field_actions": [
    {"header": "제목", "action": "map_standard", "target": "deal:title"},
    {"header": "회사명", "action": "map_standard", "target": "company:name"},
    {"header": "매출 부서", "action": "create_custom", "target": "매출 부서(원본)", "field_type": "text"}
  ],
  "transform_actions": [
    {"header": "마감일", "action": "normalize_date", "from": "2021. 12. 7", "to_format": "YYYY-MM-DD"}
  ],
  "required_field_specs": [
    {"name": "매출 부서(원본)", "type": "text", "description": "Imported from source header"}
  ],
  "risks": [
    {"code": "stage_value_check_required", "message": "단계 values must exist in target pipeline"}
  ]
}
```

### `ensure_schema`

Purpose:
- Compare transform plan against existing fields
- create only missing custom fields
- optionally verify layout presence

Input:

```json
{
  "job_id": "job_20260316_001",
  "apply": false
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "missing_fields": [
    {"name": "매출 부서(원본)", "type": "text"}
  ],
  "created_fields": [],
  "approval_required": true,
  "reason": "schema mutation requested"
}
```

If approved with `apply=true`, this tool should call the existing deal field creation flow.

### `validate_pipeline`

Purpose:
- Verify record type, pipeline, and stage values

Input:

```json
{
  "job_id": "job_20260316_001"
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "valid": true,
  "missing_stage_values": [],
  "unknown_stage_values": [],
  "pipeline_summary": {
    "record_type_id": 2234,
    "record_type_title": "for_bulk_import_test"
  }
}
```

### `preview_import`

Purpose:
- Generate the final transformed file and summarize what will happen

Input:

```json
{
  "job_id": "job_20260316_001"
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "preview_file_path": "jobs/job_20260316_001/preview/import_ready.csv",
  "sample_rows": 5,
  "expected_import_count": 312,
  "field_creations": 3,
  "stage_check_passed": true,
  "duplicate_company_candidates": [
    {"company_name": "국민대학교", "count": 2, "merge_recommended": false}
  ],
  "approval_required": true
}
```

### `run_import`

Purpose:
- Execute the actual import only after preview

Input:

```json
{
  "job_id": "job_20260316_001",
  "confirmed": true
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "ok": true,
  "imported_count": 310,
  "failed_count": 2,
  "log_file": "jobs/job_20260316_001/logs/import.log",
  "result_artifact": "jobs/job_20260316_001/artifacts/import_result.json"
}
```

### `find_duplicate_companies`

Purpose:
- Propose duplicate company groups created or touched by the import

Detection strategy for MVP:

- exact company name from imported rows
- constrained to companies touched by this job
- do not auto-merge by name alone in prod

Input:

```json
{
  "job_id": "job_20260316_001"
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "groups": [
    {
      "company_name": "test2",
      "candidate_count": 3,
      "recommended_merge_batches": [
        {"select_count": 2}
      ],
      "risk_level": "low"
    }
  ]
}
```

### `merge_duplicate_companies`

Purpose:
- Execute merge using the company merge adapter

Input:

```json
{
  "job_id": "job_20260316_001",
  "company_name": "test2",
  "select_count": 2,
  "survivor_index": 1,
  "confirmed": true
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "ok": true,
  "company_name": "test2",
  "before_visible_count": 3,
  "after_visible_count": 2,
  "log_file": "jobs/job_20260316_001/logs/company_merge.log"
}
```

### `get_job_status`

Purpose:
- Return state machine status and artifact paths for agent resume

Input:

```json
{
  "job_id": "job_20260316_001"
}
```

Output:

```json
{
  "job_id": "job_20260316_001",
  "state": "preview_ready",
  "completed_steps": ["inspect_source", "build_transform_plan", "validate_pipeline"],
  "pending_steps": ["run_import", "find_duplicate_companies"],
  "artifacts": {
    "transform_plan": "jobs/job_20260316_001/artifacts/transform_plan.json",
    "preview_file": "jobs/job_20260316_001/preview/import_ready.csv"
  }
}
```

## End-to-End MCP Sequence

Normal deal import flow:

1. `inspect_source`
2. `build_transform_plan`
3. `ensure_schema`
4. `validate_pipeline`
5. `preview_import`
6. human approval
7. `run_import`
8. `find_duplicate_companies`
9. human approval
10. `merge_duplicate_companies`

## Approval Gates

Approval is required for:

- creating missing custom fields
- modifying layout if ever enabled
- running real import outside a test environment
- merging duplicate companies

Approval should not be required for:

- reading headers
- generating transform plans
- validating pipeline stages
- producing preview artifacts

## MVP Scope

Recommended first release:

- object type: `deal` only
- source file: `csv` first, `xlsx` second
- one record type per job
- exact-match company dedupe only for imported company names
- manual approval before any mutation
- company merge limited to 2-20 selected rows

## Non-Goals for MVP

Do not include these in the first version:

- freeform dedupe across the whole database
- automatic merge by fuzzy company similarity
- lead and deal in the same job
- automatic pipeline creation
- automatic deleted-field cleanup

## Mapping to Current Code

Suggested adapter mapping:

- `ensure_schema`
  - wrap [create_fields](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/fields.py)
  - wrap [verify_fields_in_layout](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/layout.py)

- `preview_import`
  - wrap [inspect_import_page](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/import_inspect.py)
  - add transformed CSV artifact generation before upload

- `run_import`
  - wrap [import_csv_file](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_deal_bulk_import/src/recatch_deal_bulk_import/import_run.py)

- `merge_duplicate_companies`
  - wrap [merge_company_name](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_company_merge/src/recatch_company_merge/merge.py)

- auth
  - reuse [ensure_recatch_login](C:/Users/cyady/Desktop/project/QA/QA_tutorial/Codex/codex_QA_Automation/recatch_company_merge/src/recatch_company_merge/auth.py)

## Recommended Next Implementation Steps

1. Extract pure-Python adapters from the existing CLI entrypoints.
2. Add a job-state model and local artifact persistence.
3. Implement the first four MCP tools:
   - `inspect_source`
   - `build_transform_plan`
   - `ensure_schema`
   - `preview_import`
4. Add `run_import` only after preview artifacts are stable.
5. Add `find_duplicate_companies` and `merge_duplicate_companies` last.

## Bottom Line

This is feasible now.

The safest shape is:

- agent decides
- MCP validates
- human approves mutations
- adapters execute the risky browser work

That gives us a realistic internal operator, not a brittle one-click uploader.
