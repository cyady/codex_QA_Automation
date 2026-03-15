# Re:catch Company Merge

Automates duplicate company merge flows in Re:catch.

Current scope:

- Navigate to the company list with `teamSlug`
- Search a duplicate company name
- Select matching row checkboxes only
- Complete the two-step merge modal
- Verify the visible result count decreased after merge

## Quick Start

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
Copy-Item credentials\recatch_login.example.txt credentials\recatch_login.txt
```

## Example

```powershell
recatch-company-merge merge-name `
  --base-url https://recatch-nextjs-bczu3ipum-business-canvas-front-team.vercel.app `
  --credential-file credentials\recatch_login.txt `
  --team-slug becan `
  --company-name test2 `
  --select-count 2 `
  --survivor-index 1
```
