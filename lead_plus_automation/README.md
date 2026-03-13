# Lead Plus Automation

`lead_plus_automation/` is a lean recovery workspace for Re:catch lead-create E2E.

This folder was restored on March 13, 2026 from repository history after confirming that the old implementation existed in GitHub history and was deleted by commit `65664d5775f6fb3a49c4cba104abd1f0fb5df284` (`Trim legacy automation experiments`, 2026-03-10). The pre-delete source snapshot used for recovery is commit `c5931777f86d8ddbc08e098fa9a7b9240850537b`.

## Scope

This recovery intentionally keeps only the parts that are still useful for E2E:

- credential-file login
- lead create modal open/select flow
- minimal field input
- create action
- list search verification
- optional drawer verification for core fields

Bulk CSV import is already maintained in `recatch_bulk_import/`, so it is not duplicated here.

## Covered fields

The default `minimal` plan targets the same practical subset that made the original automation useful:

- `title`
- `contact_email`
- `company_website`
- `amount_krw`

The optional `extended` plan also attempts:

- `contact_full_name`
- `contact_phone`

## Files

- `skeleton_vibium_flow.py`: lead-create E2E runner
- `lead_seed_loader.py`: CSV loader and typed row model
- `lead_form_selector.py`: company/contact selector step handling
- `lead_form_title.py`: required title input helper
- `recatch_auth.py`: login helper
- `data/lead_seed.csv`: small sample regression seed

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Credential file

Create `credentials/recatch_login.txt` from `credentials/recatch_login.example.txt`.

Supported formats:

```txt
email=your-email@example.com
password=your-password
```

or:

```txt
your-email@example.com
your-password
```

## Run

```bash
python skeleton_vibium_flow.py --case-id QA_DYN_001 --limit 1
```

Examples:

```bash
python skeleton_vibium_flow.py --csv data/lead_seed.csv --limit 3
python skeleton_vibium_flow.py --manual-login-fallback
python skeleton_vibium_flow.py --field-plan minimal
python skeleton_vibium_flow.py --field-plan extended
python skeleton_vibium_flow.py --skip-verify
```

## Notes

- Default URLs point to `https://test.recatch.cc/login?redirect=/leads` and `https://test.recatch.cc/leads`.
- Runtime logs are written to `logs/run-YYYYMMDD-HHMMSS.log`.
- Screenshots are written to `shot-YYYYMMDD-HHMMSS-*.png`.
- If we decide to expand this again, the next step should be adding reusable field strategies instead of re-growing a single giant script.
