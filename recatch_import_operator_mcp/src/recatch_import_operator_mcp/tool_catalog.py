from __future__ import annotations


TOOL_CATALOG = {
    "inspect_source": {
        "status": "planned",
        "notes": "Will analyze CSV/XLSX headers and generate initial metadata.",
    },
    "build_transform_plan": {
        "status": "planned",
        "notes": "Will map headers, normalize values, and identify missing fields.",
    },
    "ensure_schema": {
        "status": "copied",
        "module": "recatch_import_operator_mcp.deal_fields",
        "functions": ["load_field_specs", "create_fields"],
    },
    "verify_layout": {
        "status": "copied",
        "module": "recatch_import_operator_mcp.deal_layout",
        "functions": ["verify_fields_in_layout"],
    },
    "preview_import": {
        "status": "copied",
        "module": "recatch_import_operator_mcp.deal_import_inspect",
        "functions": ["inspect_import_page"],
    },
    "run_import": {
        "status": "copied",
        "module": "recatch_import_operator_mcp.deal_import_run",
        "functions": ["read_csv_headers", "import_csv_file"],
    },
    "merge_duplicate_companies": {
        "status": "copied",
        "module": "recatch_import_operator_mcp.company_merge",
        "functions": ["select_company_rows", "merge_company_name"],
    },
    "auth": {
        "status": "copied",
        "module": "recatch_import_operator_mcp.auth",
        "functions": ["parse_credential_file", "ensure_recatch_login"],
    },
}
