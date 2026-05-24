from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from api.routes import router
from config import config
from security import (
    SecurityHeaders, 
    rate_limiter, 
    performance_monitor
)

# Setup logging
logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Trading Chart Analyzer API",
    description="Formula-based and AI-powered trading chart analysis",
    version="3.0.0",  # Phase 3
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware with security configuration
cors_config = SecurityHeaders.get_cors_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config["allow_origins"],
    allow_credentials=cors_config["allow_credentials"],
    allow_methods=cors_config["allow_methods"],
    allow_headers=cors_config["allow_headers"],
    max_age=cors_config["max_age"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    
    # Add security headers
    for header, value in SecurityHeaders.get_security_headers().items():
        response.headers[header] = value
    
    return response

# Add performance monitoring middleware
@app.middleware("http")
async def track_performance(request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        performance_monitor.record_request(duration_ms)
        
        return response
    except Exception as e:
        performance_monitor.record_error()
        logger.error(f"Request error: {e}")
        raise

# Include routers
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Trading Chart Analyzer API",
        "version": "3.0.0",
        "status": "running",
        "modes": ["default", "ai"],
        "endpoints": {
            "analyze": "/api/analyze",
            "session": "/api/session/{session_id}",
            "chat": "/api/chat",
            "docs": "/api/docs"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "metrics": performance_monitor.get_metrics()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    )
