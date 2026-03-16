from __future__ import annotations


TOOL_CATALOG = {
    "doctor": {
        "status": "implemented",
        "module": "recatch_import_operator_skills.cli",
        "commands": ["doctor"],
        "notes": "Checks env values and credential file resolution before browser work starts.",
    },
    "inspect_source": {
        "status": "implemented",
        "module": "recatch_import_operator_skills.source_ops",
        "functions": ["inspect_source_csv"],
        "commands": ["inspect-source"],
        "notes": "Analyzes CSV headers, row count, sample rows, and 1000-row chunk recommendations.",
    },
    "build_transform_plan": {
        "status": "implemented",
        "module": "recatch_import_operator_skills.source_ops",
        "functions": ["build_transform_plan"],
        "commands": ["build-transform-plan"],
        "notes": "Generates mapping templates and candidate deal field specs from source headers.",
    },
    "split_source": {
        "status": "implemented",
        "module": "recatch_import_operator_skills.source_ops",
        "functions": ["split_source_csv"],
        "commands": ["split-source"],
        "notes": "Splits large source CSV files into 1000-row parts for sequential import.",
    },
    "batch_import": {
        "status": "implemented",
        "module": "recatch_import_operator_skills.cli",
        "commands": ["batch-import"],
        "notes": "Runs every part from split-manifest.json with resumable state tracking.",
    },
    "ensure_schema": {
        "status": "copied",
        "module": "recatch_import_operator_skills.deal_fields",
        "functions": ["load_field_specs", "create_fields"],
    },
    "verify_layout": {
        "status": "copied",
        "module": "recatch_import_operator_skills.deal_layout",
        "functions": ["verify_fields_in_layout"],
    },
    "preview_import": {
        "status": "copied",
        "module": "recatch_import_operator_skills.deal_import_inspect",
        "functions": ["inspect_import_page"],
    },
    "run_import": {
        "status": "copied",
        "module": "recatch_import_operator_skills.deal_import_run",
        "functions": ["read_csv_headers", "import_csv_file"],
    },
    "merge_duplicate_companies": {
        "status": "implemented",
        "module": "recatch_import_operator_skills.company_merge",
        "functions": ["select_company_rows", "merge_company_name"],
        "commands": ["merge-company"],
    },
    "auth": {
        "status": "copied",
        "module": "recatch_import_operator_skills.auth",
        "functions": ["parse_credential_file", "ensure_recatch_login"],
    },
}
