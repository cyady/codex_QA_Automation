# Re:catch Segments API Evidence

수집 기준:
- 페이지 내 fetch/xhr 로거 주입 후 이벤트별로 로그 초기화
- 민감정보는 마스킹, 본 표에는 URL/상태/요약만 기록
- 기준 시각: 2026-02-16

| Event | UI Action | Method | URL | Status | Request Payload 요약 | Response 요약 | Notes |
|---|---|---|---|---|---|---|---|
| A-1 목록 조회 | 생성 직후 목록 복귀 시 목록 갱신 | GET | `https://api.recatch.cc/recipient-groups` | 200 | 없음 | 수신자 그룹 목록 반환 | 목록 데이터 소스 확인 |
| A-2 상세 진입 | 목록 첫 행 클릭 | GET | `https://api.recatch.cc/recipient-groups/902` | 200 | 없음 | 그룹 메타 반환 | 상세 헤더 데이터 |
| A-3 상세 수신자 조회 | 상세 진입 직후 | GET | `https://api.recatch.cc/recipient-groups/902/recipients?page_count=50` | 200 | 없음 | 수신자 목록 반환 | 수신자 탭 데이터 |
| A-4 필드 메타 | 상세 진입 직후 | GET | `https://api.recatch.cc/sales-entity/lead/fields?version=20250519` | 200 | 없음 | 리드 필드 메타 반환 | deal/company/contact도 동일 패턴 확인 |
| B-1 그룹 생성 | `수신자 그룹` 버튼 클릭 | POST | `https://api.recatch.cc/recipient-groups` | 201 | 빈 바디(기본 생성) | 신규 그룹 생성 | 생성된 id: `929` |
| B-2 생성 후 상세 재조회 | 생성 직후 자동 이동 | GET | `https://api.recatch.cc/recipient-groups/929` | 200 | 없음 | 생성 그룹 메타 반환 | 상세 페이지 `/segments/929` 진입 확인 |
| B-3 생성 후 수신자 초기조회 | 생성 직후 상세 | GET | `https://api.recatch.cc/recipient-groups/929/recipients?page_count=50` | 200 | 없음 | 초기 수신자 0건 | 생성 직후 기본 상태 확인 |
| C-1 수신자 후보 모달 | 상세에서 `수신자` 클릭 | GET | `https://api.recatch.cc/sales-entity/deal/record-types` | 200 | 없음 | 딜 유형 목록 반환 | 모달 필터 보조 데이터 |
| C-2 수신자 후보 로드 | 수신자 후보 모달 오픈 | POST | `https://api.recatch.cc/sales-entity/lead-deal-combined/filter?page_count=50&version=20250923` | 200 | 기본 필터 바디(비어있음) | 후보 리스트 반환 | 모달 첫 로드 핵심 API |
| D-1 필터 UI 오픈 | `필터` > `조건` | - | - | - | - | - | UI 팝업만 확인, 추가 네트워크 호출 미관측 |
| D-2 필터 초기화 | `모든 필터 삭제` | - | - | - | - | - | 본 세션 로깅 기준 네트워크 호출 미관측 |
| E-1 삭제 모달 호출 | 목록 행 액션 `삭제` 클릭 | - | - | - | - | - | 2차 모달 문구/버튼 확인 (`아니요`, `네, 삭제할게요.`) |
| E-2 삭제 취소 분기 | 모달에서 `아니요` | - | - | - | - | - | 목록 유지, 네트워크 호출 미관측 |
| E-3 삭제 확정 분기 | 모달에서 `네, 삭제할게요.` | DELETE | `https://api.recatch.cc/recipient-groups/929` | 200 | 없음 | 삭제 성공 | 이번 세션 생성 그룹만 삭제 |
| E-4 삭제 후 검증 | 새로고침 후 목록 확인 | GET | `https://api.recatch.cc/recipient-groups` | 200 | 없음 | 목록 재반환 | 최상단이 `2026. 02. 06` 행으로 변경, 생성 그룹 미노출 |

검증 스크린샷:
- `C:/Users/syh/Pictures/Vibium/recatch-delete-second-confirm-modal-visible.png`
- `C:/Users/syh/Pictures/Vibium/recatch-after-delete-refresh-check.png`
