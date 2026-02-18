# Lead Plus Automation (Vibium)

CSV 데이터를 읽어 Re:catch 리드를 자동 생성하는 스크립트입니다.

## 주요 기능

1. `data/lead_seed.csv`에서 테스트 케이스 로드
2. 로그인 모듈(`recatch_auth.py`)을 통한 텍스트 파일(`credentials/recatch_login.txt`) 기반 로그인
3. 선택 단계 모듈(`lead_form_selector.py`)로 회사/연락처 선택 처리
4. 제목 필드 모듈(`lead_form_title.py`)로 필수 제목 입력/검증
5. 생성 후 리스트 검색으로 검증

## CSV 운영 전략

- `data/lead_seed.csv`: 기본 회귀용(core) 데이터셋
- `data/lead_seed_full.csv`: 확장 필드 포함 마스터 데이터셋

현재 자동화에서 안정적으로 커버/검증하는 필드는 아래 4개입니다.

- `title`
- `contact_email`
- `company_website`
- `amount_krw`

## 요구사항

- Python 3.10+
- `vibium` (`pip install -r requirements.txt`)

## 로그인 파일 준비

`credentials/recatch_login.example.txt`를 복사해서 아래 파일을 만드세요.

- `credentials/recatch_login.txt`

형식:

```txt
email=your-email@example.com
password=your-password
```

또는

```txt
your-email@example.com
your-password
```

`credentials/recatch_login.txt`는 `.gitignore`에 포함되어 저장소에 올라가지 않습니다.

## 실행

```bash
python skeleton_vibium_flow.py --case-id QA_DYN_001 --limit 1
```

옵션 예시:

```bash
python skeleton_vibium_flow.py --csv data/lead_seed.csv --limit 10
python skeleton_vibium_flow.py --csv data/lead_seed_full.csv --limit 10
python skeleton_vibium_flow.py --credential-file credentials/recatch_login.txt --limit 3
python skeleton_vibium_flow.py --manual-login-fallback
python skeleton_vibium_flow.py --skip-verify
python skeleton_vibium_flow.py --field-plan minimal
python skeleton_vibium_flow.py --field-plan extended
```

## 출력

- 실행 로그: `logs/run-YYYYMMDD-HHMMSS.log`
- 스크린샷: `shot-YYYYMMDD-HHMMSS-*.png`

## 필드 입력 가이드

- `docs/lead_form_input_guide.md`

## 로그인 모듈 재사용 예시

```python
from pathlib import Path
from recatch_auth import ensure_recatch_login, parse_credential_file

credential = parse_credential_file(Path("credentials/recatch_login.txt"))
ensure_recatch_login(
    session=session,
    login_url="https://test.recatch.cc/login?redirect=/leads",
    leads_url="https://test.recatch.cc/leads",
    credential=credential,
    manual_login_fallback=False,
    log=print,
)
```

## New CSV control columns

- `automation_enabled`: default batch include flag
- `priority`: case priority (for example `P1`, `P2`)
- `expected_create_success`: expected create outcome for pass/fail
- `expected_fail_reason`: expected failure keyword when create is expected to fail
- `title_override`: force title value (`__EMPTY__` for blank title)
- `title_should_be_valid`: title validity expectation
- `company_select_text`: preferred company option text in selector
- `contact_select_text`: preferred contact option text in selector
