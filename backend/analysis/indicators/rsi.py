from typing import List, Optional

def calculate_rsi(prices: List[float], period: int = 14) -> List[Optional[float]]:
    """
    Calculate Relative Strength Index

    Args:
        prices: List of close prices
        period: RSI period (typically 14)

    Returns:
        List of RSI values (0-100)
    """
    if len(prices) < period + 1:
        return [None] * len(prices)

    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]

    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [abs(delta) if delta < 0 else 0 for delta in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    rsi_values = [None] * period

    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)

    return rsi_values

def get_rsi_signal(rsi_value: float) -> str:
    """Get RSI signal interpretation"""
    if rsi_value > 70:
        return "OVERBOUGHT"
    elif rsi_value < 30:
        return "OVERSOLD"
    else:
        return "NORMAL"
