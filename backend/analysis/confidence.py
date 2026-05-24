from typing import Dict, List, Any

def calculate_confidence(analysis_data: Dict[str, Any]) -> float:
    """
    Calculate confidence score based on multiple factors
    
    Args:
        analysis_data: Dict containing trend, signals, rsi, volume_strength
        
    Returns:
        Confidence score (0-100)
    """
    confidence = 50  # Base confidence
    
    trend = analysis_data.get("trend", "NEUTRAL")
    signals = analysis_data.get("signals", [])
    rsi = analysis_data.get("rsi", 50)
    volume_strength = analysis_data.get("volume_strength", "BELOW_AVERAGE")
    
    # Trend confidence
    if trend.startswith("STRONG"):
        confidence += 20
    elif trend.startswith("WEAK"):
        confidence += 10
    
    # Signal confidence
    confidence += len(signals) * 5
    
    # RSI confidence
    if 30 < rsi < 70:
        confidence += 10
    elif rsi > 70 or rsi < 30:
        confidence += 15
    
    # Volume confidence
    if volume_strength == "ABOVE_AVERAGE":
        confidence += 10
    
    return min(100, max(0, confidence))
