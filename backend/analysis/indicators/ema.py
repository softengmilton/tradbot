from typing import List, Optional

def calculate_ema(prices: List[float], period: int) -> List[Optional[float]]:
    """
    Calculate Exponential Moving Average

    Args:
        prices: List of close prices
        period: EMA period (20, 50, 200)

    Returns:
        List of EMA values (None for initial values < period)
    """
    if len(prices) < period:
        return [None] * len(prices)

    ema_values = [None] * (period - 1)
    k = 2 / (period + 1)

    # Initial SMA
    sma = sum(prices[:period]) / period
    ema_values.append(sma)

    # Subsequent EMA values
    for i in range(period, len(prices)):
        ema = (prices[i] * k) + (ema_values[-1] * (1 - k))
        ema_values.append(ema)

    return ema_values

def detect_ema_signal(ema20: List[float], ema50: List[float]) -> str:
    """Detect if EMA20 crossed above/below EMA50"""
    if len(ema20) < 2 or len(ema50) < 2:
        return "INSUFFICIENT_DATA"

    prev_above = ema20[-2] > ema50[-2]
    curr_above = ema20[-1] > ema50[-1]

    if not prev_above and curr_above:
        return "BULLISH_CROSS"
    elif prev_above and not curr_above:
        return "BEARISH_CROSS"
    elif curr_above:
        return "BULLISH_ALIGNED"
    else:
        return "BEARISH_ALIGNED"
