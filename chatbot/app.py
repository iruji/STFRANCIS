from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random
from collections import defaultdict

from session_manager import SessionManager
from intents import intents, responses
from nlp import (
    enhanced_detect_intent,
    validate_input,
    validate_session_id,
    extract_name_safely,
    detect_memory_intent,
    get_time_aware_greeting
)

app = Flask(__name__)
CORS(app)

# Initialize session manager
session_manager = SessionManager()

# Rate limiting
request_counts = defaultdict(list)
RATE_LIMIT = 30  # requests per minute
RATE_WINDOW = 60  # seconds

def is_rate_limited(client_ip):
    current_time = time.time()
    # Clean old requests
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip]
        if current_time - req_time < RATE_WINDOW
    ]
    
    if len(request_counts[client_ip]) >= RATE_LIMIT:
        return True
    
    request_counts[client_ip].append(current_time)
    return False

def handle_memory(user_input, session_id):
    """Handle memory operations with improved responses"""
    name = extract_name_safely(user_input)
    
    if name:
        session_manager.update_session(session_id, {"name": name})
        
        # Different responses based on input pattern
        if "my name is" in user_input.lower():
            return f"Nice to meet you, {name}. I'll remember that for our conversation."
        elif "call me" in user_input.lower():
            return f"Understood, {name}. I'll address you properly from now on."
        else:
            return f"Got it, {name}. Pleasure to make your acquaintance."
    else:
        return "I didn't catch your name clearly. Could you try 'My name is [NAME]' or 'Call me [NAME]'?"

def jarvis_response(user_input, session_id):
    """Generate JARVIS response with enhanced logic"""
    session = session_manager.get_session(session_id)
    
    # Check for memory intent first
    if detect_memory_intent(user_input):
        return handle_memory(user_input, session_id)
    
    # Enhanced intent detection with scoring
    intent = enhanced_detect_intent(user_input)
    
    # Get user's preferred identifier (name or title)
    identifier = session.get("name", session.get("title", "Sir"))
    
    # Get response and format it
    reply = random.choice(responses.get(intent, responses["unknown"]))
    
    # Handle time-aware greetings
    if intent == "greeting":
        time_greeting = get_time_aware_greeting()
        reply = reply.format(
            title=identifier, 
            time_greeting=time_greeting,
            time_greeting_lower=time_greeting.lower()
        )
    else:
        reply = reply.format(title=identifier)
    
    return reply

# Flask routes
@app.route('/')
def home():
    return jsonify({
        "message": "JARVIS API v2.3 - SFAC Enhanced Edition with Website Navigation is online and ready to assist.",
        "version": "2.3",
        "status": "operational",
        "features": [
            "Comprehensive SFAC curriculum coverage",
            "Enhanced intent detection with plural handling",
            "Multi-word phrase recognition",
            "Session-based personalization",
            "Rate limiting protection",
            "Fixed course inquiry handling",
            "Website navigation assistance"
        ]
    })

@app.route('/chat', methods=['POST'])
def chat():
    client_ip = request.environ.get('REMOTE_ADDR', 'unknown')
    
    # Rate limiting
    if is_rate_limited(client_ip):
        return jsonify({
            'error': 'Too many requests. Please wait a moment before trying again.',
            'status': 'rate_limited'
        }), 429
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        session_id = data.get('session_id', f'default_{int(time.time())}')
        
        # Validate inputs
        validated_message = validate_input(user_message)
        if not validated_message:
            return jsonify({'error': 'Invalid message format or too long'}), 400
        
        if not validate_session_id(session_id):
            return jsonify({'error': 'Invalid session ID'}), 400
        
        # Check for shutdown words
        shutdown_words = ["quit", "exit", "goodbye", "bye", "bye bye", "shutdown", "power off", "log off", "sign out", "okay bye", "ok bye", "alright bye", "well bye", "thanks bye", "thank you bye", "cool bye", "see ya", "see you", "cya", "later", "gtg", "gotta go", "talk later", "catch you later"]
        if validated_message.lower() in shutdown_words:
            session = session_manager.get_session(session_id)
            identifier = session.get("name", session.get("title", "Sir"))
            goodbye_responses = [
                f"Shutting down systems. Until next time, {identifier}. SFAC looks forward to serving you again.",
                f"Powering off. Farewell, {identifier}. Remember, excellence in education awaits at SFAC.",
                f"System offline. Goodbye, {identifier}. Feel free to contact SFAC anytime for your educational needs.",
            ]
            return jsonify({
                'response': random.choice(goodbye_responses),
                'status': 'shutdown'
            })
        
        # Generate JARVIS response
        bot_response = jarvis_response(validated_message, session_id)
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': 'System malfunction detected. Please try again.',
            'status': 'error'
        }), 500

@app.route('/set_title', methods=['POST'])
def set_title():
    """Allow users to set their preferred title"""
    client_ip = request.environ.get('REMOTE_ADDR', 'unknown')
    
    if is_rate_limited(client_ip):
        return jsonify({'error': 'Too many requests'}), 429
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        session_id = data.get('session_id', f'default_{int(time.time())}')
        title_choice = data.get('title', '').lower()
        
        if not validate_session_id(session_id):
            return jsonify({'error': 'Invalid session ID'}), 400
        
        title = "Ma'am" if "ma" in title_choice or "miss" in title_choice else "Sir"
        
        session_manager.update_session(session_id, {"title": title})
        
        return jsonify({
            'response': f"Acknowledged, {title}. JARVIS is fully operational and ready to assist with SFAC inquiries.",
            'status': 'success'
        })
    
    except Exception as e:
        print(f"Error in set_title endpoint: {e}")
        return jsonify({'error': 'Could not set title'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': int(time.time()),
        'active_sessions': len(session_manager.sessions),
        'version': '2.3',
        'features_active': True
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Statistics endpoint for monitoring"""
    return jsonify({
        'active_sessions': len(session_manager.sessions),
        'total_intents': len(intents),
        'total_responses': sum(len(responses[key]) for key in responses),
        'rate_limit_settings': {
            'requests_per_minute': RATE_LIMIT,
            'window_seconds': RATE_WINDOW
        },
        'session_settings': {
            'cleanup_interval_seconds': session_manager.cleanup_interval,
            'session_timeout_seconds': session_manager.session_timeout
        }
    })

@app.route('/test_intent', methods=['POST'])
def test_intent():
    """Test endpoint to check intent detection (for debugging)"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        validated_message = validate_input(user_message)
        
        if not validated_message:
            return jsonify({'error': 'Invalid message format'}), 400
        
        detected_intent = enhanced_detect_intent(validated_message)
        
        return jsonify({
            'input': validated_message,
            'detected_intent': detected_intent,
            'available_intents': list(intents.keys()),
            'matching_keywords': intents.get(detected_intent, []) if detected_intent != "unknown" else []
        })
    
    except Exception as e:
        print(f"Error in test_intent endpoint: {e}")
        return jsonify({'error': 'Test failed'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("JARVIS API v2.3 - SFAC Enhanced Edition with Website Navigation")
    print("=" * 60)
    print("Starting up enhanced JARVIS system...")
    print(f"Loaded {len(intents)} intent categories")
    print(f"Configured {sum(len(responses[key]) for key in responses)} response variations")
    print("Specialized for St. Francis of Assisi College")
    print("Website navigation assistance enabled")
    print("=" * 60)
    print("API Endpoints:")
    print("   • Main API: http://localhost:5000")
    print("   • Chat: http://localhost:5000/chat")
    print("   • Health: http://localhost:5000/health")
    print("   • Stats: http://localhost:5000/stats")
    print("   • Set Title: http://localhost:5000/set_title")
    print("   • Test Intent: http://localhost:5000/test_intent")
    print("=" * 60)
    print("JARVIS is now online and ready to assist!")
    print("Course intent detection has been FIXED!")
    print("Grade level detection has been ENHANCED!")
    print("Website navigation assistance ADDED!")
    
    app.run(debug=True, host='localhost', port=5000)