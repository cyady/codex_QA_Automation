# Re:catch Import Operator MCP

This folder is a dedicated workspace for the future internal MCP server.

The goal of this package is to keep the MCP-specific code, copied browser tools,
and future orchestration logic in one place without tightly coupling them to the
existing one-off automation packages.

## What Is Copied In

Current copied execution tools:

- `browser.py`
- `auth.py`
- `deal_fields.py`
- `deal_layout.py`
- `deal_import_inspect.py`
- `deal_import_run.py`
- `company_merge.py`

These were copied from:

- `recatch_deal_bulk_import`
- `recatch_company_merge`

So we can evolve MCP adapters independently.

## What Is Added Here

- `tool_catalog.py`: lightweight registry of reusable tool functions
- `job_state.py`: local job workspace paths and state persistence skeleton
- `cli.py`: simple package entrypoint for listing copied tools

## Intended Next Step

This package is not the full MCP server yet.

The next stage is:

1. extract adapter-safe functions
2. persist per-job artifacts
3. add an MCP server layer on top of these copied tools

## Quick Check

```powershell
python -m pip install -e .
recatch-import-operator-mcp list-tools
```
