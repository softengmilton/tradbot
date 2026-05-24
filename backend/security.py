"""
Security and optimization utilities for the trading chart analyzer
Provides input validation, CORS configuration, and caching
"""

import re
import json
from typing import Any, Dict, Optional
from functools import lru_cache
import hashlib
import logging

logger = logging.getLogger(__name__)

class InputValidator:
    """Validate and sanitize user inputs"""
    
    @staticmethod
    def validate_base64_image(image_data: str) -> bool:
        """Validate base64 image data"""
        if not image_data:
            return False
        
        # Check if string is valid base64
        try:
            # Remove common prefixes
            clean_data = image_data.replace("data:image/png;base64,", "")
            clean_data = clean_data.replace("data:image/jpeg;base64,", "")
            clean_data = clean_data.replace("data:image/jpg;base64,", "")
            
            # Validate base64
            if len(clean_data) % 4 != 0:
                return False
            
            # Attempt decode
            import base64
            base64.b64decode(clean_data, validate=True)
            return True
        except Exception as e:
            logger.warning(f"Invalid base64 image: {e}")
            return False
    
    @staticmethod
    def validate_session_id(session_id: str) -> bool:
        """Validate session ID format (UUID v4)"""
        if not session_id:
            return False
        
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(session_id))
    
    @staticmethod
    def validate_message_text(message: str, max_length: int = 5000) -> bool:
        """Validate chat message text"""
        if not message or not isinstance(message, str):
            return False
        
        # Check length
        if len(message) == 0 or len(message) > max_length:
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'<script',  # JavaScript injection
            r'javascript:',  # JavaScript protocol
            r'on\w+\s*=',  # Event handlers
        ]
        
        message_lower = message.lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, message_lower):
                return False
        
        return True
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """Validate trading symbol format"""
        if not symbol or not isinstance(symbol, str):
            return False
        
        # Allow alphanumeric and basic symbols
        if len(symbol) > 20:
            return False
        
        # Only allow letters, numbers, and common separators
        if not re.match(r'^[A-Z0-9_/]+$', symbol.upper()):
            return False
        
        return True
    
    @staticmethod
    def validate_mode(mode: str) -> bool:
        """Validate analysis mode"""
        valid_modes = ["default", "ai"]
        return mode in valid_modes
    
    @staticmethod
    def sanitize_analysis_text(text: str) -> str:
        """Remove any potentially dangerous content from analysis text"""
        if not text:
            return ""
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Limit extremely long strings
        if len(text) > 10000:
            text = text[:10000]
        
        return text

class AnalysisCache:
    """Simple LRU cache for analyzed charts"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache: Dict[str, Any] = {}
        self.access_order = []
    
    @staticmethod
    def _hash_image(image_base64: str) -> str:
        """Create hash of image for cache key"""
        return hashlib.sha256(image_base64.encode()).hexdigest()[:16]
    
    def get(self, image_base64: str, mode: str) -> Optional[Dict]:
        """Get cached analysis if available"""
        cache_key = f"{self._hash_image(image_base64)}_{mode}"
        
        if cache_key in self.cache:
            logger.info(f"Cache hit for {mode} mode")
            return self.cache[cache_key]
        
        return None
    
    def set(self, image_base64: str, mode: str, result: Dict) -> None:
        """Cache analysis result"""
        cache_key = f"{self._hash_image(image_base64)}_{mode}"
        
        # Implement LRU eviction
        if len(self.cache) >= self.max_size:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
        
        self.cache[cache_key] = result
        if cache_key in self.access_order:
            self.access_order.remove(cache_key)
        self.access_order.append(cache_key)
        
        logger.info(f"Cached {mode} mode analysis")
    
    def clear(self) -> None:
        """Clear entire cache"""
        self.cache.clear()
        self.access_order.clear()
        logger.info("Cache cleared")

class SecurityHeaders:
    """CORS and security header configurations"""
    
    @staticmethod
    def get_cors_config():
        """Get CORS configuration for FastAPI"""
        return {
            "allow_origins": [
                "http://localhost:3000",
                "http://localhost:8000",
                "chrome-extension://*"
            ],
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "max_age": 600,
        }
    
    @staticmethod
    def get_security_headers():
        """Get security headers for responses"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

class RateLimiter:
    """Simple rate limiting for API endpoints"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed"""
        import time
        
        now = time.time()
        
        # Initialize or reset if window expired
        if key not in self.requests:
            self.requests[key] = {"count": 0, "window_start": now}
        
        req_data = self.requests[key]
        
        # Check if window expired
        if now - req_data["window_start"] > self.window_seconds:
            req_data = {"count": 0, "window_start": now}
            self.requests[key] = req_data
        
        # Check if limit exceeded
        if req_data["count"] >= self.max_requests:
            return False
        
        # Increment counter
        req_data["count"] += 1
        return True

class PerformanceMonitor:
    """Monitor API performance"""
    
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "total_analysis_time": 0.0,
            "average_response_time": 0.0,
            "cache_hits": 0,
            "errors": 0,
        }
    
    def record_request(self, duration_ms: float) -> None:
        """Record request metrics"""
        self.metrics["total_requests"] += 1
        self.metrics["total_analysis_time"] += duration_ms
        self.metrics["average_response_time"] = (
            self.metrics["total_analysis_time"] / self.metrics["total_requests"]
        )
    
    def record_cache_hit(self) -> None:
        """Record cache hit"""
        self.metrics["cache_hits"] += 1
    
    def record_error(self) -> None:
        """Record error"""
        self.metrics["errors"] += 1
    
    def get_metrics(self) -> Dict:
        """Get performance metrics"""
        return self.metrics.copy()

# Global instances
input_validator = InputValidator()
analysis_cache = AnalysisCache()
rate_limiter = RateLimiter()
performance_monitor = PerformanceMonitor()
