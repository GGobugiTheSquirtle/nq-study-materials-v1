// =============================================================================
// AAL_v5_RoundShort — Round Figure + Pivot High SHORT (NT8) v1.0
// =============================================================================
// Source: Phase G2 (pivot fractal correction) + G3 (288 ATM grid) — 2026-05-06
//
//   Verified P3 (2023+) for R500 up + pivot high break (5-5) SHORT entry
//   with ATM SL 0.3 / Pre-Trail 0.2 / Trail Dist 0.2 ATR (~18/12/12 ticks):
//
//     Profit Factor:   4.559 ⭐⭐⭐⭐⭐ (Total 4.131)
//     Win Rate:        63.2%
//     Expectancy:      +0.41 ATR per trade
//     N (P3):          1,197 trades (~270/year)
//     Cost-adjusted:   0.022 ATR/RT 차감
//
//   G2 distribution edge (forward 24b signed return / ATR, h2y weighted):
//     R500  up + PH:  -0.127 ⭐ best mean revert
//     R1000 up + PH:  -0.085 (P3 -0.223, recent 강함)
//     R500  up alone:  +0.013 (no PH break = no edge)
//
//   Confluence (rare but extreme — N small caveat):
//     KST 21 + R1000 down + PL break: signed h2y -1.250 / l2y -2.626 ATR
//
//   ⚠️ G의 K-Bounce LONG (R1000 down + 전저점) REJECTED:
//     Rolling-max method artifact. Pivot 5-5 정확 detection 시 -0.074 (mild SHORT cont).
//     Don't trade R1000 down + PL as LONG.
//
// 룰 정의 (R500 up + PH break SHORT):
//   1. prev_close < ceil(prev_close/500)*500 + 500 AND high >= that round value
//      = price 가 다음 R500 round figure 위로 돌파
//   2. last confirmed pivot high (5-5) 가 broken (high > last_pivot_high)
//   3. 5m TF 만 (Forensics 검증 timeframe)
//   4. Direction: SHORT (mean revert)
//
// ATM v5.1 권장 (G3 verified, NQ 0.25/tick):
//   Stop Loss:        0.3 × ATR ≈ 18 ticks (NQ ATR ~15pt)
//   Pre-Trail trigger:0.2 × ATR ≈ 12 ticks (BE activation)
//   Trail Distance:   0.2 × ATR ≈ 12 ticks
//   Max Hold:         ~12 bars (1h, trail 빨리 활성)
//
// 시각:
//   Trigger bar:  큰 ▼ orange + "R500↑PH" label
//   Auto label:   ATM ticks 동적 표시 (ATR 기반)
//   Round line:   horizontal yellow dashed @ broken R500 (optional)
//
// 운영 권고:
//   - Live ≠ backtest. Sim PF 4.5 → live 1.5-3.0 추정 (cost/slippage/regime)
//   - Sim 4주 PF < 1.5 시 즉시 중단
//   - Confluence 추가 (KST 21 + R1000 + PL extreme) 발생 시 size up 검토
//
// 의존: AAL_Shared.cs (standalone, enum 미사용)
// 생성: 2026-05-07 (NT_AAL v5.1)
// =============================================================================

#region Using declarations
using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Windows.Media;
using NinjaTrader.Cbi;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.DrawingTools;
#endregion

namespace NinjaTrader.NinjaScript.Indicators
{
	public class AAL_v5_RoundShort : Indicator
	{
		#region Parameters
		[NinjaScriptProperty]
		[Range(50, 2000)]
		[Display(Name = "Round Step (NQ pt)", Order = 1, GroupName = "1. Round Figure")]
		[Description("Best edge: 500. R250/R1000 도 보조 marker.")]
		public double RoundStep { get; set; }

		[NinjaScriptProperty]
		[Range(2, 10)]
		[Display(Name = "Pivot Strength (Left/Right bars)", Order = 2, GroupName = "2. Pivot")]
		[Description("Pivot fractal 좌우 N봉. 5 권장 (G2 verified).")]
		public int PivotStrength { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show R1000 markers (mild SHORT)", Order = 3, GroupName = "3. Display")]
		public bool ShowR1000 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show KST 21 + R1000 + PL extreme (rare)", Order = 4, GroupName = "3. Display")]
		public bool ShowKst21Extreme { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Show ATM v5.1 ticks label", Order = 5, GroupName = "3. Display")]
		public bool ShowAtmLabel { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on R500+PH SHORT (high priority)", Order = 6, GroupName = "4. Alerts")]
		public bool AlertOnR500 { get; set; }

		[NinjaScriptProperty]
		[Display(Name = "Alert on KST21 R1000 PL extreme", Order = 7, GroupName = "4. Alerts")]
		public bool AlertOnExtreme { get; set; }
		#endregion

		#region Indicators / State
		private ATR atr14;
		private double lastPivotHigh = double.NaN;
		private double lastPivotLow = double.NaN;
		#endregion

		protected override void OnStateChange()
		{
			if (State == State.SetDefaults)
			{
				Description = "AAL v5.1 — R500 up + 전고점 break SHORT (G3 P3 PF 4.56)";
				Name = "AAL_v5_RoundShort";
				Calculate = Calculate.OnBarClose;
				IsOverlay = true;
				DisplayInDataBox = false;
				DrawOnPricePanel = true;
				PaintPriceMarkers = false;

				RoundStep = 500;
				PivotStrength = 5;
				ShowR1000 = true;
				ShowKst21Extreme = true;
				ShowAtmLabel = true;
				AlertOnR500 = true;
				AlertOnExtreme = true;
			}
			else if (State == State.DataLoaded)
			{
				if (BarsPeriod.BarsPeriodType != BarsPeriodType.Minute || BarsPeriod.Value != 5)
				{
					Print(string.Format(
						"⚠ AAL_v5_RoundShort: 5m TF 전제 (G2/G3 검증). 현재 차트 TF = {0} {1}. 신호 신뢰도 보장 안 됨.",
						BarsPeriod.BarsPeriodType, BarsPeriod.Value));
				}
				atr14 = ATR(14);
			}
		}

		protected override void OnBarUpdate()
		{
			int n = PivotStrength;
			if (CurrentBar < n * 2 + 5) return;

			// === Update last confirmed pivots (5-5 fractal) ===
			//   Pivot at bar (CurrentBar - n) is confirmed at CurrentBar
			//   if it was max/min in window [CurrentBar-2n, CurrentBar]
			int pivotBar = CurrentBar - n;
			bool isPivotHigh = true;
			bool isPivotLow = true;
			double phPrice = High[n];
			double plPrice = Low[n];
			for (int i = 0; i <= 2 * n; i++)
			{
				if (i == n) continue;
				if (High[i] >= phPrice) isPivotHigh = false;
				if (Low[i] <= plPrice) isPivotLow = false;
			}
			if (isPivotHigh) lastPivotHigh = phPrice;
			if (isPivotLow)  lastPivotLow  = plPrice;

			// === Round Figure cross detection (gap-safe, prev_close ref) ===
			double prevClose = Close[1];
			double r500Above = Math.Floor(prevClose / RoundStep) * RoundStep + RoundStep;
			double r500Below = Math.Ceiling(prevClose / RoundStep) * RoundStep - RoundStep;
			double r1000Above = Math.Floor(prevClose / 1000.0) * 1000.0 + 1000.0;
			double r1000Below = Math.Ceiling(prevClose / 1000.0) * 1000.0 - 1000.0;

			bool crossed500Up    = High[0] >= r500Above  && prevClose < r500Above;
			bool crossed1000Up   = High[0] >= r1000Above && prevClose < r1000Above;
			bool crossed1000Down = Low[0]  <= r1000Below && prevClose > r1000Below;

			// === Pivot break (require pivot exists) ===
			bool brokePivotHigh = !double.IsNaN(lastPivotHigh) && High[0] > lastPivotHigh;
			bool brokePivotLow  = !double.IsNaN(lastPivotLow)  && Low[0]  < lastPivotLow;

			// === KST hour (UTC + 9) ===
			DateTime kst = Time[0].ToUniversalTime().AddHours(9);
			int kstH = kst.Hour;
			int kstM = kst.Minute;

			// === ATM v5.1 ticks (NQ 0.25/tick → 4 ticks/pt) ===
			int slTicks    = (int)Math.Round(0.3 * atr14[0] * 4.0);
			int trailTicks = (int)Math.Round(0.2 * atr14[0] * 4.0);

			// =========================================================
			// 🔴 R500 up + Pivot High break → SHORT (G3 P3 PF 4.56)
			// =========================================================
			if (crossed500Up && brokePivotHigh)
			{
				Draw.ArrowDown(this, "R500PH_" + CurrentBar, true, 0,
					High[0] + atr14[0] * 0.5, Brushes.Orange);

				string atmText = ShowAtmLabel
					? string.Format("🔴 R500↑PH SHORT\nATM: SL {0}t / Trail {1}t / TD {2}t\n(0.3/0.2/0.2 ATR · ATR={3:F2})",
						slTicks, trailTicks, trailTicks, atr14[0])
					: "🔴 R500↑PH SHORT";

				Draw.Text(this, "R500PHtxt_" + CurrentBar, atmText,
					0, High[0] + atr14[0] * 1.4, Brushes.Orange);

				// Round value horizontal line
				Draw.HorizontalLine(this, "R500line_" + CurrentBar, r500Above,
					Brushes.Yellow, DashStyleHelper.Dash, 1);

				if (AlertOnR500)
					Alert("AAL_v51_R500_SHORT", Priority.High,
						string.Format("R500 up + 전고점 break → SHORT FIRE (G3 P3 PF 4.56). Close {0:F2}, R500 {1:F2}, PH {2:F2}, ATM {3}t/Trail {4}t",
							Close[0], r500Above, lastPivotHigh, slTicks, trailTicks),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert2.wav",
						15, Brushes.White, Brushes.Orange);
			}

			// =========================================================
			// R1000 markers (mild SHORT, less robust — 보조 신호)
			// =========================================================
			if (ShowR1000 && crossed1000Up && brokePivotHigh)
			{
				Draw.ArrowDown(this, "R1k_PH_" + CurrentBar, true, 0,
					High[0] + atr14[0] * 0.4,
					Brushes.Magenta);
				Draw.Text(this, "R1kPHtxt_" + CurrentBar, "R1k↑PH",
					0, High[0] + atr14[0] * 1.0, Brushes.Magenta);
			}

			if (ShowR1000 && crossed1000Down && brokePivotLow)
			{
				// G2 verified: NOT a LONG bounce (G's K-Bounce REJECTED)
				// Mild SHORT continuation. Marker only.
				Draw.Dot(this, "R1kPL_" + CurrentBar, true, 0,
					Low[0] - atr14[0] * 0.3, Brushes.Gray);
				Draw.Text(this, "R1kPLtxt_" + CurrentBar, "R1k↓PL\n(NOT bounce)",
					0, Low[0] - atr14[0] * 1.0, Brushes.Silver);
			}

			// =========================================================
			// 💀 KST 21 + R1000 down + PL extreme SHORT (rare, N=150)
			// =========================================================
			if (ShowKst21Extreme && kstH == 21 && kstM < 5
				&& crossed1000Down && brokePivotLow)
			{
				Draw.ArrowDown(this, "KST21X_" + CurrentBar, true, 0,
					High[0] + atr14[0] * 1.2, Brushes.Red);
				Draw.Text(this, "KST21Xtxt_" + CurrentBar,
					"💀 KST21+R1k+PL\nSHORT EXTREME\nN=150 / 10y\nl2y -2.6 ATR",
					0, High[0] + atr14[0] * 2.5, Brushes.Red);

				if (AlertOnExtreme)
					Alert("AAL_v51_KST21_R1k_extreme", Priority.High,
						string.Format("💀 KST 21 + R1000 down + Pivot Low break → SHORT EXTREME (G2 l2y -2.6 ATR, rare). Close {0:F2}",
							Close[0]),
						NinjaTrader.Core.Globals.InstallDir + @"\sounds\Alert4.wav",
						20, Brushes.White, Brushes.DarkRed);
			}
		}
	}
}

// =============================================================================
// G2 / G3 Forensics 요약
//
//   G2 — Pivot fractal correction (rolling max → 5-5 pivot):
//     R500 up + PH:  signed h2y -0.127, l2y -0.191, P3 -0.109 (모두 robust SHORT)
//     R1000 up + PH: signed h2y -0.085, P3 -0.223 (recent 강함)
//     R1000 down + PL: signed h2y -0.074 (G's "K-Bounce" artifact 였음, 진짜 mild SHORT cont)
//
//   G3 — ATM 288-grid optimization (R500 up + PH SHORT):
//     Top 1: SL 0.3 / PT 0.2 / TD 0.2 / H 12-48 → P3 PF 4.559, WR 63.2%
//     Top 5: SL 0.3 / PT 0.3 / TD 0.2 → P3 PF 3.997
//     SL 0.5 best: PF 2.943
//     SL 1.0 (default): PF 2.051 (vs 0.3 = +0.108)
//
//   Caveat:
//     - 288 grid cherry-pick — best params 선택 효과
//     - Recent regime 의존 (P3 > Total 4.13)
//     - Live ≠ backtest, cost/slippage 미세
//     - Sim 4주 PF < 1.5 시 즉시 중단
//
// 의존: AAL_Shared.cs
// =============================================================================

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private AAL_v5_RoundShort[] cacheAAL_v5_RoundShort;
		public AAL_v5_RoundShort AAL_v5_RoundShort(double roundStep, int pivotStrength, bool showR1000, bool showKst21Extreme, bool showAtmLabel, bool alertOnR500, bool alertOnExtreme)
		{
			return AAL_v5_RoundShort(Input, roundStep, pivotStrength, showR1000, showKst21Extreme, showAtmLabel, alertOnR500, alertOnExtreme);
		}

		public AAL_v5_RoundShort AAL_v5_RoundShort(ISeries<double> input, double roundStep, int pivotStrength, bool showR1000, bool showKst21Extreme, bool showAtmLabel, bool alertOnR500, bool alertOnExtreme)
		{
			if (cacheAAL_v5_RoundShort != null)
				for (int idx = 0; idx < cacheAAL_v5_RoundShort.Length; idx++)
					if (cacheAAL_v5_RoundShort[idx] != null && cacheAAL_v5_RoundShort[idx].RoundStep == roundStep && cacheAAL_v5_RoundShort[idx].PivotStrength == pivotStrength && cacheAAL_v5_RoundShort[idx].ShowR1000 == showR1000 && cacheAAL_v5_RoundShort[idx].ShowKst21Extreme == showKst21Extreme && cacheAAL_v5_RoundShort[idx].ShowAtmLabel == showAtmLabel && cacheAAL_v5_RoundShort[idx].AlertOnR500 == alertOnR500 && cacheAAL_v5_RoundShort[idx].AlertOnExtreme == alertOnExtreme && cacheAAL_v5_RoundShort[idx].EqualsInput(input))
						return cacheAAL_v5_RoundShort[idx];
			return CacheIndicator<AAL_v5_RoundShort>(new AAL_v5_RoundShort(){ RoundStep = roundStep, PivotStrength = pivotStrength, ShowR1000 = showR1000, ShowKst21Extreme = showKst21Extreme, ShowAtmLabel = showAtmLabel, AlertOnR500 = alertOnR500, AlertOnExtreme = alertOnExtreme }, input, ref cacheAAL_v5_RoundShort);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.AAL_v5_RoundShort AAL_v5_RoundShort(double roundStep, int pivotStrength, bool showR1000, bool showKst21Extreme, bool showAtmLabel, bool alertOnR500, bool alertOnExtreme)
		{
			return indicator.AAL_v5_RoundShort(Input, roundStep, pivotStrength, showR1000, showKst21Extreme, showAtmLabel, alertOnR500, alertOnExtreme);
		}

		public Indicators.AAL_v5_RoundShort AAL_v5_RoundShort(ISeries<double> input, double roundStep, int pivotStrength, bool showR1000, bool showKst21Extreme, bool showAtmLabel, bool alertOnR500, bool alertOnExtreme)
		{
			return indicator.AAL_v5_RoundShort(input, roundStep, pivotStrength, showR1000, showKst21Extreme, showAtmLabel, alertOnR500, alertOnExtreme);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.AAL_v5_RoundShort AAL_v5_RoundShort(double roundStep, int pivotStrength, bool showR1000, bool showKst21Extreme, bool showAtmLabel, bool alertOnR500, bool alertOnExtreme)
		{
			return indicator.AAL_v5_RoundShort(Input, roundStep, pivotStrength, showR1000, showKst21Extreme, showAtmLabel, alertOnR500, alertOnExtreme);
		}

		public Indicators.AAL_v5_RoundShort AAL_v5_RoundShort(ISeries<double> input, double roundStep, int pivotStrength, bool showR1000, bool showKst21Extreme, bool showAtmLabel, bool alertOnR500, bool alertOnExtreme)
		{
			return indicator.AAL_v5_RoundShort(input, roundStep, pivotStrength, showR1000, showKst21Extreme, showAtmLabel, alertOnR500, alertOnExtreme);
		}
	}
}

#endregion
