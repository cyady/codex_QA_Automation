# codex_QA_Automation

Re:catch QA automation scripts, operators' runbooks, and supporting datasets live in this workspace.
The directory is organized as a small toolbox rather than a single package, so each module documents its own install and runtime details.

## Modules

- `lead_plus_automation/`
  Vibium-based lead creation and field-input automation with CSV fixtures and runbooks.
- `recatch_bulk_import/`
  Packaged bulk-import runner for `/leads/import`, including login helpers, probe tooling, and split CSV samples.
- `recatch_mermaid/`
  Mermaid diagrams and API flow notes used to explain the Re:catch QA flow.
- `tests/`
  Shared scratch area for quick verification scripts.

## Quick Start

1. Prepare Python 3.10 or later.
2. Move into the module you want to run.
3. Install that module's dependencies.
4. Copy example env or credential files before running any browser automation.

Examples:

```bash
pip install -r lead_plus_automation/requirements.txt
pip install -e recatch_bulk_import
```

## Repository Conventions

- Credentials and local `.env` files are not committed.
- Runtime logs and screenshots stay inside each module's local output folders.
- Module-specific usage belongs in the module README, while this file only serves as an index.
