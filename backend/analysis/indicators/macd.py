from typing import List, Optional, Dict
from .ema import calculate_ema

def calculate_macd(prices: List[float]) -> Dict:
    """MACD = EMA12 - EMA26, Signal = EMA9(MACD)"""
    
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)

    macd_line = [ema12[i] - ema26[i] if ema12[i] and ema26[i] else None
                 for i in range(len(prices))]
    signal_line = calculate_ema(macd_line, 9)
    histogram = [macd_line[i] - signal_line[i]
                 if macd_line[i] and signal_line[i] else None
                 for i in range(len(prices))]

    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }
