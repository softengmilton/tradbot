from pydantic import BaseModel
from typing import Optional, List, Dict

class AnalysisRequest(BaseModel):
    mode: str  # "default" or "ai"
    image: str  # base64 encoded
    symbol: Optional[str] = None
    timeframe: Optional[str] = None

class EntryZone(BaseModel):
    min: float
    max: float

class Indicators(BaseModel):
    ema20: float
    ema50: float
    ema200: float
    rsi: float
    atr: float

class AnalysisResponse(BaseModel):
    mode: str
    trend: str
    confidence: float
    entry_zone: EntryZone
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    support: float
    resistance: float
    signals: List[str]
    indicators: Indicators
