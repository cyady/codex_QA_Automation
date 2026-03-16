# Repo Workflow

## Recommended order

1. `recatch-import-operator-skills doctor`
2. `recatch-import-operator-skills inspect-source --source-csv ... --job-id ...`
3. `recatch-import-operator-skills build-transform-plan --source-csv ... --job-id ...`
4. Review:
   - `jobs/<job_id>/artifacts/source-summary.json`
   - `jobs/<job_id>/artifacts/mapping-template.json`
   - `jobs/<job_id>/artifacts/field-spec-candidates.json`
5. `recatch-import-operator-skills split-source --source-csv ... --job-id ...`
6. If custom fields are needed, run `recatch-import-operator-skills create-fields --spec-file jobs/<job_id>/artifacts/field-spec-candidates.json --no-verify-layout`
7. `recatch-import-operator-skills inspect-import`
8. `recatch-import-operator-skills import-csv --csv-file ... --preview-only`
9. If preview is clean, `recatch-import-operator-skills import-csv --csv-file ...`
10. If the job already has split-manifest.json, prefer `recatch-import-operator-skills batch-import --job-id ... --preview-only`
11. For a real full run, use `recatch-import-operator-skills batch-import --job-id ...`
12. For duplicate companies, first run `recatch-import-operator-skills merge-company --company-name ... --select-count 2`
13. Only use `--no-preview-only` for company merge when the user explicitly approves the destructive action.
14. If direct header mapping fails in the browser, probe the exact dropdown option with Vibium and update the mapping artifact.

## Artifact meanings

- `source-summary.json`: row count, headers, sample rows, chunk recommendation
- `mapping-template.json`: initial CSV-header to Re:catch-field suggestion file
- `field-spec-candidates.json`: candidate deal custom fields inferred from source headers
- `split-manifest.json`: generated part files for sequential import
- `batch-import-state.json`: completed part numbers for resumable batch upload
- `state.json`: latest job-level state pointer

## Large import rule

- Re:catch bulk import max is `1000` rows per run.
- A `40,000` to `50,000` row file should normally produce `40` to `50` chunk files.

## Browser fallback

- Use Vibium when a suggested mapping is not found in the dropdown.
- Prefer exact option text over fuzzy matching.
- Keep any confirmed option text in the mapping artifact so later runs are deterministic.
