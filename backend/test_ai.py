import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory.session_store import SessionStore
from ai.prompts import CHART_ANALYSIS_PROMPT
import json
import time

def test_session_store_create():
    store = SessionStore()
    session_id = store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
    
    assert session_id is not None
    assert len(session_id) > 0
    print("✓ test_session_store_create passed")

def test_session_store_retrieve():
    store = SessionStore()
    session_id = store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
    session = store.get_session(session_id)
    
    assert session is not None
    assert session["symbol"] == "BTCUSD"
    assert session["analysis"] == '{"test": "data"}'
    print("✓ test_session_store_retrieve passed")

def test_session_store_add_message():
    store = SessionStore()
    session_id = store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
    
    success = store.add_message(session_id, "user", "Is this a buy signal?")
    assert success is True
    
    session = store.get_session(session_id)
    assert len(session["messages"]) == 1
    assert session["messages"][0]["role"] == "user"
    assert session["messages"][0]["content"] == "Is this a buy signal?"
    print("✓ test_session_store_add_message passed")

def test_session_store_timeout():
    store = SessionStore()
    store.timeout_minutes = 0  # Set timeout to 0 for testing
    
    session_id = store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
    time.sleep(0.1)  # Small delay
    
    session = store.get_session(session_id)
    assert session is None  # Should be expired
    print("✓ test_session_store_timeout passed")

def test_chart_analysis_prompt():
    prompt = CHART_ANALYSIS_PROMPT.format(symbol="BTCUSD")
    
    assert "BTCUSD" in prompt
    assert "market_structure" in prompt
    assert "entry_strategy" in prompt
    assert "JSON" in prompt
    print("✓ test_chart_analysis_prompt passed")

def test_session_cleanup():
    store = SessionStore()
    store.timeout_minutes = 0
    
    store.create_session("img1", "data1", "BTC")
    store.create_session("img2", "data2", "ETH")
    
    time.sleep(0.1)
    cleaned = store.cleanup_expired_sessions()
    
    assert cleaned == 2
    assert len(store.sessions) == 0
    print("✓ test_session_cleanup passed")

if __name__ == "__main__":
    test_session_store_create()
    test_session_store_retrieve()
    test_session_store_add_message()
    test_session_store_timeout()
    test_chart_analysis_prompt()
    test_session_cleanup()
    print("\nAll AI/Session tests passed! ✓")
