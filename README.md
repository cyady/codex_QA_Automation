# codex_QA_Automation

이 저장소는 현재 Re:catch 대량 리드 업로드 자동화에 맞춰 정리되어 있습니다.
학습용으로 만들었던 단일 입력 자동화, 다이어그램, 임시 산출물은 메인 브랜치에서 제거했고, 유지 대상은 `recatch_bulk_import` 중심으로 남겼습니다.

AI validation 파이프라인(`agent_a`, `schema_generator`, `qa_review_ui`, Langfuse external evaluation)은 별도 저장소 [`../AI_validation_pipeline`](/Users/admin/Desktop/Auto/Codex/repos/AI_validation_pipeline) 로 분리해 관리합니다.

## 주요 모듈

- `recatch_bulk_import/`
  `/leads/import` 기준 대량 업로드 자동화 패키지입니다.
  로그인 처리, CSV 분할, 매핑 설정, 실행 로그, 운영용 문서를 함께 관리합니다.

## 보조 작업 공간

- `tests/`
  간단한 검증용 스크립트를 두는 임시 공간입니다.

## 시작 방법

1. Python 3.10 이상 환경을 준비합니다.
2. `recatch_bulk_import/` 기준으로 작업합니다.
3. editable 모드로 설치합니다.
4. 실행 전에 예제 env 파일과 credential 파일을 복사해서 로컬 환경을 채웁니다.

```bash
pip install -e recatch_bulk_import
```

## 관리 기준

- 자격 증명, 로컬 `.env` 파일은 커밋하지 않습니다.
- 로그, 스크린샷, 임시 출력물은 로컬 산출물로만 취급합니다.
- 실제 사용 방법과 실행 절차는 `recatch_bulk_import/README.md` 와 `docs/RUNBOOK.md` 를 기준으로 봅니다.
