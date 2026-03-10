# new_build_model 채점 보고서
- 생성시각(UTC): 2026-02-27T03:00:52.037740+00:00
- 대상: bc1_model_output.json ~ bc25_model_output.json
- model_decisions 합계: 253 (TP=184, FP=12, SKIP=57)
- fn_decisions 합계: 261 (FN=6, NOT_FN=232, SKIP=23)
- HITL 후보(신뢰도<=6 또는 SKIP): 388건

## HITL 사유 요약
- 기타: 214건
- 값 변화(이전 판정 유지, HITL 권장): 97건
- 신규 field: 53건
- NOT_FN 재검토 필요: 21건
- 신규 candidate: 2건
- 값 변화 큼/근거 부족: 1건

## 메모별 집계
- M-W1: model(TP=6, FP=0, SKIP=3), fn(FN=0, NOT_FN=24, SKIP=8)
- M-W2: model(TP=7, FP=1, SKIP=1), fn(FN=0, NOT_FN=7, SKIP=2)
- M-W3: model(TP=4, FP=1, SKIP=2), fn(FN=0, NOT_FN=16, SKIP=1)
- M-W4: model(TP=4, FP=0, SKIP=3), fn(FN=1, NOT_FN=0, SKIP=1)
- M-W5: model(TP=8, FP=0, SKIP=1), fn(FN=0, NOT_FN=2, SKIP=0)
- M-W6: model(TP=5, FP=1, SKIP=1), fn(FN=1, NOT_FN=7, SKIP=0)
- M-W7: model(TP=8, FP=1, SKIP=2), fn(FN=0, NOT_FN=6, SKIP=0)
- M-W8: model(TP=9, FP=1, SKIP=1), fn(FN=0, NOT_FN=8, SKIP=1)
- M-W9: model(TP=8, FP=1, SKIP=5), fn(FN=1, NOT_FN=8, SKIP=0)
- M-W10: model(TP=7, FP=1, SKIP=1), fn(FN=0, NOT_FN=10, SKIP=1)
- M-W11: model(TP=8, FP=0, SKIP=2), fn(FN=0, NOT_FN=7, SKIP=1)
- M-W12: model(TP=11, FP=0, SKIP=1), fn(FN=0, NOT_FN=13, SKIP=2)
- M-W13: model(TP=9, FP=0, SKIP=2), fn(FN=0, NOT_FN=14, SKIP=3)
- M-W14: model(TP=5, FP=1, SKIP=4), fn(FN=0, NOT_FN=20, SKIP=1)
- M-W15: model(TP=11, FP=0, SKIP=3), fn(FN=0, NOT_FN=7, SKIP=1)
- M-W16: model(TP=2, FP=0, SKIP=0), fn(FN=0, NOT_FN=12, SKIP=0)
- M-W17: model(TP=9, FP=1, SKIP=3), fn(FN=0, NOT_FN=21, SKIP=1)
- M-W18: model(TP=10, FP=0, SKIP=2), fn(FN=0, NOT_FN=8, SKIP=0)
- M-W19: model(TP=6, FP=1, SKIP=0), fn(FN=0, NOT_FN=6, SKIP=0)
- M-W20: model(TP=6, FP=2, SKIP=6), fn(FN=2, NOT_FN=9, SKIP=0)
- M-W21: model(TP=12, FP=0, SKIP=0), fn(FN=1, NOT_FN=9, SKIP=0)
- M-W22: model(TP=6, FP=0, SKIP=2), fn(FN=0, NOT_FN=3, SKIP=0)
- M-W23: model(TP=10, FP=0, SKIP=4), fn(FN=0, NOT_FN=10, SKIP=0)
- M-W24: model(TP=4, FP=0, SKIP=3), fn(FN=0, NOT_FN=2, SKIP=0)
- M-W25: model(TP=9, FP=0, SKIP=5), fn(FN=0, NOT_FN=3, SKIP=0)