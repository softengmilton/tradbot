from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from analysis.default_analyzer import DefaultAnalyzer
import logging

router = APIRouter(prefix="/api", tags=["analysis"])
logger = logging.getLogger(__name__)

class AnalysisRequest(BaseModel):
    mode: str  # "default" or "ai"
    image: Optional[str] = None  # base64 encoded
    symbol: Optional[str] = None
    timeframe: Optional[str] = None

@router.post("/analyze")
async def analyze_chart(request: AnalysisRequest):
    """Main analysis endpoint"""

    try:
        if request.mode != "default":
            raise HTTPException(status_code=400, detail="Only default mode in Phase 1")

        # TODO: Decode image and extract price data
        # For Phase 1, use mock data
        prices_data = {
            "closes": [64000, 64100, 64050, 64150, 64200, 64250, 64300, 64350, 64400, 64450,
                      64500, 64550, 64600, 64650, 64700, 64750, 64800, 64850, 64900, 64950],
            "highs": [64100, 64150, 64150, 64250, 64300, 64350, 64400, 64450, 64500, 64550,
                     64600, 64650, 64700, 64750, 64800, 64850, 64900, 64950, 65000, 65050],
            "lows": [63950, 64000, 64000, 64100, 64150, 64200, 64250, 64300, 64350, 64400,
                    64450, 64500, 64550, 64600, 64650, 64700, 64750, 64800, 64850, 64900],
            "volumes": [1000, 1200, 900, 1100, 1300, 1150, 1050, 1250, 1350, 1100,
                       1200, 1400, 1050, 1150, 1300, 1100, 1200, 1350, 1250, 1400]
        }

        analyzer = DefaultAnalyzer(prices_data)
        result = analyzer.analyze()

        return JSONResponse(result)

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "ok"}
