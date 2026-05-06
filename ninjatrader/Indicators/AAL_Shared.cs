// =============================================================================
// AAL Shared — 공통 enum (NinjaTrader 8) v1.1
// =============================================================================
// 역할: AAL_SignalLight / AAL_HoldTimer / AAL_StE_Signal 등 여러 indicator 가
//       공유하는 enum.
//
// ⭐ NT 공식 패턴 (글로벌 scope enum):
//   근거: NT 내장 @BlockVolume.cs, @CandleStickPattern.cs 동일 패턴 사용.
//   원리: NT auto-factory 가 Indicators/Strategies/MarketAnalyzerColumns 3개
//        namespace 에 코드 생성하며 enum 을 bare name 으로 참조.
//        enum 이 namespace 밖 (글로벌 scope) 에 있어야 3곳 모두에서
//        C# 글로벌 scope fallback 으로 해석 성공.
//
// 실패했던 접근 (참고용 — 재시도 금지):
//   ❌ class 내부 선언       → Strategies factory 가 AAL_SignalLight.AALMode
//                               qualify 누락 → CS0246
//   ❌ Indicators namespace  → MarketAnalyzerColumns/Strategies 형제 namespace
//                               에서 해석 불가 → CS0246
//   ❌ NinjaScript 부모 NS   → 부모 scope 상속 작동 불확실 + NT 공식 아님
//
// v1.1 변경 (2026-05-02):
//   - AALRegime, AALTier, AALDirection enum 추가
//   - 기존 ad-hoc string ("BULL"/"BEAR"/"MIXED") 비교 → type-safe enum
//
// 설치:
//   NT8 → NinjaScript Editor → Indicators 우클릭 → New Indicator
//   Name: AALShared → Next 연타 → Generate → 빈 파일 전체 삭제 → 이 파일 복붙 → F5
//   (Indicator 가 아니므로 차트 Add 안 됨 — 정상)
//
// 참고: docs/TROUBLESHOOTING_LOG.md — 2026-04-25 CS0246 trouble log
// =============================================================================

public enum AALMode { ACTIVE, PRESET, OFF }

// v1.1 확장 — Forensics regime / Tier / Direction
public enum AALRegime { BULL, BEAR, MIXED }
public enum AALTier { A, B, C }
public enum AALDirection { LONG, SHORT }
