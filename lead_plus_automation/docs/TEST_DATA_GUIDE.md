# TEST_DATA_GUIDE

## 목적
동적 수신자 그룹 QA를 위해 리드 테스트 데이터를 CSV로 관리하고, 자동화 실행 제어/기대 결과를 함께 기록한다.

## 파일
- `data/lead_seed.csv`: 리드 생성 입력 + 기대 결과 데이터
- `data/deal_seed.csv`: 리드 -> 딜 전환 검증 데이터

## lead_seed.csv 핵심 컬럼
- 식별: `case_id`, `title`
- 리드 기본값: `full_name`, `email`, `phone`, `mobile`
- 회사/프로필: `company_name`, `job_title`, `department`, `industry`, `company_size`, `revenue_krw`, `website`
- 상태/마케팅: `owner`, `lead_status`, `lifecycle_stage`, `score`, `utm_source`, `utm_medium`, `utm_campaign`
- 날짜/금액/동의: `last_activity_date`, `amount_krw`, `created_date`, `consent_status`
- 동적그룹 기대: `expected_dynamic_match`
- 실행 제어: `automation_enabled`, `priority`
- 생성 기대: `expected_create_success`, `expected_fail_reason`
- 제목 제어: `title_override`, `title_should_be_valid`
- 선택 제어: `company_select_text`, `contact_select_text`
- 메모: `notes`

## 실행 제어 규칙
1. `automation_enabled=TRUE` 인 케이스만 기본 실행 대상.
2. `--case-id`를 직접 지정하면 `automation_enabled`와 무관하게 해당 케이스 실행.
3. `expected_create_success`와 실제 결과를 비교해 pass/fail 판정.
4. `expected_fail_reason`가 있으면 실패 상세 메시지에 해당 키워드가 포함되어야 pass.

## 제목 제어 규칙
1. `title_override`가 비어 있으면 기본 제목 생성 규칙 사용.
2. `title_override=__EMPTY__`이면 빈 제목으로 입력 시도.
3. `title_override`에 `{suffix}` 포함 시 실행 시각 suffix로 치환.
4. `title_should_be_valid=FALSE`이고 `title_override`가 비어 있으면 빈 제목으로 간주.

## 선택 제어 규칙
1. `company_select_text`, `contact_select_text`가 비어 있으면 첫 옵션 선택.
2. 값이 있으면 옵션 텍스트 우선 매칭 후 선택.
3. 매칭 실패 시 첫 옵션 fallback.

## 운영 팁
1. 신규 케이스는 `case_id`를 고유하게 유지.
2. 회귀 배치는 `priority=P1` 중심으로 먼저 실행.
3. 실패 재현용 케이스는 `expected_create_success=FALSE`로 명시.
