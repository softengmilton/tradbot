from typing import Dict, List
from analysis.indicators import ema, rsi, macd, atr
from analysis.support_resistance import detect_support_resistance
from analysis.confidence import calculate_confidence

class DefaultAnalyzer:
    def __init__(self, prices_data: Dict[str, List[float]]):
        """
        Args:
            prices_data: {
                "closes": [...],
                "highs": [...],
                "lows": [...],
                "volumes": [...]
            }
        """
        self.closes = prices_data["closes"]
        self.highs = prices_data["highs"]
        self.lows = prices_data["lows"]
        self.volumes = prices_data["volumes"]

    def analyze(self) -> Dict:
        """Run complete analysis"""

        # Calculate all indicators
        ema20 = ema.calculate_ema(self.closes, 20)
        ema50 = ema.calculate_ema(self.closes, 50)
        ema200 = ema.calculate_ema(self.closes, 200)

        rsi14 = rsi.calculate_rsi(self.closes, 14)
        macd_data = macd.calculate_macd(self.closes)
        atr14 = atr.calculate_atr(self.highs, self.lows, self.closes, 14)

        support_res = detect_support_resistance(self.closes)

        # Determine trend
        trend = self._determine_trend(ema20, ema50, ema200)

        # Get signals
        signals = self._generate_signals(ema20, ema50, rsi14, macd_data, atr14)

        # Calculate entry/exit levels
        current_price = self.closes[-1]
        atr_value = atr14[-1] if atr14[-1] else 100

        entry_zone = {
            "min": support_res["support"],
            "max": current_price + (atr_value * 0.5)
        }

        stop_loss = support_res["support"] - (atr_value * 0.5)
        take_profit_1 = current_price + (atr_value * 2)
        take_profit_2 = current_price + (atr_value * 3)

        # Calculate confidence
        confidence = calculate_confidence({
            "trend": trend,
            "signals": signals,
            "rsi": rsi14[-1] if rsi14[-1] else 50,
            "volume_strength": self._assess_volume()
        })

        return {
            "mode": "default",
            "trend": trend,
            "confidence": confidence,
            "entry_zone": entry_zone,
            "stop_loss": round(stop_loss, 2),
            "take_profit_1": round(take_profit_1, 2),
            "take_profit_2": round(take_profit_2, 2),
            "support": support_res["support"],
            "resistance": support_res["resistance"],
            "signals": signals,
            "indicators": {
                "ema20": round(ema20[-1], 2) if ema20[-1] else 0,
                "ema50": round(ema50[-1], 2) if ema50[-1] else 0,
                "ema200": round(ema200[-1], 2) if ema200[-1] else 0,
                "rsi": round(rsi14[-1], 2) if rsi14[-1] else 0,
                "atr": round(atr_value, 2)
            }
        }

    def _determine_trend(self, ema20, ema50, ema200):
        # Bullish: 20 > 50 > 200
        # Bearish: 20 < 50 < 200
        # Neutral: Mixed
        e20 = ema20[-1] if ema20[-1] else 0
        e50 = ema50[-1] if ema50[-1] else 0
        e200 = ema200[-1] if ema200[-1] else 0

        if e20 > e50 > e200:
            return "STRONG_BULLISH"
        elif e20 > e50 and e50 < e200:
            return "WEAK_BULLISH"
        elif e20 < e50 < e200:
            return "STRONG_BEARISH"
        elif e20 < e50 and e50 > e200:
            return "WEAK_BEARISH"
        else:
            return "NEUTRAL"

    def _generate_signals(self, ema20, ema50, rsi14, macd_data, atr14):
        signals = []

        # EMA signals
        if ema20[-1] and ema50[-1] and ema20[-1] > ema50[-1]:
            signals.append("EMA20 > EMA50")

        # RSI signals
        if rsi14[-1]:
            if rsi14[-1] > 60:
                signals.append("RSI Bullish")
            elif rsi14[-1] < 40:
                signals.append("RSI Bearish")

        return signals

    def _assess_volume(self):
        avg_volume = sum(self.volumes[-20:]) / 20 if len(self.volumes) >= 20 else sum(self.volumes) / len(self.volumes)
        current_volume = self.volumes[-1]
        return "ABOVE_AVERAGE" if current_volume > avg_volume else "BELOW_AVERAGE"
