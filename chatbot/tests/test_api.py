import sys
import os
import json
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch
from app import app

class TestJARVISAPI(unittest.TestCase):
    """Test suite for JARVIS API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Test the home endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('version', data)
        self.assertIn('status', data)
        self.assertEqual(data['version'], '2.3')
        self.assertEqual(data['status'], 'operational')
    
    def test_chat_endpoint_valid_message(self):
        """Test chat endpoint with valid message"""
        payload = {
            'message': 'Hello JARVIS',
            'session_id': 'test_session_123'
        }
        
        response = self.app.post('/chat', 
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('JARVIS', data['response'])
    
    def test_chat_endpoint_course_inquiry(self):
        """Test chat endpoint with course inquiry"""
        payload = {
            'message': 'tell me about computer science',
            'session_id': 'test_session_456'
        }
        
        response = self.app.post('/chat',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertIn('Computer Science', data['response'])
    
    def test_chat_endpoint_no_message(self):
        """Test chat endpoint without message"""
        payload = {'session_id': 'test_session_789'}
        
        response = self.app.post('/chat',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_chat_endpoint_invalid_message(self):
        """Test chat endpoint with invalid message"""
        payload = {
            'message': '',  # Empty message
            'session_id': 'test_session_empty'
        }
        
        response = self.app.post('/chat',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_chat_endpoint_long_message(self):
        """Test chat endpoint with message too long"""
        long_message = 'x' * 501  # Exceeds MAX_MESSAGE_LENGTH
        payload = {
            'message': long_message,
            'session_id': 'test_session_long'
        }
        
        response = self.app.post('/chat',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_chat_endpoint_shutdown_command(self):
        """Test chat endpoint with shutdown command"""
        payload = {
            'message': 'goodbye',
            'session_id': 'test_session_shutdown'
        }
        
        response = self.app.post('/chat',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'shutdown')
        self.assertIn('Shutting down', data['response'])
    
    def test_set_title_endpoint(self):
        """Test set title endpoint"""
        payload = {
            'session_id': 'test_title_session',
            'title': 'ma'  # Should set to Ma'am
        }
        
        response = self.app.post('/set_title',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertIn("Ma'am", data['response'])
        
        # Test default title (Sir)
        payload['title'] = 'sir'
        response = self.app.post('/set_title',
                                json=payload,
                                content_type='application/json')
        
        data = json.loads(response.data)
        self.assertIn('Sir', data['response'])
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('timestamp', data)
        self.assertIn('active_sessions', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_stats_endpoint(self):
        """Test statistics endpoint"""
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('active_sessions', data)
        self.assertIn('total_intents', data)
        self.assertIn('total_responses', data)
        self.assertIn('rate_limit_settings', data)
        self.assertIn('session_settings', data)
    
    def test_test_intent_endpoint(self):
        """Test intent testing endpoint"""
        payload = {
            'message': 'tell me about computer science'
        }
        
        response = self.app.post('/test_intent',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('input', data)
        self.assertIn('detected_intent', data)
        self.assertIn('available_intents', data)
        self.assertEqual(data['detected_intent'], 'computer_science')
    
    @patch('app.is_rate_limited')
    def test_rate_limiting(self, mock_rate_limited):
        """Test rate limiting functionality"""
        # Mock rate limiting to return True
        mock_rate_limited.return_value = True
        
        payload = {
            'message': 'Hello',
            'session_id': 'test_rate_limit'
        }
        
        response = self.app.post('/chat',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 429)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['status'], 'rate_limited')
    
    def test_session_persistence(self):
        """Test that sessions persist user preferences"""
        session_id = 'test_persistence_session'
        
        # First, set a title
        title_payload = {
            'session_id': session_id,
            'title': 'ma'
        }
        
        response = self.app.post('/set_title',
                                json=title_payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Then send a chat message to see if title persists
        chat_payload = {
            'message': 'hello',
            'session_id': session_id
        }
        
        response = self.app.post('/chat',
                                json=chat_payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn("Ma'am", data['response'])
    
    def test_name_memory(self):
        """Test that the system remembers user names"""
        session_id = 'test_memory_session'
        
        # First, introduce with a name
        name_payload = {
            'message': 'My name is John',
            'session_id': session_id
        }
        
        response = self.app.post('/chat',
                                json=name_payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('John', data['response'])
        
        # Then send another message to see if name persists
        follow_up_payload = {
            'message': 'tell me about computer science',
            'session_id': session_id
        }
        
        response = self.app.post('/chat',
                                json=follow_up_payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('John', data['response'])
    
    def test_invalid_session_id(self):
        """Test handling of invalid session IDs"""
        payload = {
            'message': 'Hello',
            'session_id': 'invalid@session#id'  # Contains invalid characters
        }
        
        response = self.app.post('/chat',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        response = self.app.post('/chat',
                                data='{"message": "Hello"',  # Malformed JSON
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_missing_content_type(self):
        """Test handling of missing content type"""
        response = self.app.post('/chat',
                                data='{"message": "Hello"}')
        
        self.assertEqual(response.status_code, 400)


def run_api_tests():
    """Run API endpoint tests"""
    print("🧪 Running JARVIS API Test Suite")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJARVISAPI)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("📊 API TEST RESULTS:")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.errors:
        print("\n❌ ERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n🎉 ALL API TESTS PASSED!")
    else:
        print(f"\n⚠️  {len(result.failures + result.errors)} test(s) failed.")
    
    print("=" * 60)
    return success


if __name__ == '__main__':
    run_api_tests()