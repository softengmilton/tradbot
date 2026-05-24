from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from analysis.default_analyzer import DefaultAnalyzer
from ai.openai_client import OpenAIAnalyzer
from memory.session_store import SessionStore
import logging
import json

router = APIRouter(prefix="/api", tags=["analysis"])
logger = logging.getLogger(__name__)

# Initialize AI and session store
session_store = SessionStore()
ai_analyzer = OpenAIAnalyzer()

class AnalysisRequest(BaseModel):
    mode: str  # "default" or "ai"
    image: Optional[str] = None  # base64 encoded
    symbol: Optional[str] = None
    timeframe: Optional[str] = None

@router.post("/analyze")
async def analyze_chart(request: AnalysisRequest):
    """Main analysis endpoint - handles both Default and AI modes"""

    try:
        if request.mode == "default":
            # Phase 1: Default mode logic
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

        elif request.mode == "ai":
            # Phase 2: AI mode logic
            if not request.image:
                raise HTTPException(status_code=400, detail="Image required for AI analysis")

            ai_result = ai_analyzer.analyze_chart(
                image_base64=request.image,
                symbol=request.symbol
            )

            if ai_result["status"] != "success":
                raise HTTPException(status_code=500, detail=ai_result["message"])

            # Parse AI response to validate JSON
            analysis_text = ai_result["analysis"]
            try:
                analysis_json = json.loads(analysis_text)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Invalid AI response format")

            # Create session for chat
            session_id = session_store.create_session(
                image_base64=request.image,
                analysis=analysis_text,
                symbol=request.symbol or "Unknown"
            )

            return {
                "mode": "ai",
                "session_id": session_id,
                "analysis": analysis_json,
                "tokens_used": ai_result.get("tokens_used", 0),
                "timestamp": datetime.now().isoformat()
            }

        else:
            raise HTTPException(status_code=400, detail="Invalid mode")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Retrieve session data"""
    
    session = session_store.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint for follow-up questions on chart analysis
    
    Expects:
    {
        "session_id": "uuid",
        "message": "user question"
    }
    """
    
    session_id = request.session_id
    user_message = request.message
    
    # Retrieve session
    session = session_store.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Add user message to history
    session_store.add_message(session_id, "user", user_message)
    
    # Build context for AI
    system_message = f"""You are an expert trading analyst discussing a chart analysis.
Original analysis summary: {session['analysis']}
Chart symbol: {session['symbol']}

Remember the chart context and answer questions about it. Be concise and trading-focused."""
    
    # Build message history for OpenAI
    messages = [
        {"role": "system", "content": system_message}
    ]
    
    # Add previous messages
    for msg in session_store.get_messages(session_id) or []:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    try:
        # Get AI response using OpenAI client
        response = ai_analyzer.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
        
        # Store AI response in history
        session_store.add_message(session_id, "assistant", ai_response)
        
        return {
            "session_id": session_id,
            "response": ai_response,
            "tokens_used": tokens_used,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.get("/session/{session_id}/messages")
async def get_session_messages(session_id: str):
    """Get chat messages for a session"""
    
    messages = session_store.get_messages(session_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"messages": messages}

@router.post("/session/{session_id}/message")
async def add_message(session_id: str, request: dict):
    """Add message to session chat"""
    
    success = session_store.add_message(
        session_id,
        role=request.get("role", "user"),
        content=request.get("content", "")
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"status": "success"}

@router.get("/health")
async def health_check():
    return {"status": "ok"}
