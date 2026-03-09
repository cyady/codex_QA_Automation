# codex_QA_Automation

This repository is now focused on the Re:catch bulk import workflow.
Legacy learning scripts and diagram experiments were removed so the main branch stays aligned with the maintained automation path.

## Main Module

- `recatch_bulk_import/`
  Packaged bulk-import runner for `/leads/import`, including login helpers, probe tooling, split CSV handling, and operator runbooks.

## Supporting Workspace

- `tests/`
  Small scratch area for quick verification scripts.

## Quick Start

1. Prepare Python 3.10 or later.
2. Move into `recatch_bulk_import/`.
3. Install the package in editable mode.
4. Copy the example env or credential files before running browser automation.

```bash
pip install -e recatch_bulk_import
```

## Repository Conventions

- Credentials and local `.env` files are not committed.
- Runtime logs and screenshots stay in local output folders.
- Module-specific usage belongs in `recatch_bulk_import/README.md`.
