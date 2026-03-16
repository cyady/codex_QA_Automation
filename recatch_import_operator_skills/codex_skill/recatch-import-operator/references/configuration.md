# Configuration

## Files

- `.env`: repo-level defaults for target Re:catch environment and source CSV path
- `credentials/recatch_login.txt`: login credential file

## Required `.env` keys

- `RECATCH_BASE_URL`
- `RECATCH_RECORD_TYPE_ID`
- `RECATCH_RECORD_TYPE_TITLE`
- `RECATCH_CREDENTIAL_FILE`

## Useful optional keys

- `RECATCH_SOURCE_CSV`
- `RECATCH_JOB_DIR`
- `RECATCH_MAX_ROWS_PER_IMPORT`
- `RECATCH_HEADLESS`
- `RECATCH_KEEP_OPEN`
- `RECATCH_UPLOAD_TIMEOUT_SEC`

## Credential format

Either of the formats below is valid:

```txt
email=user@example.com
password=secret
```

or:

```txt
user@example.com
secret
```

## Login boundary

- This repo only automates the Re:catch email/password login form.
- If the browser shows a workspace SSO button such as `Recatch_alphakey(으)로 로그인`, the automation must stop instead of clicking through.
- External Alphakey login is intentionally out of scope.

## Path rules

- Relative paths are resolved from the `.env` file directory when an env file is loaded.
- CSV paths with spaces must be shell-quoted.
