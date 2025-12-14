<?php
/**
 * JARVIS Chatbot API - Main Entry Point
 * Converted from Flask (app.py) to PHP
 * Version: 2.3 - SFAC Enhanced Edition
 */

// Error reporting for development (disable in production) ini_set('display_errors', 0); between them
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/error.log');

// CORS headers
header('Access-Control-Allow-Origin: *'); // header('Access-Control-Allow-Origin: https://stfrancisbacoor.com');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept');
header('Content-Type: application/json');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Start session
session_start();

// Include dependencies
require_once 'includes/SessionManager.php';
require_once 'includes/intents.php';
require_once 'includes/nlp.php';

// Initialize session manager
$sessionManager = new SessionManager();

// Rate limiting configuration
$RATE_LIMIT = 30; // requests per minute
$RATE_WINDOW = 60; // seconds

/**
 * Simple rate limiting using session
 */
function isRateLimited() {
    global $RATE_LIMIT, $RATE_WINDOW;
    
    if (!isset($_SESSION['request_times'])) {
        $_SESSION['request_times'] = [];
    }
    
    $currentTime = time();
    
    // Clean old requests
    $_SESSION['request_times'] = array_filter(
        $_SESSION['request_times'],
        function($time) use ($currentTime, $RATE_WINDOW) {
            return ($currentTime - $time) < $RATE_WINDOW;
        }
    );
    
    if (count($_SESSION['request_times']) >= $RATE_LIMIT) {
        return true;
    }
    
    $_SESSION['request_times'][] = $currentTime;
    return false;
}

/**
 * Validate and sanitize input
 */
function validateInput($text, $maxLength = 500) {
    if (empty($text) || !is_string($text)) {
        return null;
    }
    
    $text = trim($text);
    if (strlen($text) === 0 || strlen($text) > $maxLength) {
        return null;
    }
    
    // Remove potentially harmful characters but keep basic punctuation
    $sanitized = preg_replace('/[^\w\s\.\,\?\!\-\'\"()]/', '', $text);
    return $sanitized;
}

/**
 * Validate session ID
 */
function validateSessionId($sessionId) {
    if (empty($sessionId) || !is_string($sessionId)) {
        return false;
    }
    
    if (strlen($sessionId) > 50) {
        return false;
    }
    
    // Only allow alphanumeric, hyphens, and underscores
    if (!preg_match('/^[a-zA-Z0-9_-]+$/', $sessionId)) {
        return false;
    }
    
    return true;
}

/**
 * Handle memory operations (name extraction)
 */
function handleMemory($userInput, $sessionId) {
    global $sessionManager;
    
    $name = extractNameSafely($userInput);
    
    if ($name) {
        $sessionManager->updateSession($sessionId, ['name' => $name]);
        
        if (stripos($userInput, 'my name is') !== false) {
            return "Nice to meet you, {$name}. I'll remember that for our conversation.";
        } elseif (stripos($userInput, 'call me') !== false) {
            return "Understood, {$name}. I'll address you properly from now on.";
        } else {
            return "Got it, {$name}. Pleasure to make your acquaintance.";
        }
    } else {
        return "I didn't catch your name clearly. Could you try 'My name is [NAME]' or 'Call me [NAME]'?";
    }
}

/**
 * Generate JARVIS response
 */
function jarvisResponse($userInput, $sessionId) {
    global $sessionManager, $responses;
    
    // Check for memory intent first
    if (detectMemoryIntent($userInput)) {
        return handleMemory($userInput, $sessionId);
    }
    
    // Enhanced intent detection
    $intent = enhancedDetectIntent($userInput);
    
    // Get user's preferred identifier
    $session = $sessionManager->getSession($sessionId);
    $identifier = $session['name'] ?? $session['title'] ?? 'Sir';
    
    // Get response and format it
    $intentResponses = $responses[$intent] ?? $responses['unknown'];
    $reply = $intentResponses[array_rand($intentResponses)];
    
    // Handle time-aware greetings
    if ($intent === 'greeting') {
        $timeGreeting = getTimeAwareGreeting();
        $reply = str_replace(
            ['{title}', '{time_greeting}', '{time_greeting_lower}'],
            [$identifier, $timeGreeting, strtolower($timeGreeting)],
            $reply
        );
    } else {
        $reply = str_replace('{title}', $identifier, $reply);
    }
    
    return $reply;
}

// Get the action from query string or default to chat
$action = $_GET['action'] ?? 'home';

// Route handling
switch ($action) {
    case 'home':
    case '':
        // Home endpoint - API info
        echo json_encode([
            'message' => 'JARVIS API v2.3 - SFAC Enhanced Edition with Website Navigation is online and ready to assist.',
            'version' => '2.3',
            'status' => 'operational',
            'features' => [
                'Comprehensive SFAC curriculum coverage',
                'Enhanced intent detection with plural handling',
                'Multi-word phrase recognition',
                'Session-based personalization',
                'Rate limiting protection',
                'Fixed course inquiry handling',
                'Website navigation assistance'
            ]
        ]);
        break;
        
    case 'chat':
        // Chat endpoint
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            exit;
        }
        
        // Rate limiting
        if (isRateLimited()) {
            http_response_code(429);
            echo json_encode([
                'error' => 'Too many requests. Please wait a moment before trying again.',
                'status' => 'rate_limited'
            ]);
            exit;
        }
        
        // Get POST data
        $input = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($input['message'])) {
            http_response_code(400);
            echo json_encode(['error' => 'No message provided']);
            exit;
        }
        
        $userMessage = $input['message'];
        $sessionId = $input['session_id'] ?? 'default_' . time();
        
        // Validate inputs
        $validatedMessage = validateInput($userMessage);
        if (!$validatedMessage) {
            http_response_code(400);
            echo json_encode(['error' => 'Invalid message format or too long']);
            exit;
        }
        
        if (!validateSessionId($sessionId)) {
            http_response_code(400);
            echo json_encode(['error' => 'Invalid session ID']);
            exit;
        }
        
        // Check for shutdown words
        $shutdownWords = [
            'quit', 'exit', 'goodbye', 'bye', 'bye bye', 'shutdown', 
            'power off', 'log off', 'sign out', 'okay bye', 'ok bye', 
            'alright bye', 'well bye', 'thanks bye', 'thank you bye', 
            'cool bye', 'see ya', 'see you', 'cya', 'later', 'gtg', 
            'gotta go', 'talk later', 'catch you later'
        ];
        
        if (in_array(strtolower($validatedMessage), $shutdownWords)) {
            $session = $sessionManager->getSession($sessionId);
            $identifier = $session['name'] ?? $session['title'] ?? 'Sir';
            
            $goodbyes = [
                "Shutting down systems. Until next time, {$identifier}. SFAC looks forward to serving you again.",
                "Powering off. Farewell, {$identifier}. Remember, excellence in education awaits at SFAC.",
                "System offline. Goodbye, {$identifier}. Feel free to contact SFAC anytime for your educational needs."
            ];
            
            echo json_encode([
                'response' => $goodbyes[array_rand($goodbyes)],
                'status' => 'shutdown'
            ]);
            exit;
        }
        
        // Generate JARVIS response
        try {
            $botResponse = jarvisResponse($validatedMessage, $sessionId);
            
            echo json_encode([
                'response' => $botResponse,
                'status' => 'success'
            ]);
        } catch (Exception $e) {
            http_response_code(500);
            echo json_encode([
                'error' => 'System malfunction detected. Please try again.',
                'status' => 'error'
            ]);
        }
        break;
        
    case 'set_title':
        // Set title endpoint
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            exit;
        }
        
        if (isRateLimited()) {
            http_response_code(429);
            echo json_encode(['error' => 'Too many requests']);
            exit;
        }
        
        $input = json_decode(file_get_contents('php://input'), true);
        
        if (!$input) {
            http_response_code(400);
            echo json_encode(['error' => 'No data provided']);
            exit;
        }
        
        $sessionId = $input['session_id'] ?? 'default_' . time();
        $titleChoice = strtolower($input['title'] ?? '');
        
        if (!validateSessionId($sessionId)) {
            http_response_code(400);
            echo json_encode(['error' => 'Invalid session ID']);
            exit;
        }
        
        $title = (strpos($titleChoice, 'ma') !== false || strpos($titleChoice, 'miss') !== false) 
            ? "Ma'am" 
            : "Sir";
        
        $sessionManager->updateSession($sessionId, ['title' => $title]);
        
        echo json_encode([
            'response' => "Acknowledged, {$title}. JARVIS is fully operational and ready to assist with SFAC inquiries.",
            'status' => 'success'
        ]);
        break;
        
    case 'health':
        // Health check endpoint
        echo json_encode([
            'status' => 'healthy',
            'timestamp' => time(),
            'active_sessions' => $sessionManager->getSessionCount(),
            'version' => '2.3',
            'features_active' => true
        ]);
        break;
        
    case 'stats':
        // Statistics endpoint
        global $intents, $responses;
        
        $totalResponses = 0;
        foreach ($responses as $responseArray) {
            $totalResponses += count($responseArray);
        }
        
        echo json_encode([
            'active_sessions' => $sessionManager->getSessionCount(),
            'total_intents' => count($intents),
            'total_responses' => $totalResponses,
            'rate_limit_settings' => [
                'requests_per_minute' => $RATE_LIMIT,
                'window_seconds' => $RATE_WINDOW
            ],
            'session_settings' => [
                'cleanup_interval_seconds' => 3600,
                'session_timeout_seconds' => 7200
            ]
        ]);
        break;
        
    case 'test_intent':
        // Test intent endpoint
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            exit;
        }
        
        $input = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($input['message'])) {
            http_response_code(400);
            echo json_encode(['error' => 'No message provided']);
            exit;
        }
        
        $userMessage = $input['message'];
        $validatedMessage = validateInput($userMessage);
        
        if (!$validatedMessage) {
            http_response_code(400);
            echo json_encode(['error' => 'Invalid message format']);
            exit;
        }
        
        $detectedIntent = enhancedDetectIntent($validatedMessage);
        
        echo json_encode([
            'input' => $validatedMessage,
            'detected_intent' => $detectedIntent,
            'available_intents' => array_keys($intents),
            'matching_keywords' => $intents[$detectedIntent] ?? []
        ]);
        break;
        
    default:
        http_response_code(404);
        echo json_encode([
            'error' => 'Endpoint not found',
            'available_endpoints' => [
                '?action=home',
                '?action=chat',
                '?action=set_title',
                '?action=health',
                '?action=stats',
                '?action=test_intent'
            ]
        ]);
        break;
}
?>