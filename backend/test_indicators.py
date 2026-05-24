import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis.indicators import ema, rsi, macd, atr
from analysis.support_resistance import detect_support_resistance

def test_ema_calculation():
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    ema_vals = ema.calculate_ema(prices, 3)
    assert ema_vals[0] is None
    assert ema_vals[1] is None
    assert isinstance(ema_vals[2], float)
    assert len(ema_vals) == len(prices)
    print("✓ test_ema_calculation passed")

def test_ema_signal_detection():
    signal = ema.detect_ema_signal([105, 106], [104, 107])
    assert signal in ["BULLISH_CROSS", "BEARISH_CROSS", "BULLISH_ALIGNED", "BEARISH_ALIGNED"]
    print("✓ test_ema_signal_detection passed")

def test_rsi_calculation():
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]
    rsi_vals = rsi.calculate_rsi(prices, 14)
    assert len(rsi_vals) == len(prices)
    assert all(v is None or (0 <= v <= 100) for v in rsi_vals)
    print("✓ test_rsi_calculation passed")

def test_rsi_signal():
    signal = rsi.get_rsi_signal(75)
    assert signal == "OVERBOUGHT"
    signal = rsi.get_rsi_signal(25)
    assert signal == "OVERSOLD"
    print("✓ test_rsi_signal passed")

def test_macd_calculation():
    prices = list(range(100, 150))
    macd_vals = macd.calculate_macd(prices)
    assert "macd" in macd_vals
    assert "signal" in macd_vals
    assert "histogram" in macd_vals
    print("✓ test_macd_calculation passed")

def test_atr_calculation():
    highs = [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    lows = [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    closes = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]
    atr_vals = atr.calculate_atr(highs, lows, closes, 14)
    assert len(atr_vals) == len(closes)
    assert all(v is None or v > 0 for v in atr_vals)
    print("✓ test_atr_calculation passed")

def test_support_resistance():
    prices = [100, 99, 98, 99, 100, 101, 100, 99, 100, 101]
    sr = detect_support_resistance(prices, window=2)
    assert sr["support"] < sr["resistance"]
    print("✓ test_support_resistance passed")

if __name__ == "__main__":
    test_ema_calculation()
    test_ema_signal_detection()
    test_rsi_calculation()
    test_rsi_signal()
    test_macd_calculation()
    test_atr_calculation()
    test_support_resistance()
    print("\nAll tests passed! ✓")
