from typing import List

def detect_support_resistance(prices: List[float],
                              window: int = 5) -> dict:
    """
    Detect support (local lows) and resistance (local highs)

    Args:
        prices: List of close prices
        window: Lookback period for extremes

    Returns:
        {"support": float, "resistance": float}
    """

    def is_local_minimum(arr, i, window):
        start = max(0, i - window)
        end = min(len(arr), i + window + 1)
        return arr[i] == min(arr[start:end])

    def is_local_maximum(arr, i, window):
        start = max(0, i - window)
        end = min(len(arr), i + window + 1)
        return arr[i] == max(arr[start:end])

    # Find recent local lows and highs
    lows = []
    highs = []

    for i in range(max(window, len(prices) - 20), len(prices)):
        if is_local_minimum(prices, i, window):
            lows.append(prices[i])
        if is_local_maximum(prices, i, window):
            highs.append(prices[i])

    # Primary support = highest low
    # Primary resistance = lowest high

    support = max(lows) if lows else prices[-1] * 0.98
    resistance = min(highs) if highs else prices[-1] * 1.02

    return {
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "support_touches": len(lows),
        "resistance_touches": len(highs)
    }
