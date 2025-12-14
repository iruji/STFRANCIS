<?php
/**
 * SessionManager Class
 * Converted from Python session_manager.py to PHP
 * Handles session storage and management
 */

class SessionManager {
    private $sessionTimeout;
    private $storageFile;
    
    /**
     * Initialize session manager
     * 
     * @param int $sessionTimeout Session timeout in seconds (default: 2 hours)
     */
    public function __construct($sessionTimeout = 7200) {
        $this->sessionTimeout = $sessionTimeout;
        $this->storageFile = __DIR__ . '/sessions.json';
        $this->cleanupOldSessions();
    }
    
    /**
     * Load sessions from storage file
     * 
     * @return array Sessions data
     */
    private function loadSessions() {
        if (!file_exists($this->storageFile)) {
            return [];
        }
        
        $data = file_get_contents($this->storageFile);
        if (!$data) {
            return [];
        }
        
        $sessions = json_decode($data, true);
        return is_array($sessions) ? $sessions : [];
    }
    
    /**
     * Save sessions to storage file
     * 
     * @param array $sessions Sessions data to save
     */
    private function saveSessions($sessions) {
        file_put_contents($this->storageFile, json_encode($sessions, JSON_PRETTY_PRINT));
    }
    
    /**
     * Remove expired sessions from memory
     */
    public function cleanupOldSessions() {
        $sessions = $this->loadSessions();
        $currentTime = time();
        $expiredCount = 0;
        
        foreach ($sessions as $sessionId => $data) {
            $lastActivity = $data['last_activity'] ?? 0;
            if (($currentTime - $lastActivity) > $this->sessionTimeout) {
                unset($sessions[$sessionId]);
                $expiredCount++;
            }
        }
        
        if ($expiredCount > 0) {
            $this->saveSessions($sessions);
            error_log("Cleaned up {$expiredCount} expired sessions");
        }
    }
    
    /**
     * Get or create a session
     * 
     * @param string $sessionId Unique session identifier
     * @return array Session data
     */
    public function getSession($sessionId) {
        $sessions = $this->loadSessions();
        
        if (!isset($sessions[$sessionId])) {
            $sessions[$sessionId] = [
                'title' => 'Sir',
                'last_activity' => time()
            ];
            $this->saveSessions($sessions);
        } else {
            // Update last activity
            $sessions[$sessionId]['last_activity'] = time();
            $this->saveSessions($sessions);
        }
        
        return $sessions[$sessionId];
    }
    
    /**
     * Update session data
     * 
     * @param string $sessionId Session identifier
     * @param array $updates Data to update
     */
    public function updateSession($sessionId, $updates) {
        $sessions = $this->loadSessions();
        
        if (!isset($sessions[$sessionId])) {
            $sessions[$sessionId] = [
                'title' => 'Sir',
                'last_activity' => time()
            ];
        }
        
        foreach ($updates as $key => $value) {
            $sessions[$sessionId][$key] = $value;
        }
        
        $sessions[$sessionId]['last_activity'] = time();
        $this->saveSessions($sessions);
    }
    
    /**
     * Delete a specific session
     * 
     * @param string $sessionId Session identifier to delete
     * @return bool True if deleted, false if not found
     */
    public function deleteSession($sessionId) {
        $sessions = $this->loadSessions();
        
        if (isset($sessions[$sessionId])) {
            unset($sessions[$sessionId]);
            $this->saveSessions($sessions);
            return true;
        }
        
        return false;
    }
    
    /**
     * Get the current number of active sessions
     * 
     * @return int Number of active sessions
     */
    public function getSessionCount() {
        $sessions = $this->loadSessions();
        return count($sessions);
    }
    
    /**
     * Get all sessions (for debugging)
     * 
     * @return array All sessions
     */
    public function getAllSessions() {
        return $this->loadSessions();
    }
}
?>