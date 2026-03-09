# Bulk CSV Import Runbook

## Purpose

`bulk_csv_import_vibium.py` automates the Re:catch bulk import flow for the split CSV files under `data/lead_seed_instance_email_50000_csv_split`.

It is intended for the same workflow that was already validated in the browser:

1. Open the import page
2. Paste CSV text
3. Move to the field-mapping step
4. Search each dropdown
5. Click the dropdown option by calculated coordinates
6. Continue through validation
7. Upload
8. Confirm success

## What It Maps

The script assumes these CSV headers are present:

- `lead:deal_name`
- `contact:name`
- `contact:email`
- `company:name`

The default mapping is:

- select index `1` -> `성명`
- select index `2` -> `이메일`
- select index `3` -> `회사명`

Index `0` is expected to stay mapped to `제목`.

## Credential File

Use the existing credential file format:

```txt
email=your-email@example.com
password=your-password
```

Default path:

```txt
credentials/recatch_login.txt
```

If prod login is not handled cleanly by the credential flow, run with `--manual-login-fallback`.

## Staging Example

```bash
python bulk_csv_import_vibium.py ^
  --base-url "https://recatch-nextjs-56tswe37d-business-canvas-front-team.vercel.app" ^
  --team-slug "becan" ^
  --record-type-id 0 ^
  --start 1 ^
  --end 50 ^
  --credential-file "credentials/recatch_login.txt"
```

## Test Re:catch Example

For routes like `https://test.recatch.cc/leads`, do not pass `--team-slug`.

```bash
python bulk_csv_import_vibium.py ^
  --base-url "https://test.recatch.cc" ^
  --start 1 ^
  --end 1 ^
  --credential-file "credentials/recatch_login.txt" ^
  --manual-login-fallback ^
  --keep-open
```

## Prod Example

If prod also uses `?teamSlug=...`, pass the slug. If prod uses plain `/leads`, omit it.

```bash
python bulk_csv_import_vibium.py ^
  --base-url "https://your-prod-host.example.com" ^
  --team-slug "your-team-slug" ^
  --record-type-id 0 ^
  --start 1 ^
  --end 50 ^
  --credential-file "credentials/recatch_login.txt" ^
  --manual-login-fallback
```

## Resume After Partial Success

The script writes a progress file in `logs/` by default.

To skip parts that already succeeded:

```bash
python bulk_csv_import_vibium.py ^
  --base-url "https://your-prod-host.example.com" ^
  --team-slug "your-team-slug" ^
  --start 1 ^
  --end 50 ^
  --skip-completed
```

You can also pin the state file explicitly:

```bash
python bulk_csv_import_vibium.py ^
  --base-url "https://your-prod-host.example.com" ^
  --team-slug "your-team-slug" ^
  --state-file "logs/prod-import-state.json" ^
  --skip-completed
```

## Useful Flags

- `--headless`: run without opening the browser window
- `--keep-open`: keep the browser open after the script finishes
- `--delay-between-parts 2`: wait between files to reduce server pressure
- `--upload-timeout-sec 600`: extend the upload success wait
- `--login-url`, `--leads-url`, `--import-url`: override route construction if prod differs

## Failure Artifacts

On failure the script writes:

- log file: `logs/bulk-import-YYYYMMDD-HHMMSS.log`
- screenshot: `shot-YYYYMMDD-HHMMSS-bulk-import-error.png`

## Recommended Prod Rollout

1. Run a single file first.
2. Confirm the imported records on the prod list page.
3. Resume the rest with `--skip-completed`.

Example first-pass smoke test:

```bash
python bulk_csv_import_vibium.py ^
  --base-url "https://your-prod-host.example.com" ^
  --team-slug "your-team-slug" ^
  --start 1 ^
  --end 1 ^
  --manual-login-fallback ^
  --keep-open
```
