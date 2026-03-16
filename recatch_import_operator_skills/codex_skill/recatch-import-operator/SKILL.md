---
name: recatch-import-operator
description: Use when preparing or operating large Re:catch deal imports from CSV in the recatch_import_operator_skills repo, especially for non-developers. Handles env checks, source inspection, transform plans, 1000-row CSV splitting, deal field creation, preview/import, resumable batch import, and duplicate company merge preview.
---

# Re:catch Import Operator

Use this skill only inside the cloned `recatch_import_operator_skills` repo.

## Start Here

1. Confirm the repo root by locating `pyproject.toml`.
2. Run `recatch-import-operator-skills doctor` before doing any browser work.
3. For a new CSV, run:
   - `recatch-import-operator-skills inspect-source --source-csv ... --job-id ...`
   - `recatch-import-operator-skills build-transform-plan --source-csv ... --job-id ...`
   - `recatch-import-operator-skills split-source --source-csv ... --job-id ...`
4. If candidate fields are needed, run:
   - `recatch-import-operator-skills create-fields --spec-file jobs/<job_id>/artifacts/field-spec-candidates.json --no-verify-layout`
5. Before a real upload, run:
   - `recatch-import-operator-skills inspect-import`
   - `recatch-import-operator-skills import-csv --csv-file ... --preview-only`
6. Only after preview is clean, run:
   - `recatch-import-operator-skills import-csv --csv-file ...`
7. When a job already has split parts, prefer:
   - `recatch-import-operator-skills batch-import --job-id ... --preview-only`
   - `recatch-import-operator-skills batch-import --job-id ...`
8. For duplicate companies, use:
   - `recatch-import-operator-skills merge-company --company-name ... --select-count 2`
   - add `--no-preview-only` only when the user explicitly wants the final merge executed

## Rules

- Keep chunk size at `1000` rows unless the user explicitly changes it.
- Treat generated files in `jobs/<job_id>/artifacts/` as the source of truth.
- If a header is blank, duplicated, or suspicious, surface it before any import attempt.
- Do not automate Alphakey or click workspace SSO buttons such as `Recatch_alphakey(으)로 로그인`.
- Use preview import before any real upload.
- Prefer `batch-import` over ad hoc per-file loops when split-manifest.json already exists.
- Treat `merge-company` as destructive unless it stays in preview mode.
- When mapping or field existence is uncertain, use Vibium-based browser inspection as a fallback, not as the first step.
- Do not assume a custom field exists just because a CSV header exists.

## Read Next

- For setup and operator workflow: `references/repo-workflow.md`
- For `.env` and credential expectations: `references/configuration.md`
