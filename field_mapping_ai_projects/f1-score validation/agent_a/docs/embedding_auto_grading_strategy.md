# 임베딩 기반 자동 채점 고도화 방안

## 1. 문서 목적

이 문서는 필드 매핑 AI QA 과정에서 TP/FP/FN 채점을 부분 자동화하기 위한 고도화 방안을 정리한다.
목표는 다음과 같다.

- 사람이 전부 수동으로 채점하던 반복 작업을 줄인다.
- 자동 판정은 높은 정밀도를 우선 목표로 삼고, 애매한 케이스는 HITL(Human-in-the-loop)로 안전하게 회수한다.
- 기존 QA 결과물을 calibration dataset으로 재활용하여 type family별 threshold를 조정 가능하게 만든다.

이 문서는 현재 논의된 방향을 구현 기준점으로 삼기 위한 설계 문서이며, 추후 PoC 및 운영 버전 구현 시 참조용으로 사용한다.

---

## 2. 문제 정의

현재 QA 프로세스는 사람이 다음 두 축을 직접 판단한다.

1. `model_output`에 이미 매핑된 필드가 TP인지 FP인지 판단
2. `memo`에는 존재하지만 `model_output`에 매핑되지 않은 정보가 FN인지 판단

수동 QA는 정확하지만 비용이 크고, 빌드가 자주 바뀌는 상황에서 반복 비용이 빠르게 증가한다.

따라서 다음과 같은 자동화가 필요하다.

- 명확한 TP/FP/FN은 자동 판정
- 애매한 구간은 HITL로 보내기
- type family별 threshold를 조정하면서 점진적으로 자동화율을 늘리기

---

## 3. 핵심 설계 원칙

### 3.1 FN은 `model_output`만으로 판정할 수 없다

가장 중요한 전제는 다음과 같다.

- `TP/FP`는 `model_output` 기준으로 판단 가능하다.
- `FN`은 `model_output`만 봐서는 판단할 수 없다.

이유는 FN의 정의가 다음이기 때문이다.

- 메모 또는 candidate 수준에서는 존재함
- 하지만 모델이 해당 필드를 매핑하지 않음

즉 FN 탐지는 반드시 다음 중 하나를 기준으로 해야 한다.

- `memo` 원문
- `candidate_pool`
- `fn_review_input` 생성 전 단계의 candidate

따라서 자동 채점의 입력은 다음처럼 분리해야 한다.

- TP/FP 자동 판정 입력: `model_output`
- FN 자동 판정 입력: `input data(memo/candidate_pool)`

### 3.2 코사인 유사도는 핵심 신호이지만 단독 판정기로 쓰지 않는다

임베딩 cosine similarity는 유용하지만, 다음 이유로 단독 판정기는 위험하다.

- 숫자/금액/날짜 필드는 semantic similarity보다 type/rule이 더 중요할 수 있다.
- 비슷한 의미의 필드들([B] 예산, 총 계약 금액, MRR 등)은 semantic 상 가깝게 모일 수 있다.
- field label/caption/description 품질이 필드마다 균일하지 않다.
- 실제 운영에서는 high score라도 top1-top2 margin이 좁으면 불확실성이 크다.

따라서 최종 판정은 다음의 하이브리드 구조를 권장한다.

- embedding score
- type compatibility
- lexical overlap
- normalized value parsing success 여부
- top1-top2 margin
- type family별 calibration threshold

### 3.2.1 taxonomy는 field id가 아니라 `effective_schema.type` 중심으로 가져간다

고객마다 사용하는 field id와 label 구성이 달라질 수 있다.
따라서 자동 채점 정책을 특정 고객의 field id에 묶어두면 재사용성이 급격히 떨어진다.

정책의 기준축은 다음 순서를 권장한다.

1. `effective_schema.type`
2. 필요 시 `category`, `attributes`, option 구조
3. 값 파싱 결과(regex/normalization)
4. `field_id`는 분석/추적용으로만 사용

즉 threshold calibration과 HITL 정책은 `field id별 정책`이 아니라 `type family별 정책`으로 관리한다.

### 3.3 자동화의 목표는 F1 최대화보다 안전한 자동화율 확보

초기 버전의 목표는 다음이 적절하다.

- 자동 TP precision >= 95%
- 자동 FN candidate precision >= 90%
- 자동 FP precision >= 90%
- 애매한 구간은 과감하게 HITL

즉 초기 목표는 coverage 극대화가 아니라, **신뢰 가능한 자동 판정 영역 확보**이다.

---

## 4. 권장 아키텍처

## 4.1 입력 데이터

자동 채점기는 다음 입력을 사용한다.

### A. field metadata
- `effective_schema`
- 사용 필드: `label`, `caption`, `description`, `attributes.options.label`, `type`, `category`

### B. TP/FP 판정 입력
- `model_output`
- 사용 필드: `field_definition.id`, `field_definition.label`, `extracted_value`, 가능하면 evidence/source 정보

### C. FN 판정 입력
- `candidate_pool` 또는 `fn_review_input` 생성 전 candidate
- 사용 필드: `candidate_id`, `semantic_type`, `raw_text`, `normalized`, `mentions`, `line_text`

### D. calibration label
- 기존 수동 QA 결과
- `qa_review_ui/data/decisions/<build_version>/M-W*.json`

---

## 4.2 Field text blob 생성

각 field에 대해 임베딩용 설명 문자열을 생성한다.

권장 구성:

```text
[label]
[caption]
[description]
[option labels]
[type/category 힌트]
```

예시:

```text
필드명: [B] 예산
caption: 고객이 언급한 예산 또는 집행 가능 금액
description: 계약 금액이 아니라 예산 문맥의 금액을 기록
field_type: textarea
category: custom
```

주의:
- 일부 schema에서는 `caption`, `description`이 비어 있는 필드가 꽤 있다.
- 따라서 label만 존재하는 field는 embedding discrimination power가 약할 수 있다.
- 이런 field는 이후 rule-based 보강이 특히 중요하다.

---

## 4.3 Query text blob 생성

### A. TP/FP용 query blob

`model_output`의 각 item을 다음과 같이 요약한다.

```text
predicted_field_label: ...
extracted_value: ...
source_hint: ...
```

예시:

```text
predicted_field_label: 총 계약 금액
extracted_value: 1억 2천만 원
```

이 query를 모든 field blob과 비교한다.

### B. FN용 query blob

`candidate_pool`의 각 candidate를 다음과 같이 요약한다.

```text
semantic_type: ...
raw_text: ...
line_text: ...
normalized: ...
```

예시:

```text
semantic_type: risk_or_concern
raw_text: 마케팅 중요성: 연간 약 10억 원의 마케팅 예산을 투자하고 있습니다
line_text: • 마케팅 중요성: ...
```

이 query를 모든 field blob과 비교한다.

---

## 4.4 Score 계산

각 query에 대해 모든 field와 cosine similarity를 계산한다.

출력 예시:

```json
{
  "query_id": "item_12",
  "top_candidates": [
    {"field_id": "5374", "score": 0.84},
    {"field_id": "5557", "score": 0.72},
    {"field_id": "1593", "score": 0.51}
  ]
}
```

추가 feature도 함께 계산한다.

- `top1_score`
- `top2_score`
- `margin = top1_score - top2_score`
- `mapped_field_score`
- `type_compatible`
- `lexical_overlap`
- `value_parse_success`

---

## 5. 자동 판정 규칙

## 5.1 Auto TP

다음을 만족하면 자동 TP 후보로 본다.

- `top1 == mapped_field`
- `top1_score >= T_high[group]`
- `margin >= M_high[group]`
- `type_compatible == true`

해석:
- 현재 모델이 붙인 field가 semantic ranking 1위이고
- 점수도 충분히 높고
- 2위와도 충분히 차이가 나며
- 값 타입도 잘 맞는 경우

---

## 5.2 Auto FP

다음 중 하나에 해당하면 자동 FP 후보로 본다.

- `mapped_field_score <= T_low[group]`
- 또는 `top1 != mapped_field` 이고 `top1_score - mapped_field_score >= D_fp[group]`

해석:
- 모델이 붙인 field는 semantic 상으로 약하고
- 다른 field가 더 자연스러운 경우

예시:
- 예산 문맥인데 총 계약 금액으로 매핑됨
- 날짜 문맥인데 첫 세일즈 미팅 일자로 과탐됨

---

## 5.3 Auto FN candidate

다음을 만족하면 자동 FN 후보로 본다.

- `candidate`는 현재 `model_output`에서 unmatched
- `top1_score >= T_fn[group]`
- `margin >= M_fn[group]`
- `type_compatible == true`

해석:
- 메모 쪽 candidate는 강하게 특정 field를 가리키는데
- 모델이 해당 field를 출력하지 않은 경우

이 경우 최종 라벨은 `FN candidate`로 두고, 초기 버전에서는 사람이 빠르게 검토하는 방식이 적절하다.

---

## 5.4 HITL

다음 경우는 HITL로 보낸다.

- absolute score는 나쁘지 않지만 margin이 좁은 경우
- field군 자체가 historically unstable한 경우
- type은 맞지만 sibling field와 경쟁이 심한 경우
- value parsing 결과가 불안정한 경우
- calibration set에서 false positive가 잦았던 필드인 경우

중요한 점:

**HITL band는 단순한 점수 구간이 아니라, 불확실성 조건의 묶음이다.**

---

## 6. HITL band 설계 원칙

HITL을 단순히 `0.65 ~ 0.75면 HITL`처럼 고정폭으로 두는 것은 권장하지 않는다.

권장 방식은 다음과 같다.

### 6.1 주요 feature
- `top1_score`
- `margin`
- `type compatibility`
- `type family`
- `historical stability`

### 6.2 정책 예시

- `score 높음 + margin 큼` -> auto
- `score 낮음` -> reject/FP/NOT_FN 방향
- `score는 괜찮지만 margin이 작음` -> HITL
- `숫자/날짜인데 parsing 실패` -> HITL
- `과거에 반복적으로 흔들린 field` -> HITL band 확장

### 6.3 운영 원칙

초기에는 auto zone을 좁게 잡고, HITL zone을 넓게 잡는다.
시간이 지나 calibration data가 늘어나면 auto zone을 확대한다.

---

## 7. Type family별 threshold 전략

전역 threshold 하나로 모든 field를 처리하는 것은 비추천이다.
최소한 다음 그룹으로 나누는 것이 좋다.

### 7.1 taxonomy는 field id가 아니라 `effective_schema.type`을 기준으로 잡는다

고객마다 field 구성과 field id는 달라질 수 있다.
따라서 taxonomy를 특정 field id나 특정 고객의 label에 종속시키면 재사용성이 깨진다.

초기 taxonomy의 기준축은 다음이어야 한다.

- `effective_schema.type`
- 필요 시 `category`, `attributes`, 값 파싱 결과를 보조 신호로 사용
- `field_id`는 추적성 확보용으로만 사용

즉, threshold와 auto-grading policy는 **field id별 정책**이 아니라 **type family별 정책**으로 정의한다.

### 7.2 recommended type families

#### A. free_text family
대상 type 예시:
- `text`
- `textarea`

특징:
- embedding 성능이 잘 나오는 편
- label/caption/description 품질 영향을 많이 받음
- 의미가 비슷한 필드끼리 충돌 가능
- margin 중요

#### B. numeric family
대상 type 예시:
- `currency`
- `number`

특징:
- semantic보다 숫자/단위/문맥 rule이 중요
- regex/normalization 결합이 필요
- 값 파싱 성공 여부를 강한 feature로 사용

#### C. temporal family
대상 type 예시:
- `date`
- `date-time`

특징:
- 짧은 표현이 많아 semantic disambiguation이 어렵다
- margin과 parsing 성공 여부가 중요
- 날짜 계열 과탐 방지 rule이 필요하다

#### D. enum family
대상 type 예시:
- `select`
- `multi-select`
- `checkbox`

특징:
- option label lexical match가 중요
- embedding은 보조 신호로 사용
- option 집합 자체를 field blob에 포함하는 것이 중요

#### E. relation / actor family
대상 type 예시:
- `many-to-one`
- `user`

특징:
- 사람/담당자/소유자/관계 객체와 연관
- semantic만으로는 불안정할 수 있어 role/entity rule 보강 필요

#### F. contact / identifier family
대상 type 예시:
- `email`
- `phone-number`
- `url`
- `name`

특징:
- deterministic pattern matching이 강력함
- embedding은 보조 신호로만 사용해도 충분할 수 있음

### 7.3 운영 메모

동일한 `text` 타입 안에서도 실제 의미는 다양할 수 있다.
따라서 운영 단계에서는 다음 확장이 가능하다.

- 1차: type family 기준 threshold
- 2차: type family + value pattern 기준 세분화
- 3차: type family + semantic cluster 기준 세분화

하지만 초기 버전에서는 특정 고객의 field id 기준 taxonomy를 두지 않는다.

---

## 8. Calibration 방법

## 8.1 사용할 supervised set

초기 calibration set은 기존 수동 QA 결과를 사용한다.

예시 기준:
- `qa_review_ui/data/decisions/new_build_model/M-W*.json`

현재 확인된 데이터 규모 예시:
- reviewed decision files: 28개
- `model_decisions`: 290건
- `fn_decisions`: 312건

이 정도면 1차 calibration은 가능하지만, type family를 더 잘게 쪼갠 threshold를 세밀하게 잡기에는 아직 적을 수 있다.
따라서 초기에는 **field별이 아니라 type family별 threshold**를 권장한다.

## 8.2 positive / negative 분포 정의

### TP/FP calibration
- positive: 인간이 `TP`로 확정한 query-field pair
- negative: 인간이 `FP`로 확정한 query-field pair

### FN calibration
- positive: 인간이 `FN`으로 확정한 candidate-field pair
- negative: 인간이 `NOT_FN`으로 확정한 candidate-field pair

## 8.3 threshold 산출 전략

단순 `mean ± sigma`는 참고용으로 두고, 실제 threshold는 다음 방식이 더 안전하다.

### 권장
- precision target 기반 threshold
- empirical quantile 기반 threshold

예시:
- auto TP는 precision 95% 이상이 되는 최소 threshold
- auto FN candidate는 precision 90% 이상이 되는 최소 threshold

즉 threshold는 F1만 최대화하는 방향이 아니라, **자동 판정 precision을 보장하는 방향**으로 잡는다.

---

## 9. 임베드 모델 검토

## 9.1 후보 모델
- `multilingual-e5-large-instruct`

## 9.2 적합한 이유

이 모델은 다음 이유로 1차 베이스라인으로 적절하다.

- 한국어 포함 multilingual retrieval에 강한 편
- instruction-tuned query encoding 지원
- field retrieval / semantic ranking 용도와 잘 맞음

## 9.3 주의점

- 긴 입력은 512 token 부근에서 truncation 관리 필요
- cosine 점수가 상대적으로 높은 영역에 몰릴 수 있어 absolute threshold를 그대로 믿기 어렵다
- 모델 단독으로 숫자/날짜/옵션형 field 분리를 완전히 해결하지 못한다

## 9.4 결론

`multilingual-e5-large-instruct`는 **retrieval / ranking용 베이스라인 모델로 적절**하다.
다만 최종 분류기는 다음과 결합해야 한다.

- type compatibility
- type family별 threshold
- margin
- lexical/rule feature
- HITL fallback

---

## 9.5 Langfuse external evaluation pipeline 설계

Langfuse 문서의 external evaluation pipeline 패턴은 다음 3단계로 정리된다.

1. traces fetch
2. evaluator 실행
3. score를 다시 Langfuse에 attach

참고 문서:
- Query traces via SDK/API: https://langfuse.com/docs/api-and-data-platform/features/query-via-sdk
- External evaluation pipeline 예시: https://langfuse.com/guides/cookbook/example_external_evaluation_pipelines

### 실제 `field-mapper` trace 조회 결과 요약

`field-mapper` tag로 최근 traces를 직접 조회해본 결과, 현재 trace shape는 다음과 같다.

- `name = field-mapper`
- `tags = ["field-mapper"]`
- `output.structuredResponse.field_mappings` 존재
- trace 아래 observation에는 `GENERATION` 1개와 여러 `SPAN`이 존재
- 현재 trace metadata는 사실상 `resourceAttributes`, `scope` 수준만 존재
- 즉, `decision_key`, `memo_id`, `build_version`, `deal_id`, `schema_hash` 같은 평가용 식별자는 아직 없음

이 구조는 external evaluator를 붙이기에는 충분히 좋지만, gold label과 안정적으로 join하기 위한 metadata 보강이 필요하다.

### 권장 파이프라인

현재 목표는 reviewed 28건으로 calibration을 먼저 끝내는 것이 아니라, **live `field-mapper` traces에 external evaluation pipeline을 먼저 연결하는 것**이다.
즉 운영 순서는 다음을 권장한다.

1. live traces fetch + evaluator attach
2. score/comment/metadata를 Langfuse에 적재
3. 이후 reviewed 28건으로 threshold를 calibration
4. calibration 결과를 운영 evaluator 변수값에 반영

따라서 calibration은 중요하지만, 파이프라인 구성의 선행 조건은 아니다.
초기 버전은 threshold를 고정 상수 또는 환경 변수로 두고 운영해도 된다.

#### Step 1. 평가 대상 trace 조회

기본 필터:
- `tags = field-mapper`
- `from_timestamp`, `to_timestamp`
- 필요 시 `name = field-mapper` 추가 확인

초기 운영은 batch 방식이 적절하다.

- 예: 최근 24시간 trace를 50개씩 조회
- 또는 특정 빌드 배포 이후 생성된 trace만 조회

#### Step 2. trace에서 prediction 추출

현재 trace output에는 `structuredResponse.field_mappings`가 들어 있으므로, 이 값을 prediction으로 사용한다.

즉 evaluator가 비교할 prediction source는 다음과 같다.

- `trace.output.structuredResponse.field_mappings`

필요 시 observation의 `GENERATION`도 함께 조회해 reasoning/모델 정보/실행 컨텍스트를 참고할 수 있다.

#### Step 3. gold label resolve

live external evaluation의 1차 목표는 **실시간 trace 자체를 평가하는 것**이므로, 초기에 반드시 `decision_key`가 있어야 하는 것은 아니다.
현재 trace에는 다음이 함께 포함되어 있다.

- input
- schema
- output

따라서 live evaluator는 trace 단독으로도 동작 가능하다.

다만 `human-reviewed gold label`과 결합하는 offline calibration 단계에서는 join key가 있으면 훨씬 편해진다.
따라서 운영 우선순위는 다음과 같이 둔다.

1. 초기 live evaluator: trace 단독 평가
2. 이후 calibration 단계: reviewed set과 join
3. 필요 시 tracing metadata 보강

즉 `decision_key`는 필수 선행 조건은 아니지만, 나중에 reviewed set과 안정적으로 연결하려면 `memo_hash` 또는 유사 식별자 정도는 추가하는 것이 바람직하다.

#### Step 4. evaluator 실행

외부 evaluator는 다음 2단계로 동작한다.

- `model_output` 기반 auto TP/FP 판정
- `input data(candidate_pool/memo)` 기반 auto FN candidate 판정

출력은 다음 4-way 중 하나다.

- `AUTO_TP`
- `AUTO_FP`
- `AUTO_FN_CANDIDATE`
- `HITL`

#### Step 5. Langfuse score attach

Langfuse score는 trace level aggregate와 observation/detail level을 분리해서 생각하는 것이 좋다.

##### A. trace-level aggregate score

초기 버전에서는 trace-level score가 핵심이다.
이번 단계에서는 score를 모두 **numeric 퍼센트 값(0~100 스케일)**으로 두고, `0.78` 같은 비율값이 아니라 `78`처럼 기록한다.

추천 score name은 다음과 같다.

- `fm_N`
- `fm_est.tp_count`
- `fm_est.fp_count`
- `fm_est.fn_count`
- `fm_est.hitl_count`
- `fm_est.f1_per`

권장 의미는 다음과 같다.

- `fm_N = TP + FP + FN + HITL`
- 모든 score의 분모는 동일하게 `TP + FP + FN + HITL`로 통일한다.
- `fm_est.tp_count = (TP / (TP + FP + FN + HITL)) * 100`
- `fm_est.fp_count = (FP / (TP + FP + FN + HITL)) * 100`
- `fm_est.fn_count = (FN / (TP + FP + FN + HITL)) * 100`
- `fm_est.hitl_count = (HITL / (TP + FP + FN + HITL)) * 100`
- `fm_est.f1_per = (2 * tp_ratio / (2 * tp_ratio + fp_ratio + fn_ratio)) * 100`
  - 여기서 `tp_ratio`, `fp_ratio`, `fn_ratio`는 `0~1` 내부 계산값이며, Langfuse에 저장할 최종 값은 `0~100`이다.

주의:
- `fm_N`은 비율이 아니라 raw count이다.
- 이름은 `*_count`이지만 실제 저장 값은 raw count가 아니라 퍼센트 값이다.
- 네 값의 합은 100이 되도록 설계한다.
- 따라서 문서와 대시보드에서 이 점을 명시해야 해석 혼란이 없다.
- raw count 자체는 `comment`나 `metadata`에 함께 남기는 것을 권장한다.

추가 aggregate score가 필요하면 다음도 고려할 수 있다.

- `fm_est.auto_coverage`
- `fm_est.precision_proxy`
- `fm_est.recall_proxy`
- `fm_est.f1_proxy`

하지만 초기 버전에서는 위 4개 score만으로도 상태 파악은 충분하다.

comment에는 어떤 필드가 TP/FP/FN/HITL인지 사람이 바로 볼 수 있도록 요약을 넣는다.
예시:

- `TP: 1593(✅ MRR), 5361(Next Action) | FP: 1591(첫 세일즈 미팅 일자) | FN: 5374([B] 예산) | HITL: 5378([T] 타임라인)`
- `TP_raw=12 FP_raw=1 FN_raw=2 HITL_raw=3 | numeric family margin conflict on budget/contract_amount`

권장 comment 원칙:

- `field_id(label)` 형식으로 표시
- 너무 길어지면 상위 위험 항목만 노출
- 전체 breakdown은 metadata JSON에 저장

##### B. observation-level score

초기 버전에서는 observation-level score는 선택 사항이다.

만약 붙인다면 `GENERATION` observation에 한정하는 것을 권장한다.
이유는 현재 trace 안에 여러 `SPAN`이 존재하므로, 세부 span마다 score를 붙이면 오히려 분석이 지저분해질 수 있기 때문이다.

추천 use case:
- `fm.generation_quality`
- `fm.output_parseable`

##### C. per-field 세부 결과

per-field 결과를 Langfuse score 하나하나로 다 쪼개는 것은 초기에 비추천이다.
필드 수가 많고 고객별 field id가 달라서 score cardinality가 급격히 증가한다.

초기에는 다음처럼 운영하는 것이 더 낫다.

- trace-level aggregate score는 Langfuse score로 저장
- per-field breakdown은 comment와 metadata로 저장
- comment에는 TP/FP/FN/HITL 필드를 사람이 읽기 좋게 요약
- metadata에는 raw count, full field list, family breakdown을 구조화해서 저장
- 충분히 안정화되면 일부 핵심 aggregate만 score로 승격

### 현재 구조 기준 결론

현재 `field-mapper` trace는 input, output, schema가 함께 들어 있어 live external evaluation pipeline을 붙이기 적합하다.

초기 버전의 우선순위는 다음과 같다.

1. live traces를 대상으로 evaluator 연결
2. `fm_est.tp_count`, `fm_est.fp_count`, `fm_est.fn_count`, `fm_est.hitl_count`를 numeric score로 적재
3. comment와 metadata에 필드 breakdown 저장
4. 이후 reviewed 28건으로 threshold calibration 수행

또한 Python 3.14 환경에서는 Langfuse SDK가 불안정하므로, 당장은 public API 직접 호출 방식으로 구현하는 것이 안전하다.

---

## 10. 구현 단계 제안

## Phase 1. Live external evaluator 연결

목표:
- `field-mapper` traces를 조회하여 live evaluator를 실행하고 Langfuse score/comment/metadata를 적재

산출물:
- trace fetcher
- evaluator runner
- Langfuse score attach 로직

## Phase 2. Score schema 안정화

목표:
- `fm_est.tp_count`, `fm_est.fp_count`, `fm_est.fn_count`, `fm_est.hitl_count` 및 comment/metadata 포맷 고정

산출물:
- score naming spec
- comment template
- metadata schema

## Phase 3. Threshold calibration

목표:
- reviewed set을 사용하여 type family별 `T_high`, `T_low`, `M_high`, `M_fn`, `D_fp` 추정

산출물:
- calibration report
- auto coverage vs precision 표

## Phase 4. Auto-grader 안정화 및 UI 연동

목표:
- 자동 판정 결과를 QA UI 기본값 또는 추천값으로 표시

산출물:
- decision 초안 preload
- HITL 우선순위 정렬

---

## 11. 추천 데이터 구조

자동 채점 결과 예시:

```json
{
  "decision_key": "M-W1",
  "item_type": "model_output",
  "item_id": "item_3",
  "mapped_field_id": "5374",
  "top1_field_id": "5374",
  "top1_score": 0.84,
  "top2_field_id": "5557",
  "top2_score": 0.72,
  "margin": 0.12,
  "type_compatible": true,
  "predicted_label": "AUTO_TP",
  "confidence": 0.93,
  "reason": [
    "top1 equals mapped field",
    "score above threshold",
    "margin above threshold"
  ]
}
```

FN candidate 예시:

```json
{
  "decision_key": "M-W1",
  "item_type": "candidate_pool",
  "candidate_id": "C-0002",
  "top1_field_id": "5374",
  "top1_score": 0.81,
  "top2_field_id": "5376",
  "top2_score": 0.58,
  "margin": 0.23,
  "predicted_label": "AUTO_FN_CANDIDATE",
  "confidence": 0.91
}
```

---

## 12. 리스크 및 주의사항

### 12.1 Schema 품질 편차
- field metadata가 빈약한 필드는 embedding discrimination이 약할 수 있다.

### 12.2 Sibling field 충돌
- 예산/계약금액/MRR/Seat 수 등은 semantic proximity가 높아 FP가 반복될 수 있다.

### 12.3 Date 계열 과탐
- 첫 세일즈 미팅 일자 vs 타임라인은 여전히 rule 보강이 필요하다.

### 12.4 Coverage 욕심 금지
- 초기 단계에서 auto coverage를 과도하게 늘리면 오히려 reviewer 신뢰를 잃는다.

---

## 13. 우선순위 높은 다음 액션

1. `field-mapper` live traces를 읽는 external evaluator 스크립트 작성
2. Langfuse score/comment/metadata schema 확정
3. `fm_est.tp_count`, `fm_est.fp_count`, `fm_est.fn_count`, `fm_est.hitl_count` 적재 로직 구현
4. reviewed set 기반 calibration feature table 생성
5. calibration 결과를 evaluator 변수값에 반영

---

## 14. 한 줄 요약

자동 채점의 핵심은 다음이다.

- `TP/FP는 model_output 기반`
- `FN은 input data(candidate/memo) 기반`
- `embedding은 retrieval/ranking의 핵심 신호`
- `최종 판정은 type/rule/margin/threshold/HITL을 결합한 hybrid 방식`
- `threshold는 전역 하나가 아니라 type family별로 calibration`

이 방향으로 가면, 수동 QA를 완전히 대체하기보다 **신뢰 가능한 자동 초안 + HITL 우선순위화**를 먼저 달성할 수 있다.

부가 원칙:
- taxonomy의 기준은 `field_id`가 아니라 `effective_schema.type`이다.
- `field_id`는 threshold 정의의 기준이 아니라 결과 추적성과 분석의 기준이다.
