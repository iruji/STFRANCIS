# import time
# import threading


# class SessionManager:
#     """Thread-safe session storage with automatic cleanup"""
    
#     def __init__(self, cleanup_interval=3600, session_timeout=7200):
#         """
#         Initialize session manager with cleanup parameters
        
#         Args:
#             cleanup_interval (int): Seconds between cleanup runs (default: 1 hour)
#             session_timeout (int): Session timeout in seconds (default: 2 hours)
#         """
#         self.sessions = {}
#         self.session_lock = threading.RLock()
#         self.cleanup_interval = cleanup_interval
#         self.session_timeout = session_timeout
#         self.start_cleanup_thread()
    
#     def start_cleanup_thread(self):
#         """Start the background cleanup thread"""
#         def cleanup():
#             while True:
#                 time.sleep(self.cleanup_interval)
#                 self.cleanup_old_sessions()
        
#         thread = threading.Thread(target=cleanup, daemon=True)
#         thread.start()
    
#     def cleanup_old_sessions(self):
#         """Remove expired sessions from memory"""
#         current_time = time.time()
#         with self.session_lock:
#             expired_sessions = [
#                 session_id for session_id, data in self.sessions.items()
#                 if current_time - data.get('last_activity', 0) > self.session_timeout
#             ]
#             for session_id in expired_sessions:
#                 del self.sessions[session_id]
#             if expired_sessions:
#                 print(f"Cleaned up {len(expired_sessions)} expired sessions")
    
#     def get_session(self, session_id):
#         """
#         Get or create a session
        
#         Args:
#             session_id (str): Unique session identifier
            
#         Returns:
#             dict: Session data
#         """
#         with self.session_lock:
#             if session_id not in self.sessions:
#                 self.sessions[session_id] = {
#                     'title': 'Sir',
#                     'last_activity': time.time()
#                 }
#             else:
#                 self.sessions[session_id]['last_activity'] = time.time()
#             return self.sessions[session_id]
    
#     def update_session(self, session_id, updates):
#         """
#         Update session data
        
#         Args:
#             session_id (str): Session identifier
#             updates (dict): Data to update
#         """
#         with self.session_lock:
#             session = self.get_session(session_id)
#             session.update(updates)
#             session['last_activity'] = time.time()
    
#     def delete_session(self, session_id):
#         """
#         Delete a specific session
        
#         Args:
#             session_id (str): Session identifier to delete
#         """
#         with self.session_lock:
#             if session_id in self.sessions:
#                 del self.sessions[session_id]
#                 return True
#             return False
    
#     def get_session_count(self):
#         """Get the current number of active sessions"""
#         with self.session_lock:
#             return len(self.sessions)
    
#     def get_all_sessions(self):
#         """Get a copy of all sessions (for debugging)"""
#         with self.session_lock:
#             return dict(self.sessions)