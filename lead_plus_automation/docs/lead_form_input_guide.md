# Re:catch 리드 생성 폼 입력 가이드

## 1. 목적

- 사용자별 커스텀 필드 구성이 달라도, 최소한의 필드만 안정적으로 입력하는 기준을 만든다.
- 자동화 실패 시 어떤 선택자/입력 단계가 깨졌는지 빠르게 파악할 수 있게 한다.
- 모달 선행 단계(회사 선택/연락처 선택)는 `lead_form_selector.py`로 분리해 독립적으로 안정화한다.

현재 스크립트 기본 전략은 `--field-plan minimal` 이다.

## 2. 권장 원칙

1. `XPath`보다 `CSS + 라벨 텍스트 매칭`을 우선 사용한다.
2. 클래스명 해시(`sc-xxxx`)에 직접 의존하지 않는다.
3. 모달 내부에서만 탐색한다. (전역 탐색 금지)
4. 값을 넣은 뒤 `input/change` 이벤트를 반드시 발생시킨다.
5. 실패 시 모달 상단 텍스트를 로그에 남겨 디버깅한다.

## 3. minimal 필드 플랜

`skeleton_vibium_flow.py --field-plan minimal` 기준 입력 대상:

1. 제목 (`제목`) - 사실상 필수
2. 이메일 (`QA-이메일` 또는 `테스트(이메일)`)
3. URL (`QA-URL` 또는 `테스트(도메인)`)
4. 금액 (`금액`) - 숫자형

선행 단계:

1. `lead_form_selector.py`의 `ensure_lead_form_ready(...)` 호출
2. 모달이 `회사 선택/연락처 선택` 단계에서 멈춰 있으면 선택 처리
3. 편집 가능한 필드 영역이 확인되면 필드 입력 단계 진행

## 4. 필드별 입력 방식

### 4.1 제목

1. 모달 상단의 텍스트 input을 먼저 탐색
2. 실패 시 라벨 `제목` 행을 찾아 같은 로직으로 입력
3. `input/change` 이벤트 발생
4. `필수값을 입력해주세요.` 메시지가 남아있는지 확인

핵심 구현 함수:

- `lead_form_title.py:set_required_title_field(...)`
- `set_modal_field_by_label(...)`

### 4.2 라벨 기반 공통 입력 (문자/숫자)

1. 모달 내부에서 라벨 텍스트를 정규화 후 contains 매칭
2. 해당 행의 value box (`[data-field-id]` 또는 input/textarea) 클릭
3. `document.activeElement`를 우선 에디터로 사용
4. 없으면 근처 가시 input 후보에서 에디터 선택
5. 타입별로 값 주입

타입별 처리:

1. `number`: 숫자만 남겨 입력 (`_normalize_number`)
2. `text/textarea`: 문자열 입력
3. `checkbox`: boolean 변환 후 체크

핵심 구현 함수:

- `set_modal_field_by_label(...)`
- `choose_first_success(...)`

## 5. 로그인 입력 방식 (참고)

로그인은 아래 순서로 처리한다.

1. Vibium `find().type()` 우선
2. readback 값 이상(빈 값/submit disabled) 시 native value setter fallback
3. submit 클릭 후 URL 전환 확인

핵심 구현 함수:

- `login_with_credentials(...)`

## 6. XPath를 꼭 써야 하는 경우

기본 권장은 아니다. 다만 라벨 구조가 비표준이라 CSS/텍스트 매칭이 실패하면 임시로 사용 가능하다.

예시 (개념):

```xpath
//div[contains(@class,'recatch-ant-modal')]//*[normalize-space(text())='금액']
```

주의:

1. DOM 레이어가 자주 바뀌어 취약하다.
2. 테넌트별 커스텀 UI에서 재사용성이 낮다.
3. 가능하면 XPath는 디버깅용으로만 사용하고, 최종 코드는 라벨 기반 JS 탐색으로 유지한다.

## 7. 신규 필드 추가 절차

1. 라벨 후보 2~3개 정의 (예: `["QA-이메일", "테스트(이메일)"]`)
2. CSV 컬럼과 매핑
3. `mappings_minimal` 또는 `mappings_extended`에 추가
4. 1건 회귀 실행으로 로그 확인
5. 실패 시 모달 텍스트 로그 + 스크린샷으로 라벨/입력타입 재확인

## 8. 실행 예시

```bash
python skeleton_vibium_flow.py --case-id QA_DYN_001 --limit 1 --field-plan minimal
python skeleton_vibium_flow.py --case-id QA_DYN_001 --limit 1 --field-plan extended
```
