# Re:catch Bulk Import With UI

비즈니스 팀원이 각자 로컬 환경에서 실행할 수 있도록 `recatch_bulk_import`를 별도 복제한 UI 버전입니다.

이 프로젝트는 기존 CLI 자동화를 그대로 사용하되, 아래를 UI에서 처리합니다.

1. 원본 CSV 경로 입력
2. split CSV 저장/조회 디렉터리 안내
3. 파트 범위 선택
4. 필드 매핑 입력
5. 진행률 표시
6. 실패 시 재시작 권장 범위 안내
7. Vibium/chromedriver 충돌 자동 정리
8. 에러 로그 확인
9. Agentation feedback 수집

## 핵심 특징

- 로컬 전용 UI: 각 사용자 PC에서 `localhost`로 실행
- 기존 CLI 유지: 필요하면 `recatch-bulk-import`도 그대로 사용 가능
- 별도 runner 사용: UI 브라우저 탭을 닫아도 백그라운드 작업은 계속 진행 가능
- 자동 정리 루틴 포함: `vibium serve`, `chromedriver`, 포트 `9515` 충돌 발생 시 정리 후 재시도
- 필드 매핑 UI 필수화: CSV 헤더별로 `검색어`와 `선택지 텍스트`를 명시적으로 입력
- Agentation 내장: 페이지 우하단 toolbar로 개선 의견을 남기고 로컬 파일/MCP로 수집 가능

## 빠른 시작

### macOS

```bash
cd /Users/admin/Desktop/Auto/Codex/codex_QA_Automation/recatch_bulk_import_withUI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
recatch-bulk-import-ui
```

UI 주소:

```text
http://127.0.0.1:8877
```

루트의 `run_ui.command`로도 실행할 수 있습니다.

## Agentation / MCP

이 UI에는 Agentation toolbar가 기본 내장되어 있습니다.

- endpoint: `http://localhost:4747`
- UI 로드 시 우하단 Agentation toolbar가 표시됩니다.
- `Send Annotations`를 누르면 로컬 로그 파일에도 저장됩니다.

Codex MCP 등록:

- 현재 머신의 Codex 설정 `~/.codex/config.toml` 에 `agentation-mcp server` 항목을 추가해 두었습니다.
- 새 Codex 세션부터 MCP 서버가 자동 등록됩니다.

현재 세션에서 바로 endpoint가 필요하면 아래 스크립트로 수동 실행할 수 있습니다.

```bash
/Users/admin/Desktop/Auto/Codex/codex_QA_Automation/recatch_bulk_import_withUI/run_agentation_mcp.command
```

## 실행 전 준비

사용자가 직접 준비해야 하는 것은 아래 2개입니다.

1. `env` 파일
2. credential 파일

실제 값 세팅은 전달자가 미리 맞춰서 배포하는 것을 권장합니다.

## UI 사용 순서

1. `env 파일`, `원본 CSV 경로`, `split CSV 디렉터리`, `파일 Prefix`, `시작/종료 파트` 확인
2. `CSV 헤더 불러오기` 클릭
3. 필드 매핑 입력
4. `임포트 시작` 클릭
5. 진행률/로그/권장 재시작 범위 확인

## 필드 매핑 규칙

필드 매핑은 UI에서 필수로 입력합니다.

- `검색어`: 드롭다운 검색창에 입력할 텍스트
- `선택지 텍스트`: 실제로 클릭할 옵션 텍스트
- `Skip`: 해당 열을 명시적으로 건너뜀

주의:

- 필드명은 Re:catch 화면의 텍스트와 정확히 일치해야 합니다.
- 잘못 입력하면 자동화가 실패하거나 잘못된 필드가 선택될 수 있습니다.

기본값 자동 채움 대상 헤더:

- `lead:deal_name` -> `제목`
- `contact:name` -> `이름`
- `contact:email` -> `이메일`
- `company:name` -> `회사명`

## 로그와 상태 파일

UI 실행 시 주요 산출물은 아래에 쌓입니다.

- 상태 파일: `logs/ui/*.state.json`
- runner 상태: `logs/ui/active-job-status.json`
- 실행 로그: `logs/ui/*.log`
- 매핑 파일: `mappings/ui/*.mapping.json`
- Vibium 스크린샷: `screenshots/`

문제 발생 시 아래 3개를 전달받으면 원인 파악이 가능합니다.

1. `logs/ui/active-job-status.json`
2. 해당 실행 `.log`
3. 필요 시 `screenshots/` 파일

Agentation feedback 파일:

- `logs/ui/agentation/latest-session.json`
- `logs/ui/agentation/latest-submit.json`
- `logs/ui/agentation/*.json`

## 재시작 원칙

- UI는 `next pending part`를 기준으로 재시작 권장 범위를 표시합니다.
- recoverable failure로 분류되면 runner가 자동 재시도합니다.
- 설정 오류나 파일 누락처럼 recover 불가한 오류는 `failed`로 멈춥니다.

## 포함된 명령

- `recatch-bulk-import-ui`: 로컬 UI 실행
- `recatch-bulk-import`: 기존 CLI 실행
- `recatch-bulk-import-probe`: 기존 매핑 probe 실행

## 참고

원본 CLI 문서와 runbook도 같이 남겨두었습니다.

- `docs/RUNBOOK.md`
- 기존 `src/recatch_bulk_import/*`
