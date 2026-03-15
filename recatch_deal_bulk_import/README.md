# Re:catch Deal Bulk Import

Re:catch 딜 전용 대량 import 준비를 위한 자동화 프로젝트입니다.

현재 범위:

- 딜 데이터 필드 생성 자동화
- 레코드 타입 레이아웃 반영 여부 검증
- 딜 import 화면 요구사항 점검

현재 구현된 필드 타입:

- `text`
- `long_text`
- `date`
- `number`
- `percentage`
- `currency`
- `email`
- `phone`
- `checkbox`
- `url`
- `user`

추가 탐색이 더 필요한 타입:

- `single_select`
- `multi_select`
- `reference`

## 빠른 시작

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
Copy-Item credentials\recatch_login.example.txt credentials\recatch_login.txt
```

필드 생성:

```powershell
recatch-deal-bulk-import create-fields `
  --credential-file credentials\recatch_login.txt `
  --record-type-id 2234 `
  --spec-file specs\deal_field_matrix_example.json `
  --verify-layout
```

import 화면 점검:

```powershell
recatch-deal-bulk-import inspect-import `
  --credential-file credentials\recatch_login.txt `
  --record-type-id 2234 `
  --record-type-title "for_bulk_import_test(건들지 말것)"
```

샘플 딜 import:

```powershell
recatch-deal-bulk-import import-csv `
  --credential-file credentials\recatch_login.txt `
  --record-type-id 2234 `
  --record-type-title "for_bulk_import_test(건들지 말것)" `
  --csv-file samples\deal_import_smoke.csv
```
