# 최종 채점 보고서 (new_build_model)

## 1) 1~10점 신뢰도 기준
- 9~10: 이전 빌드와 추출값이 사실상 동일, 판정 이관 리스크 낮음
- 7~8: 커버 근거가 충분하거나(문자열/의미상) 이전 판정 유지가 타당
- 5~6: 이전 판정 유지는 가능하지만 값 변화가 있어 검증 권장
- 3~4: 신규 항목/커버 불명확/판정 충돌로 HITL 필요
- 1~2: 이번 배치에서는 미사용

## 2) HITL 기준 점수
- 운영 임계값: `4점 이하` 또는 `decision=SKIP`
- 이유: NOT_FN 기본값 정책을 보수적으로 유지하면서, 불확실 구간만 수동 검증 대상으로 제한

## 3) HITL 리스트 요약
- HITL 총 건수: 80
- model_decisions: TP=184, FP=12, SKIP=57 (총 253)
- fn_decisions: FN=6, NOT_FN=232, SKIP=23 (총 261)
- 주요 사유:
  - 신규 field: 53건
  - NOT_FN 재검토 필요: 21건
  - 기타: 3건
  - 신규 candidate: 2건
  - 값 변화 큼/근거 부족: 1건
- decision-key 전체 목록: `HITL_list_threshold4.csv` 참조

메모별 HITL 건수:
- M-W1: 11건
- M-W2: 3건
- M-W3: 3건
- M-W4: 4건
- M-W5: 1건
- M-W6: 1건
- M-W7: 2건
- M-W8: 2건
- M-W9: 5건
- M-W10: 2건
- M-W11: 3건
- M-W12: 3건
- M-W13: 5건
- M-W14: 5건
- M-W15: 4건
- M-W17: 4건
- M-W18: 2건
- M-W20: 6건
- M-W22: 2건
- M-W23: 4건
- M-W24: 3건
- M-W25: 5건

## 4) 특이사항
- M-W1, M-W2는 기존 대비 FN candidate 집합이 달라져(각각 -4, +2) 신규/누락 candidate가 발생함
- model_output은 1~25 전체에서 필드 구성/값 변화가 있어, 신규 field_id는 전부 SKIP(HITL) 처리함
- NOT_FN 변경은 최소화했고, 커버 근거가 약한 경우에는 FN으로 즉시 변경하지 않고 SKIP으로 보류함
- 생성 산출물은 기존 폴더를 건드리지 않고 `new_build_model`에 분리 저장함

## 5) 유사도 계산 방법
- `유사도 x.xx`는 기존/신규 `extracted_value` 문자열을 비교한 값입니다.
- 계산 절차:
  - 값이 `dict/list`면 JSON 문자열로 직렬화 (`sort_keys=True`)
  - 소문자 변환 + 연속 공백을 단일 공백으로 정규화
  - Python `difflib.SequenceMatcher(None, old, new).ratio()` 사용
- 점수 범위: `0.00 ~ 1.00` (1.00이면 문자열 동일)
- 예시: `유사도 0.51`은 정규화 후 문자 시퀀스 기준으로 약 51% 유사하다는 뜻입니다.

참고: FN 쪽 `cov`는 위 유사도와 별도입니다.
- `cov`는 `raw_text`가 `model_output` 필드들에 얼마나 커버되는지 계산한 값
- `max(부분문자열 포함 여부, SequenceMatcher ratio, 토큰 겹침비율)` 방식으로 산출
