import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory.session_store import SessionStore
from ai.prompts import CHART_ANALYSIS_PROMPT
from analysis.default_analyzer import DefaultAnalyzer
from analysis.confidence import ConfidenceCalculator
import json
import time
import unittest

class TestSessionStore(unittest.TestCase):
    """Unit tests for SessionStore"""
    
    def setUp(self):
        self.store = SessionStore()
    
    def test_session_store_create(self):
        """Test creating a new session"""
        session_id = self.store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
        
        self.assertIsNotNone(session_id)
        self.assertGreater(len(session_id), 0)
        self.assertIn(session_id, self.store.sessions)
    
    def test_session_store_retrieve(self):
        """Test retrieving a session"""
        session_id = self.store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
        session = self.store.get_session(session_id)
        
        self.assertIsNotNone(session)
        self.assertEqual(session["symbol"], "BTCUSD")
        self.assertEqual(session["analysis"], '{"test": "data"}')
        self.assertEqual(session["id"], session_id)
    
    def test_session_store_add_message(self):
        """Test adding messages to session"""
        session_id = self.store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
        
        success = self.store.add_message(session_id, "user", "Is this a buy signal?")
        self.assertTrue(success)
        
        session = self.store.get_session(session_id)
        self.assertEqual(len(session["messages"]), 1)
        self.assertEqual(session["messages"][0]["role"], "user")
        self.assertEqual(session["messages"][0]["content"], "Is this a buy signal?")
    
    def test_session_store_multiple_messages(self):
        """Test adding multiple messages"""
        session_id = self.store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
        
        self.store.add_message(session_id, "user", "First question")
        self.store.add_message(session_id, "assistant", "First answer")
        self.store.add_message(session_id, "user", "Second question")
        
        session = self.store.get_session(session_id)
        self.assertEqual(len(session["messages"]), 3)
    
    def test_session_get_messages(self):
        """Test retrieving all messages"""
        session_id = self.store.create_session("base64_image", '{"test": "data"}', "BTCUSD")
        
        self.store.add_message(session_id, "user", "Q1")
        self.store.add_message(session_id, "assistant", "A1")
        
        messages = self.store.get_messages(session_id)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]["role"], "assistant")
    
    def test_session_add_message_invalid_session(self):
        """Test adding message to non-existent session"""
        success = self.store.add_message("invalid_id", "user", "test")
        self.assertFalse(success)
    
    def test_session_cleanup_expired(self):
        """Test cleanup of expired sessions"""
        # Create session with very short timeout
        self.store.timeout_minutes = 0.0001
        session_id = self.store.create_session("image", '{"data": "test"}', "BTC")
        
        # Wait to expire
        time.sleep(0.1)
        
        # Cleanup should remove it
        expired_count = self.store.cleanup_expired_sessions()
        self.assertGreater(expired_count, 0)
    
    def test_session_last_accessed_update(self):
        """Test that last_accessed is updated"""
        session_id = self.store.create_session("image", '{"data": "test"}', "BTC")
        original_time = self.store.sessions[session_id]["last_accessed"]
        
        time.sleep(0.05)
        self.store.get_session(session_id)
        updated_time = self.store.sessions[session_id]["last_accessed"]
        
        self.assertNotEqual(original_time, updated_time)

class TestDefaultAnalyzer(unittest.TestCase):
    """Unit tests for DefaultAnalyzer"""
    
    def setUp(self):
        self.sample_data = {
            "closes": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                      110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
            "highs": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                     111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
            "lows": [99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
                    109, 110, 111, 112, 113, 114, 115, 116, 117, 118],
            "volumes": [1000, 1100, 1050, 1200, 1150, 1100, 1250, 1300, 1200, 1100,
                       1150, 1200, 1100, 1250, 1300, 1200, 1100, 1150, 1200, 1250]
        }
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = DefaultAnalyzer(self.sample_data)
        self.assertIsNotNone(analyzer)
    
    def test_analyzer_output_structure(self):
        """Test analyzer outputs correct structure"""
        analyzer = DefaultAnalyzer(self.sample_data)
        result = analyzer.analyze()
        
        self.assertIn("mode", result)
        self.assertIn("trend", result)
        self.assertIn("confidence", result)
        self.assertIn("entry_zone", result)
        self.assertIn("stop_loss", result)
        self.assertIn("take_profit_1", result)
        self.assertIn("take_profit_2", result)
    
    def test_analyzer_confidence_in_range(self):
        """Test confidence is within valid range"""
        analyzer = DefaultAnalyzer(self.sample_data)
        result = analyzer.analyze()
        
        self.assertGreaterEqual(result["confidence"], 0)
        self.assertLessEqual(result["confidence"], 100)
    
    def test_analyzer_trend_valid(self):
        """Test trend is one of valid values"""
        analyzer = DefaultAnalyzer(self.sample_data)
        result = analyzer.analyze()
        
        valid_trends = ["BULLISH", "BEARISH", "NEUTRAL"]
        self.assertIn(result["trend"], valid_trends)

class TestConfidenceCalculator(unittest.TestCase):
    """Unit tests for ConfidenceCalculator"""
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        calc = ConfidenceCalculator()
        
        # Test with sample signals
        factors = {
            "ema_alignment": True,
            "rsi_signal": True,
            "volume_confirmation": False,
            "macd_signal": True
        }
        
        confidence = calc.calculate_confidence(factors)
        self.assertGreaterEqual(confidence, 0)
        self.assertLessEqual(confidence, 100)

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def test_full_analysis_workflow(self):
        """Test complete default analysis workflow"""
        test_data = {
            "closes": list(range(100, 120)),
            "highs": list(range(101, 121)),
            "lows": list(range(99, 119)),
            "volumes": [1000] * 20
        }
        
        analyzer = DefaultAnalyzer(test_data)
        result = analyzer.analyze()
        
        # Verify complete result structure
        self.assertIsNotNone(result)
        self.assertIn("mode", result)
        self.assertIn("indicators", result)
    
    def test_session_full_chat_workflow(self):
        """Test complete chat workflow"""
        store = SessionStore()
        
        # Create session
        session_id = store.create_session("image", '{"analysis": "data"}', "BTCUSD")
        self.assertIsNotNone(session_id)
        
        # Add user message
        store.add_message(session_id, "user", "What is the entry point?")
        
        # Add AI response
        store.add_message(session_id, "assistant", "The entry point is at 100000")
        
        # Retrieve and verify
        messages = store.get_messages(session_id)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]["role"], "assistant")

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSessionStore))
    suite.addTests(loader.loadTestsFromTestCase(TestDefaultAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestConfidenceCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

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
