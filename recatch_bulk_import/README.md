# Re:catch Bulk Import

QA 팀이 공용으로 사용할 수 있게 분리한 Re:catch 리드 대량 임포트 프로젝트입니다.

이 프로젝트는 아래 흐름을 자동화합니다.

1. 로그인
2. 원본 CSV 자동 분할 또는 기존 분할 CSV 로드
3. `/leads/import` 진입
4. CSV 붙여넣기
5. 필드 매핑
6. 검증 통과
7. 업로드
8. 완료 파트 상태 저장

## 요구사항

- Python 3.10+
- 데스크탑 환경에서 Vibium 실행 가능

## 빠른 시작

### Windows PowerShell

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
Copy-Item .env.test.example .env.test
Copy-Item credentials\recatch_login.example.txt credentials\recatch_login.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
cp .env.test.example .env.test
cp credentials/recatch_login.example.txt credentials/recatch_login.txt
```

## 권장 실행 흐름

1. 사용자가 원본 CSV 1개를 준비합니다.
2. `.env` 또는 CLI 인자에 `RECATCH_SOURCE_CSV`, `RECATCH_SPLIT_SIZE`를 설정합니다.
3. 필요하면 `RECATCH_PROMPT_MAPPING=true` 또는 `--prompt-mapping` 으로 각 열의 매핑을 입력합니다.
4. CLI가 CSV를 자동으로 분할하고, 생성된 파트를 순서대로 임포트합니다.
5. 실행 로그에 `[part 1/50]`, `[part 2/50]` 형태로 진행 상황이 남습니다.

`RECATCH_SOURCE_CSV`를 비워두면 기존처럼 `data/csv_split/` 안의 분할 CSV를 그대로 사용합니다.

## 기본 폴더

- `data/`: 원본 CSV 및 분할 CSV 위치
- `credentials/`: 로그인 정보 파일 위치
- `logs/`: 실행 로그, 상태 파일
- `screenshots/`: 실패 스크린샷

기본 원본 CSV는 `.env`에서 `RECATCH_SOURCE_CSV`, 분할 CSV 디렉터리는 `RECATCH_CSV_DIR`로 조정할 수 있습니다.

## 포함된 데이터셋

공유 편의를 위해 2026-03-08 테스트 서버 50,000건 임포트에 사용한 데이터셋을 같이 포함했습니다.

- `data/lead_seed.csv`
- `data/lead_seed_full.csv`
- `data/lead_seed_instance_email_50000.json`
- `data/csv_split/lead_seed_instance_email_50000_part_001.csv` ... `050.csv`

기본 예시는 이 분할 CSV 50개를 바로 사용하도록 맞춰져 있지만, 새 실행 흐름에서는 원본 CSV 1개만 준비해도 됩니다.

## 데이터 규칙

- 원본 CSV 자동 분할을 쓰려면 `RECATCH_SOURCE_CSV` 또는 `--source-csv` 를 설정합니다.
- 기본 업로드 디렉터리는 `data/csv_split` 입니다.
- 기본 파일 prefix는 `lead_seed_instance_email_50000_part_` 입니다.
- 분할 단위는 `RECATCH_SPLIT_SIZE` 또는 `--split-size` 로 설정합니다.
- 현재 기본값은 `1000` 이며, 이는 2026-03-08 기준 Re:catch 한 번당 업로드 제한에 맞춘 값입니다.
- 파일명 규칙은 `{prefix}{part번호}.csv` 입니다.
- 현재 CLI는 내부적으로 `part:03d` 형식으로 파일명을 만듭니다.
- 예시:
  - `part 1` -> `lead_seed_instance_email_50000_part_001.csv`
  - `part 50` -> `lead_seed_instance_email_50000_part_050.csv`
  - `part 1000` -> `lead_seed_instance_email_50000_part_1000.csv`
- `--start`, `--end` 는 행 수가 아니라 파일 번호 범위입니다.
- `--end 0` 또는 `RECATCH_END=0` 은 "마지막 생성/감지 파트까지 전부"를 뜻합니다.
- 예시:
  - `--start 1 --end 50` -> `001`부터 `050`까지 50개 파일 업로드
  - `--start 1 --end 0` -> 마지막 파트까지 자동 감지 후 업로드
  - `--start 1 --end 1000` -> `001`부터 `1000`까지 파일이 실제로 있을 때만 업로드
- 중간 파일이 하나라도 없으면 그 지점에서 실패합니다.
- 현재 기본 운영 규칙은 `파일 1개 = 1000행` 이지만, 스크립트 자체는 파일 수 기준으로 동작합니다.

### CSV 헤더 규칙

기본 내장 매핑은 아래 헤더를 기준으로 작성되어 있습니다.

- `lead:deal_name`
- `contact:name`
- `contact:email`
- `company:name`

하지만 이제는 헤더가 달라도 실행 시점에 매핑을 직접 입력할 수 있습니다.

- `필드명`
  - 검색어와 선택지 텍스트를 동일하게 사용합니다.
- `검색어|선택지`
  - 검색어와 실제 클릭할 선택지 텍스트를 다르게 지정합니다.
- 빈 값
  - 기본값이 있으면 기본 매핑을 사용하고, 없으면 해당 열을 건너뜁니다.
- `-`
  - 해당 열을 명시적으로 건너뜁니다.

예시:

- `이메일`
- `텍스트|텍스트29`
- `-`

## 실행 예시

테스트 서버에서 원본 CSV 1개를 자동 분할하고, 매핑을 직접 입력하는 스모크 테스트:

```powershell
recatch-bulk-import --env-file .env.test --source-csv data\my_leads.csv --split-size 1000 --prompt-mapping --start 1 --end 1
```

기존처럼 이미 분할된 CSV 1개 파일만 테스트:

```powershell
recatch-bulk-import --env-file .env.test --start 1 --end 1
```

원본 CSV 전체 배치:

```powershell
recatch-bulk-import --env-file .env.prod --source-csv data\my_leads.csv --split-size 1000 --prompt-mapping --start 1 --end 0
```

매핑 파일을 재사용하는 전체 배치:

```powershell
recatch-bulk-import --env-file .env.prod --source-csv data\my_leads.csv --mapping-file mappings\prod-fields.json --start 1 --end 0
```

직접 모듈 실행도 가능합니다.

```powershell
$env:PYTHONPATH = "src"
python -m recatch_bulk_import --env-file .env.test --start 1 --end 1
```

## 주요 환경 변수

- `RECATCH_BASE_URL`
- `RECATCH_TEAM_SLUG`
- `RECATCH_RECORD_TYPE_ID`
- `RECATCH_SOURCE_CSV`
- `RECATCH_CSV_DIR`
- `RECATCH_FILE_PREFIX`
- `RECATCH_SPLIT_SIZE`
- `RECATCH_MAPPING_FILE`
- `RECATCH_PROMPT_MAPPING`
- `RECATCH_CREDENTIAL_FILE`
- `RECATCH_STATE_FILE`
- `RECATCH_LOG_DIR`
- `RECATCH_SCREENSHOT_DIR`
- `RECATCH_SKIP_COMPLETED`
- `RECATCH_MANUAL_LOGIN_FALLBACK`

상세 실행 규칙은 [`docs/RUNBOOK.md`](docs/RUNBOOK.md)에 정리했습니다.
