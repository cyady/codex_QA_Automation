# Re:catch Lead Memo Automation

`recatch_lead_memo_automation/` is a standalone Vibium utility for bulk-adding memos to a single Re:catch lead.

## Scope

- launch a fresh test browser process
- login with a credential file or manual fallback
- load memo payloads from CSV
- generate memo text when the CSV has no dedicated memo column
- post memos into a target lead page
- keep screenshots and logs as E2E artifacts

## Files

- `fill_lead_memos.py`: main CLI entrypoint
- `memo_seed_loader.py`: CSV loader and memo text renderer
- `recatch_auth.py`: lightweight Re:catch login helper
- `credentials/recatch_login.example.txt`: credential file template

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

Dry-run memo generation only:

```bash
python fill_lead_memos.py \
  --lead-url https://test.recatch.cc/leads/755915 \
  --dry-run \
  --preview-output logs/memo-preview.txt
```

Live run with credential login:

```bash
python fill_lead_memos.py \
  --lead-url https://test.recatch.cc/leads/755915 \
  --csv ../recatch_bulk_import_withUI/data/DB_Migration_Company_Part.csv \
  --count 500
```

Live run with manual login fallback:

```bash
python fill_lead_memos.py \
  --lead-url https://test.recatch.cc/leads/755915 \
  --count 500 \
  --manual-login-fallback \
  --keep-open
```

## Defaults

- default CSV: `../recatch_bulk_import_withUI/data/DB_Migration_Company_Part.csv`
- default memo count: `500`
- default run tag: `MEMO-YYYYMMDD-HHMMSS`
- screenshots: start, finish, and every `100` memos by default

## Notes

- If the CSV has a `notes`, `memo`, `메모`, or similar column, that text is reused.
- Otherwise the utility composes a compact memo from columns like `제목`, `회사명`, `매출 부서`, `단계`, `금액`, and `Deal ID`.
- `--dry-run` is useful for checking memo payload quality before touching the live page.
