# Bulk Import Runbook

## 공유 운영 원칙

1. 프로드 반영 전에는 반드시 테스트 서버에서 1개 파일로 스모크 테스트를 수행합니다.
2. 프로드에서는 `--skip-completed` 또는 상태 파일을 사용해 재실행 가능하게 유지합니다.
3. 실계정 자격증명은 `credentials/recatch_login.txt` 또는 별도 보안 저장소로 관리합니다.

## 권장 세팅

- `.env.test`: 테스트 서버용
- `.env.prod`: 프로드 서버용
- `data/`: 원본 CSV 저장
- `data/csv_split/`: 자동 생성되거나 직접 준비한 분할 CSV 저장
- `RECATCH_SPLIT_SIZE`: 현재 기본값 `1000`
- `RECATCH_MAPPING_FILE`: 재사용할 매핑 JSON 경로

## 권장 실행 흐름

1. 원본 CSV 1개를 `data/` 아래에 둡니다.
2. `.env`에 `RECATCH_SOURCE_CSV` 와 `RECATCH_SPLIT_SIZE` 를 설정합니다.
3. 처음 한 번은 `RECATCH_PROMPT_MAPPING=true` 또는 `--prompt-mapping` 으로 열별 매핑을 입력합니다.
4. 필요하면 매핑 JSON을 저장해서 다음 실행부터 재사용합니다.
5. 로그에서 `[part 1/50]` 형태의 진행 상황을 확인합니다.

## 추천 실행 순서

### 1. 테스트 스모크

원본 CSV 자동 분할 + 매핑 입력:

```powershell
recatch-bulk-import --env-file .env.test --source-csv data\my_leads.csv --split-size 1000 --prompt-mapping --start 1 --end 1
```

기존 분할 CSV 스모크:

```powershell
recatch-bulk-import --env-file .env.test --start 1 --end 1
```

### 2. 테스트 전체 실행

```powershell
recatch-bulk-import --env-file .env.test --source-csv data\my_leads.csv --split-size 1000 --prompt-mapping --start 1 --end 0
```

### 3. 프로드 스모크

```powershell
recatch-bulk-import --env-file .env.prod --source-csv data\my_leads.csv --mapping-file mappings\prod-fields.json --start 1 --end 1 --manual-login-fallback
```

### 4. 프로드 전체 실행

```powershell
recatch-bulk-import --env-file .env.prod --source-csv data\my_leads.csv --mapping-file mappings\prod-fields.json --start 1 --end 0 --skip-completed
```

## 실패 시 확인 위치

- 실행 로그: `logs/bulk-import-YYYYMMDD-HHMMSS.log`
- 상태 파일: `logs/*.json`
- 실패 스크린샷: `screenshots/shot-*.png`

## 포트 충돌

Vibium 포트 충돌이 나면 남아 있는 `vibium` 또는 `chromedriver` 프로세스를 정리한 뒤 재실행합니다.

## 필드 매핑 전제

기본 내장 매핑은 아래 헤더 구조를 기준으로 합니다.

- `lead:deal_name`
- `contact:name`
- `contact:email`
- `company:name`

그 외 헤더는 실행 시점에 직접 입력할 수 있습니다.

- `필드명`
  - 검색어와 선택지 텍스트를 동일하게 사용
- `검색어|선택지`
  - 검색어와 실제 클릭할 선택지를 분리
- 빈 값
  - 기본값 사용 또는 skip
- `-`
  - 명시적 skip

예시:

- `이메일`
- `텍스트|텍스트29`
- `-`
