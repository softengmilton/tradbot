from typing import List, Optional

def calculate_atr(highs: List[float], lows: List[float],
                  closes: List[float], period: int = 14) -> List[Optional[float]]:
    """Average True Range for volatility & stop loss sizing"""

    tr_values = []
    for i in range(len(closes)):
        if i == 0:
            tr = highs[i] - lows[i]
        else:
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
        tr_values.append(tr)

    atr = [None] * (period - 1)
    atr.append(sum(tr_values[:period]) / period)

    for i in range(period, len(tr_values)):
        atr.append((atr[-1] * (period - 1) + tr_values[i]) / period)

    return atr
