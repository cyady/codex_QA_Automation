# Re:catch Import Operator Skills

비개발자도 Codex skill과 함께 사용할 수 있도록 정리한 Re:catch 딜 대량 import 운영용 repo입니다.

이 repo의 역할은 아래 6개입니다.

1. `.env`와 credential 상태 점검
2. 원본 CSV 분석과 변환 계획 산출
3. Re:catch 1회 최대 1000건 제한에 맞춘 CSV 분할
4. 딜 필드 생성
5. 레코드 타입 레이아웃 검증
6. 실제 딜 import 실행
7. split된 CSV 전 파트 batch import
8. 중복 회사 병합

## 포함된 명령

- `recatch-import-operator-skills doctor`
- `recatch-import-operator-skills inspect-source`
- `recatch-import-operator-skills build-transform-plan`
- `recatch-import-operator-skills split-source`
- `recatch-import-operator-skills create-fields`
- `recatch-import-operator-skills verify-layout`
- `recatch-import-operator-skills inspect-import`
- `recatch-import-operator-skills import-csv`
- `recatch-import-operator-skills batch-import`
- `recatch-import-operator-skills merge-company`
- `recatch-import-operator-skills list-tools`

## 빠른 시작

```bash
cd /Users/admin/Desktop/Auto/Codex/codex_QA_Automation/recatch_import_operator_skills
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
cp .env.example .env
cp credentials/recatch_login.example.txt credentials/recatch_login.txt
```

`.env` 예시:

```dotenv
RECATCH_BASE_URL=https://test.recatch.cc
RECATCH_RECORD_TYPE_ID=2234
RECATCH_RECORD_TYPE_TITLE=for_bulk_import_test(건들지 말것)
RECATCH_CREDENTIAL_FILE=credentials/recatch_login.txt
RECATCH_SOURCE_CSV="data/test_DB_Migration_Part1 .csv"
RECATCH_JOB_DIR=jobs
RECATCH_MAX_ROWS_PER_IMPORT=1000
RECATCH_HEADLESS=false
RECATCH_KEEP_OPEN=false
RECATCH_UPLOAD_TIMEOUT_SEC=60
```

credential 파일 예시:

```txt
email=your-email@example.com
password=your-password
```

주의:

- 이 repo는 Re:catch 로그인 화면의 이메일/비밀번호 입력까지만 자동화합니다.
- 로그인 중 `Recatch_alphakey(으)로 로그인` 같은 workspace SSO 버튼이 보이면 중단합니다.
- 알파키 화면으로 넘어가거나 알파키 입력을 자동화하지 않습니다.

## 샘플 데이터

샘플 CSV는 아래 파일을 사용합니다.

[`data/test_DB_Migration_Part1 .csv`](/Users/admin/Desktop/Auto/Codex/codex_QA_Automation/recatch_import_operator_skills/data/test_DB_Migration_Part1%20.csv)
이 샘플은 현재 기준:

- 헤더 28열
- 데이터 999행
- `1000`건 기준 분할 시 1개 파트

실제 운영 CSV는 보통 `4만~5만`행이므로 `1000`건 기준으로 `40~50`개 파트로 나누는 것을 전제로 합니다.

## 권장 작업 순서

### 1. 설정 점검

```bash
recatch-import-operator-skills doctor
```

### 2. 원본 CSV 분석

```bash
recatch-import-operator-skills \
  inspect-source \
  --source-csv "data/test_DB_Migration_Part1 .csv" \
  --job-id sample-db-migration
```

### 3. 변환 계획 생성

```bash
recatch-import-operator-skills \
  build-transform-plan \
  --source-csv "data/test_DB_Migration_Part1 .csv" \
  --job-id sample-db-migration
```

생성되는 주요 파일:

- `jobs/sample-db-migration/artifacts/source-summary.json`
- `jobs/sample-db-migration/artifacts/mapping-template.json`
- `jobs/sample-db-migration/artifacts/field-spec-candidates.json`
- `jobs/sample-db-migration/artifacts/transform-plan.json`

### 4. 필요한 필드 생성

```bash
recatch-import-operator-skills \
  create-fields \
  --spec-file jobs/sample-db-migration/artifacts/field-spec-candidates.json \
  --no-verify-layout
```

### 5. Import 화면 점검

```bash
recatch-import-operator-skills inspect-import
```

만약 여기서 workspace SSO 프롬프트가 뜨면, 현재 환경은 알파키 경유 로그인이 필요한 상태입니다. 이 repo는 그 버튼을 누르지 않고 실패로 종료합니다.

### 6. CSV 분할

```bash
recatch-import-operator-skills \
  split-source \
  --source-csv "data/test_DB_Migration_Part1 .csv" \
  --job-id sample-db-migration
```

생성되는 주요 파일:

- `jobs/sample-db-migration/source/parts/*.csv`
- `jobs/sample-db-migration/artifacts/split-manifest.json`

### 7. Preview Import

```bash
recatch-import-operator-skills \
  import-csv \
  --csv-file jobs/sample-db-migration/source/parts/test_DB_Migration_Part1_part_001.csv \
  --preview-only
```

### 8. 실제 업로드

```bash
recatch-import-operator-skills \
  import-csv \
  --csv-file jobs/sample-db-migration/source/parts/test_DB_Migration_Part1_part_001.csv
```

### 9. 전 파트 batch import

```bash
recatch-import-operator-skills \
  batch-import \
  --job-id sample-db-migration \
  --preview-only
```

실업로드:

```bash
recatch-import-operator-skills \
  batch-import \
  --job-id sample-db-migration
```

batch state 파일:

- `jobs/sample-db-migration/artifacts/batch-import-state.json`
- 기본값은 `--skip-completed` 이므로 중단 후 같은 명령으로 재실행하면 완료 파트를 건너뜁니다.

### 10. 중복 회사 병합

preview-only:

```bash
recatch-import-operator-skills \
  merge-company \
  --company-name "국민대학교" \
  --select-count 2
```

실제 병합:

```bash
recatch-import-operator-skills \
  merge-company \
  --company-name "국민대학교" \
  --select-count 2 \
  --survivor-index 1 \
  --no-preview-only
```

## Codex Skill 전달

이 repo에는 portable skill 폴더가 포함되어 있습니다.

- skill source: [`codex_skill/recatch-import-operator/SKILL.md`](/Users/admin/Desktop/Auto/Codex/codex_QA_Automation/recatch_import_operator_skills/codex_skill/recatch-import-operator/SKILL.md)
- install script: [`scripts/install_codex_skill.py`](/Users/admin/Desktop/Auto/Codex/codex_QA_Automation/recatch_import_operator_skills/scripts/install_codex_skill.py)

설치:

```bash
python scripts/install_codex_skill.py
```

설치 후 Codex에서는 `recatch-import-operator` skill을 사용해 다음 흐름을 안내할 수 있습니다.

1. env/credential 점검
2. CSV 분석
3. 필요한 필드 후보 파악
4. 1000건 분할
5. 필요한 필드 생성
6. preview import
7. 실제 import
8. batch import 재개
9. 중복 회사 병합 preview/실행

## 참고

실제 검증 기준:

- `inspect-import` 로그인/화면 진입 성공
- smoke CSV `import-csv --preview-only` 성공
- smoke CSV 실제 `import-csv` 성공
- smoke manifest `batch-import --preview-only` 성공
- `merge-company --company-name "국민대학교" --select-count 2 --preview-only` 성공

`list-tools`를 실행하면 현재 repo가 직접 제공하는 작업 목록을 볼 수 있습니다.
