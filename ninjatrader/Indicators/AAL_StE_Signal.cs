// =============================================================================
// AAL_StE_Signal — Stochastic Extreme Signal (NinjaTrader 8) v1.2
// =============================================================================
// 포팅 원본: MNQ_5m_Chart_v3.pine 의 sig_l3 / sig_s2
// 강화 근거: .gongbang/research/v34_forensics_findings.md §10, §11, §15, §22.3
//            (10y NQ 5m, 2016-05 ~ 2026-04, 278k bars)
//
// =============================================================================
// v1.2 변경 (2026-05-02)
// =============================================================================
//   - TF guard 추가: 5m TF 가 아니면 Log warning (Forensics 5m 전제)
//
// v1.1 변경 (2026-04-27)
// =============================================================================
//   1. Stoch Cross 명시 검출 (K vs D crossover) — Pine 원본 동작
//   2. ATR Ratio 계산 (atr14 / SMA(atr14, 20))
//   3. Regime 계산 (BULL/BEAR/MIXED)
//        - EMA200 slope over 288 bars
//        - % bars above EMA200 (last 50)
//   4. L3 Tier A:  atr_ratio > 1.0
//        Forensics: N=309, WR 81.2%, EV +6.48, Sharpe 4.10
//   5. L3 Tier B:  baseline
//        Forensics: N=662, WR 76.1%, EV +4.27, Sharpe 2.84
//   6. S2 Tier A:  atr_ratio > 1.0 + regime != MIXED
//        Forensics: N=604, WR 78.6%, EV +7.63, Sharpe 4.43 ⭐
//   7. S2 Tier B:  baseline (참고용 표시)
//        Forensics: N=4392, WR 74.0%, EV +4.43, Sharpe 2.50
//   8. Thursday L3 SKIP (Sharpe -0.75)
//        Source: §15.5 day_of_week.csv
//   9. Visual 차등 (Tier A = 큰 ▲▼ + bright, Tier B = 작은 ▲▼ + dark)
//  10. Alert: Tier A 만 default (AlertOnTierA), Tier B 별도 toggle
//
// ATM 매핑:
//   L3 (LONG):  BURN_REV (SL 280 / Trail 32 / Step 4 / Freq 4 ticks = 70/8/1pt)
//   S2 (SHORT): BURN_S   (SL 320 / Trail 16 / Step 4 / Freq 4 ticks = 80/4/1pt)
//
// Hold cap: 30 min (Forensics §15.2 — 5m 신호 30min 거의 동등)
//
// 설치:
//   1. NT8 → New → NinjaScript Editor
//   2. Indicators 우클릭 → New Indicator → 이름: AAL_StE_Signal
//   3. 빈 파일 전체 삭제 → 본 파일 전체 복붙 → F5
//   4. 차트 → Indicators → "AAL_StE_Signal" → Add
// =============================================================================

#region Using declarations
using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Windows.Media;
using NinjaTrader.Cbi;
using NinjaTrader.Data;          // v1.2: BarsPeriodType 위해 필요 (TF guard)
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.DrawingTools;
#endregion

namespace NinjaTrader.NinjaScript.Indicators
{
	public class AAL_StE_Signal : Indicator
	{
		#region Parameters — Stochastic
		[NinjaScriptProperty]
		[Range(5, 30)]
		[Display(Name = "Stoch Period", Order = 1, GroupName = "1. Stochastic")]
		public int StochPeriod { get; set; }

		[NinjaScriptProperty]
		[Range(1, 5)]
		[Display(Name = "Stoch K Smooth", Order = 2, GroupName = "1. Stochastic")]
		public int StochK { get; set; }

		[NinjaScriptProperty]
		[Range(1, 5)]
		[Display(Name = "Stoch D Smooth", Order = 3, GroupName = "1. Stochastic")]
		public int StochD { get; set; }

		[NinjaScriptProperty]
		[Range(10, 40)]
		[Display(Name = "Oversold Threshold", Order = 4, GroupName = "2. Thresholds")]
		public int Oversold { get; set; }

		[NinjaScriptProperty]
		[Range(60, 90)]
		[Display(Name = "Overbought Threshold", Order = 5, GroupName = "2. Thresholds")]
		public int Overbought { get; set; }
		#endregion

		#region Parameters — Filter
		[NinjaScriptProperty]
		[Range(0.0, 2.0)]
		[Display(Name = "Near EMA Threshold (ATR x)", Order = 6, GroupName = "3. Filter")]
		public double NearEmaAtrMult { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Enforce Session Active (KST 20:30~05:00)", Order = 7, GroupName = "3. Filter")]
		public bool SessionActiveOnly { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Require Stoch Cross (K x D)", Order = 8, GroupName = "3. Filter")]
		public bool RequireCross { get; set; }
		#endregion

		#region Parameters — Tier (v1.1 신규)
		[NinjaScriptProperty]
		[Range(0.5, 3.0)]
		[Display(Name = "Tier A — ATR Ratio Min", Order = 9, GroupName = "4. Tier (v1.1)")]
		[Description("Tier A 자격: atr14 / SMA(atr14, 20) >= 이 값. Forensics 기준 1.0 (L3 Sharpe 4.10 / S2 Sharpe 4.43).")]
		public double TierAAtrRatioMin { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Tier A — S2 Require non-MIXED Regime", Order = 10, GroupName = "4. Tier (v1.1)")]
		[Description("S2(SHORT) Tier A 추가 조건. Forensics: regime!=MIXED 시 Sharpe 4.43, regime_all 3.04.")]
		public bool TierAS2NonMixedRegime { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Skip L3 on Thursday", Order = 11, GroupName = "4. Tier (v1.1)")]
		[Description("Forensics §15.5: l3_stE_up Thursday Sharpe -0.75. KST Thursday 종일 L3 차단.")]
		public bool SkipL3Thursday { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show Tier B (작은 화살표)", Order = 12, GroupName = "4. Tier (v1.1)")]
		public bool ShowTierB { get; set; }
		#endregion

		#region Parameters — Alerts
		[NinjaScriptProperty]
		[Display(Name = "Alert on Tier A fire", Order = 13, GroupName = "5. Alerts")]
		public bool AlertOnTierA { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on Tier B fire", Order = 14, GroupName = "5. Alerts")]
		public bool AlertOnTierB { get; set; }
		#endregion

		#region Indicators
		private Stochastics stoch;
		private EMA ema20, ema50, ema200;
		private SMA ma20, atrSma20;
		private StdDev sd20;
		private ATR atr14;
		#endregion

		protected override void OnStateChange()
		{
			if (State == State.SetDefaults)
			{
				Description   = "AAL StE v1.1 — Pine L3/S2 + Tier A/B + Thursday SKIP + Regime (Forensics §22.3)";
				Name          = "AAL_StE_Signal";
				Calculate     = Calculate.OnBarClose;
				IsOverlay     = true;
				DisplayInDataBox = false;
				DrawOnPricePanel = true;
				PaintPriceMarkers = false;

				// Stochastic
				StochPeriod    = 14;
				StochK         = 3;
				StochD         = 3;
				Oversold       = 20;
				Overbought     = 80;

				// Filter
				NearEmaAtrMult    = 1.0;
				SessionActiveOnly = true;
				RequireCross      = true;

				// Tier (v1.1)
				TierAAtrRatioMin       = 1.0;
				TierAS2NonMixedRegime  = true;
				SkipL3Thursday         = true;
				ShowTierB              = true;

				// Alerts
				AlertOnTierA = true;
				AlertOnTierB = false;
			}
			else if (State == State.DataLoaded)
			{
				// v1.2: TF guard — Forensics 가 5m 전제
				if (BarsPeriod.BarsPeriodType != BarsPeriodType.Minute || BarsPeriod.Value != 5)
				{
					Print(string.Format(
						"⚠ AAL_StE_Signal: 5m TF 전제 (Forensics 검증). 현재 차트 TF = {0} {1}. " +
						"신호 신뢰도 보장 안 됨.",
						BarsPeriod.BarsPeriodType, BarsPeriod.Value));
				}

				stoch    = Stochastics(StochK, StochPeriod, StochD);
				ema20    = EMA(20);
				ema50    = EMA(50);
				ema200   = EMA(200);
				ma20     = SMA(20);
				sd20     = StdDev(20);
				atr14    = ATR(14);
				atrSma20 = SMA(atr14, 20);
			}
		}

		protected override void OnBarUpdate()
		{
			// EMA200 slope 288 + above-ratio 50 → 충분히 워밍업
			if (CurrentBar < 290) return;

			// --- Stochastic K, D ---
			double k     = stoch.K[0];
			double d     = stoch.D[0];
			double kPrev = stoch.K[1];
			double dPrev = stoch.D[1];

			bool crossUp   = kPrev <= dPrev && k > d;   // bullish cross (L3)
			bool crossDown = kPrev >= dPrev && k < d;   // bearish cross (S2)

			// --- EMA trend ---
			bool emaUp   = ema20[0] > ema50[0] && ema50[0] > ema200[0];
			bool emaDown = ema20[0] < ema50[0] && ema50[0] < ema200[0];

			// --- Near EMA20 ---
			double distToEma = Math.Abs(Close[0] - ema20[0]);
			double threshold = atr14[0] * NearEmaAtrMult;
			bool nearEma = distToEma <= threshold;

			// --- Session Active (KST 20:30 ~ 05:00) ---
			DateTime kst = Time[0].ToUniversalTime().AddHours(9);
			int kstHm = kst.Hour * 100 + kst.Minute;
			bool sessionActive = (kstHm >= 2030) || (kstHm < 500);

			// --- Day of Week (KST 기준) ---
			bool isThursdayKst = kst.DayOfWeek == DayOfWeek.Thursday;

			// --- ATR Ratio (v1.1) ---
			double atrRatio = atrSma20[0] > 0.0001 ? atr14[0] / atrSma20[0] : 0.0;

			// --- Regime (v1.1) ---
			//   slope: EMA200 % change over 288 bars (5m × 288 = 24h)
			//   above: % of last 50 bars where Close > EMA200
			//   BULL : slope > +0.10% AND above >= 70%
			//   BEAR : slope < -0.10% AND above <= 30%
			//   else : MIXED
			double slope = (ema200[0] - ema200[288]) / ema200[288] * 100.0;
			int aboveCnt = 0;
			for (int i = 0; i < 50; i++)
				if (Close[i] > ema200[i]) aboveCnt++;
			double abovePct = aboveCnt * 100.0 / 50.0;

			string regime;
			if      (slope >  0.10 && abovePct >= 70) regime = "BULL";
			else if (slope < -0.10 && abovePct <= 30) regime = "BEAR";
			else                                       regime = "MIXED";

			// --- MED vol (참고용, S2 표시에 활용) ---
			double bbWidth = 0.0;
			if (ma20[0] > 0.0001)
			{
				double bbUp = ma20[0] + 2.0 * sd20[0];
				double bbLo = ma20[0] - 2.0 * sd20[0];
				bbWidth = (bbUp - bbLo) / ma20[0] * 100.0;
			}

			// ═══════════════════════════ L3 (LONG) ═══════════════════════════

			bool l3Base = k < Oversold
			           && (!RequireCross || crossUp)
			           && nearEma
			           && emaUp
			           && (!SessionActiveOnly || sessionActive);

			// Thursday SKIP (l3_stE_up Sharpe -0.75)
			if (SkipL3Thursday && isThursdayKst) l3Base = false;

			bool l3TierA = l3Base && atrRatio >= TierAAtrRatioMin;
			bool l3TierB = l3Base && !l3TierA;

			if (l3TierA)
			{
				Draw.ArrowUp(this, "L3A_" + CurrentBar, true, 0,
					Low[0] - atr14[0] * 0.5, Brushes.Lime);
				Draw.Text(this, "L3Atxt_" + CurrentBar,
					string.Format("L3 A\nATR {0:F2}\n{1}", atrRatio, regime),
					0, Low[0] - atr14[0] * 1.2, Brushes.Lime);

				if (AlertOnTierA)
					Alert("AAL_StE_L3A", Priority.High,
						string.Format("L3 Tier A FIRE - Close {0:F2}, K {1:F1}, ATR {2:F2}, {3}",
							Close[0], k, atrRatio, regime),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert1.wav",
						10, Brushes.Black, Brushes.Lime);
			}
			else if (l3TierB && ShowTierB)
			{
				Draw.ArrowUp(this, "L3B_" + CurrentBar, true, 0,
					Low[0] - atr14[0] * 0.4, Brushes.DarkGreen);
				Draw.Text(this, "L3Btxt_" + CurrentBar, "L3 B",
					0, Low[0] - atr14[0] * 0.9, Brushes.DarkGreen);

				if (AlertOnTierB)
					Alert("AAL_StE_L3B", Priority.Medium,
						string.Format("L3 Tier B - Close {0:F2}, K {1:F1}", Close[0], k),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert2.wav",
						5, Brushes.White, Brushes.DarkGreen);
			}

			// ═══════════════════════════ S2 (SHORT) ═══════════════════════════

			bool s2Base = k > Overbought
			           && (!RequireCross || crossDown)
			           && nearEma
			           && emaDown
			           && (!SessionActiveOnly || sessionActive);

			bool s2TierA = s2Base && atrRatio >= TierAAtrRatioMin
			            && (!TierAS2NonMixedRegime || regime != "MIXED");
			bool s2TierB = s2Base && !s2TierA;

			if (s2TierA)
			{
				Draw.ArrowDown(this, "S2A_" + CurrentBar, true, 0,
					High[0] + atr14[0] * 0.5, Brushes.Red);
				Draw.Text(this, "S2Atxt_" + CurrentBar,
					string.Format("S2 A\nATR {0:F2}\n{1}", atrRatio, regime),
					0, High[0] + atr14[0] * 1.2, Brushes.Red);

				if (AlertOnTierA)
					Alert("AAL_StE_S2A", Priority.High,
						string.Format("S2 Tier A FIRE (SHORT) - Close {0:F2}, K {1:F1}, ATR {2:F2}, {3}",
							Close[0], k, atrRatio, regime),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert2.wav",
						10, Brushes.White, Brushes.Red);
			}
			else if (s2TierB && ShowTierB)
			{
				Draw.ArrowDown(this, "S2B_" + CurrentBar, true, 0,
					High[0] + atr14[0] * 0.4, Brushes.DarkRed);
				Draw.Text(this, "S2Btxt_" + CurrentBar, "S2 B",
					0, High[0] + atr14[0] * 0.9, Brushes.DarkRed);

				if (AlertOnTierB)
					Alert("AAL_StE_S2B", Priority.Medium,
						string.Format("S2 Tier B - Close {0:F2}, K {1:F1}", Close[0], k),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert3.wav",
						5, Brushes.White, Brushes.DarkRed);
			}
		}
	}
}

// =============================================================================
// Forensics 메타정보 요약 (10y NQ 5m, 2,626~10k+ signals)
//
//   L3 (LONG):
//     Tier A (atr_ratio>1.0): N=309, WR 81.2%, EV +6.48, Sharpe 4.10
//     Tier B (baseline):       N=662, WR 76.1%, EV +4.27, Sharpe 2.84
//
//   S2 (SHORT):
//     Tier A (atr>1.0 + non-MIXED): N=604, WR 78.6%, EV +7.63, Sharpe 4.43 ⭐
//     Tier B (baseline):             N=4392, WR 74.0%, EV +4.43, Sharpe 2.50
//
//   Thursday L3 SKIP: Sharpe -0.75 (day_of_week.csv 검증)
//
//   Walk-Forward (16-19 / 19-22 / 22-26):
//     L3:  0.48 / 2.08 / 5.24  (Stdev 2.42 — 시기 의존성 큼)
//     S2: -0.10 / 2.38 / 3.74  (Stdev 1.95 — 최근 강함)
//
// 운영 권고:
//   - Tier A 만 진입, Tier B 는 시각만 (학습용)
//   - L3 + AAL_BullOB_R41A 동시 발생 0회 (mutually exclusive)
//   - S2 + slot_RTH_pre 21:55/22:25 KST = Forensics top slot
//   - ATM Templates: L3 → BURN_REV (70/8/1pt), S2 → BURN_S (80/4/1pt)
//
// 의존: AAL_Shared.cs (enum 미사용, 본 파일은 standalone)
// =============================================================================

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private AAL_StE_Signal[] cacheAAL_StE_Signal;
		public AAL_StE_Signal AAL_StE_Signal(int stochPeriod, int stochK, int stochD, int oversold, int overbought, double nearEmaAtrMult, bool sessionActiveOnly, bool requireCross, double tierAAtrRatioMin, bool tierAS2NonMixedRegime, bool skipL3Thursday, bool showTierB, bool alertOnTierA, bool alertOnTierB)
		{
			return AAL_StE_Signal(Input, stochPeriod, stochK, stochD, oversold, overbought, nearEmaAtrMult, sessionActiveOnly, requireCross, tierAAtrRatioMin, tierAS2NonMixedRegime, skipL3Thursday, showTierB, alertOnTierA, alertOnTierB);
		}

		public AAL_StE_Signal AAL_StE_Signal(ISeries<double> input, int stochPeriod, int stochK, int stochD, int oversold, int overbought, double nearEmaAtrMult, bool sessionActiveOnly, bool requireCross, double tierAAtrRatioMin, bool tierAS2NonMixedRegime, bool skipL3Thursday, bool showTierB, bool alertOnTierA, bool alertOnTierB)
		{
			if (cacheAAL_StE_Signal != null)
				for (int idx = 0; idx < cacheAAL_StE_Signal.Length; idx++)
					if (cacheAAL_StE_Signal[idx] != null && cacheAAL_StE_Signal[idx].StochPeriod == stochPeriod && cacheAAL_StE_Signal[idx].StochK == stochK && cacheAAL_StE_Signal[idx].StochD == stochD && cacheAAL_StE_Signal[idx].Oversold == oversold && cacheAAL_StE_Signal[idx].Overbought == overbought && cacheAAL_StE_Signal[idx].NearEmaAtrMult == nearEmaAtrMult && cacheAAL_StE_Signal[idx].SessionActiveOnly == sessionActiveOnly && cacheAAL_StE_Signal[idx].RequireCross == requireCross && cacheAAL_StE_Signal[idx].TierAAtrRatioMin == tierAAtrRatioMin && cacheAAL_StE_Signal[idx].TierAS2NonMixedRegime == tierAS2NonMixedRegime && cacheAAL_StE_Signal[idx].SkipL3Thursday == skipL3Thursday && cacheAAL_StE_Signal[idx].ShowTierB == showTierB && cacheAAL_StE_Signal[idx].AlertOnTierA == alertOnTierA && cacheAAL_StE_Signal[idx].AlertOnTierB == alertOnTierB && cacheAAL_StE_Signal[idx].EqualsInput(input))
						return cacheAAL_StE_Signal[idx];
			return CacheIndicator<AAL_StE_Signal>(new AAL_StE_Signal(){ StochPeriod = stochPeriod, StochK = stochK, StochD = stochD, Oversold = oversold, Overbought = overbought, NearEmaAtrMult = nearEmaAtrMult, SessionActiveOnly = sessionActiveOnly, RequireCross = requireCross, TierAAtrRatioMin = tierAAtrRatioMin, TierAS2NonMixedRegime = tierAS2NonMixedRegime, SkipL3Thursday = skipL3Thursday, ShowTierB = showTierB, AlertOnTierA = alertOnTierA, AlertOnTierB = alertOnTierB }, input, ref cacheAAL_StE_Signal);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.AAL_StE_Signal AAL_StE_Signal(int stochPeriod, int stochK, int stochD, int oversold, int overbought, double nearEmaAtrMult, bool sessionActiveOnly, bool requireCross, double tierAAtrRatioMin, bool tierAS2NonMixedRegime, bool skipL3Thursday, bool showTierB, bool alertOnTierA, bool alertOnTierB)
		{
			return indicator.AAL_StE_Signal(Input, stochPeriod, stochK, stochD, oversold, overbought, nearEmaAtrMult, sessionActiveOnly, requireCross, tierAAtrRatioMin, tierAS2NonMixedRegime, skipL3Thursday, showTierB, alertOnTierA, alertOnTierB);
		}

		public Indicators.AAL_StE_Signal AAL_StE_Signal(ISeries<double> input , int stochPeriod, int stochK, int stochD, int oversold, int overbought, double nearEmaAtrMult, bool sessionActiveOnly, bool requireCross, double tierAAtrRatioMin, bool tierAS2NonMixedRegime, bool skipL3Thursday, bool showTierB, bool alertOnTierA, bool alertOnTierB)
		{
			return indicator.AAL_StE_Signal(input, stochPeriod, stochK, stochD, oversold, overbought, nearEmaAtrMult, sessionActiveOnly, requireCross, tierAAtrRatioMin, tierAS2NonMixedRegime, skipL3Thursday, showTierB, alertOnTierA, alertOnTierB);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.AAL_StE_Signal AAL_StE_Signal(int stochPeriod, int stochK, int stochD, int oversold, int overbought, double nearEmaAtrMult, bool sessionActiveOnly, bool requireCross, double tierAAtrRatioMin, bool tierAS2NonMixedRegime, bool skipL3Thursday, bool showTierB, bool alertOnTierA, bool alertOnTierB)
		{
			return indicator.AAL_StE_Signal(Input, stochPeriod, stochK, stochD, oversold, overbought, nearEmaAtrMult, sessionActiveOnly, requireCross, tierAAtrRatioMin, tierAS2NonMixedRegime, skipL3Thursday, showTierB, alertOnTierA, alertOnTierB);
		}

		public Indicators.AAL_StE_Signal AAL_StE_Signal(ISeries<double> input , int stochPeriod, int stochK, int stochD, int oversold, int overbought, double nearEmaAtrMult, bool sessionActiveOnly, bool requireCross, double tierAAtrRatioMin, bool tierAS2NonMixedRegime, bool skipL3Thursday, bool showTierB, bool alertOnTierA, bool alertOnTierB)
		{
			return indicator.AAL_StE_Signal(input, stochPeriod, stochK, stochD, oversold, overbought, nearEmaAtrMult, sessionActiveOnly, requireCross, tierAAtrRatioMin, tierAS2NonMixedRegime, skipL3Thursday, showTierB, alertOnTierA, alertOnTierB);
		}
	}
}

#endregion
