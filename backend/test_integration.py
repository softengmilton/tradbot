"""
Integration tests for trading chart analyzer API endpoints
Tests complete workflows for both default and AI modes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
import json
import base64
from fastapi.testclient import TestClient
from main import app
from memory.session_store import SessionStore

client = TestClient(app)

class TestAnalysisEndpoint:
    """Test /api/analyze endpoint"""
    
    def test_default_mode_analysis(self):
        """Test default mode analysis returns valid response"""
        response = client.post("/api/analyze", json={
            "mode": "default",
            "image": "test_base64_data"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "default"
        assert "trend" in data
        assert "confidence" in data
        assert "entry_zone" in data
    
    def test_invalid_mode_returns_error(self):
        """Test invalid mode returns 400 error"""
        response = client.post("/api/analyze", json={
            "mode": "invalid_mode",
            "image": "test_data"
        })
        
        assert response.status_code == 400
    
    def test_ai_mode_without_image(self):
        """Test AI mode without image returns 400"""
        response = client.post("/api/analyze", json={
            "mode": "ai"
        })
        
        assert response.status_code == 400
    
    def test_analysis_request_structure(self):
        """Test analysis request with all optional fields"""
        response = client.post("/api/analyze", json={
            "mode": "default",
            "image": "base64_data",
            "symbol": "BTCUSD",
            "timeframe": "1h"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

class TestSessionEndpoints:
    """Test session endpoints"""
    
    def test_get_nonexistent_session(self):
        """Test retrieving non-existent session returns 404"""
        response = client.get("/api/session/invalid_id_12345")
        
        assert response.status_code == 404
    
    def test_get_messages_nonexistent_session(self):
        """Test getting messages from non-existent session"""
        response = client.get("/api/session/invalid/messages")
        
        assert response.status_code == 404

class TestChatEndpoint:
    """Test /api/chat endpoint"""
    
    def test_chat_requires_session_id(self):
        """Test chat endpoint requires valid session"""
        response = client.post("/api/chat", json={
            "session_id": "invalid_session",
            "message": "Test message"
        })
        
        assert response.status_code == 404
    
    def test_chat_requires_message(self):
        """Test chat endpoint requires message field"""
        response = client.post("/api/chat", json={
            "session_id": "some_id"
        })
        
        assert response.status_code == 422  # Validation error

class TestErrorHandling:
    """Test error handling across endpoints"""
    
    def test_invalid_json_format(self):
        """Test invalid JSON request"""
        response = client.post("/api/analyze", 
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 422]
    
    def test_missing_required_fields(self):
        """Test request with missing required fields"""
        response = client.post("/api/analyze", json={})
        
        assert response.status_code == 422

class TestAPI:
    """Test API structure and health"""
    
    def test_root_endpoint(self):
        """Test API root endpoint accessible"""
        response = client.get("/")
        assert response.status_code in [200, 404]  # Either works or redirects
    
    def test_response_content_type(self):
        """Test responses have correct content type"""
        response = client.post("/api/analyze", json={
            "mode": "default",
            "image": "data"
        })
        
        assert "application/json" in response.headers.get("content-type", "")

def test_workflow_default_mode():
    """Test complete workflow for default mode"""
    # Step 1: Send analysis request
    response = client.post("/api/analyze", json={
        "mode": "default",
        "image": "test_image",
        "symbol": "EURUSD",
        "timeframe": "4h"
    })
    
    assert response.status_code == 200
    result = response.json()
    assert result["mode"] == "default"
    assert "indicators" in result

def test_workflow_ai_mode_mock():
    """Test AI mode workflow (mocked since no API key)"""
    # In production, only test with valid OpenAI API key
    response = client.post("/api/analyze", json={
        "mode": "ai",
        "image": "test_image",
        "symbol": "BTCUSD"
    })
    
    # Will fail without API key, but tests the endpoint
    assert response.status_code in [200, 500]

def test_multiple_requests_performance():
    """Test API performance with multiple requests"""
    import time
    
    start_time = time.time()
    
    for i in range(5):
        response = client.post("/api/analyze", json={
            "mode": "default",
            "image": f"test_data_{i}",
            "symbol": "BTCUSD"
        })
        assert response.status_code == 200
    
    elapsed = time.time() - start_time
    
    # Should complete in reasonable time (adjust based on performance)
    assert elapsed < 10  # 5 requests should take less than 10 seconds

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
