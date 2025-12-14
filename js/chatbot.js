// Morphing Chatbot JavaScript - WITH STATE PERSISTENCE
console.log("Morphing chatbot script loading...");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing morphing chatbot...");
    
    // Grab elements
    const chatArea = document.getElementById("chatArea");
    const newMsgBadge = document.getElementById("new-msg-badge");
    const userInput = document.getElementById("userInput");
    const chatHeader = document.getElementById("chatbot-header");
    const chatHeaderBar = document.querySelector(".chat-header-bar");
    const closeBtn = document.querySelector(".close-btn");
    const sendBtn = document.querySelector(".send-btn");
    
    let isChatOpen = false;

    // ============================================
    // CHAT PERSISTENCE FUNCTIONS
    // ============================================
    
    /**
     * Save a message to localStorage
     */
    function saveMessageToStorage(content, isUser) {
        try {
            let chatHistory = JSON.parse(localStorage.getItem('jarvis_chat_history') || '[]');
            chatHistory.push({
                content: content,
                isUser: isUser,
                timestamp: Date.now()
            });
            
            // Keep only last 50 messages to avoid storage limits
            if (chatHistory.length > 50) {
                chatHistory = chatHistory.slice(-50);
            }
            
            localStorage.setItem('jarvis_chat_history', JSON.stringify(chatHistory));
        } catch (e) {
            console.error('Error saving message to storage:', e);
        }
    }
    
    /**
     * Load chat history from localStorage
     */
    function loadChatHistory() {
        try {
            const chatHistory = JSON.parse(localStorage.getItem('jarvis_chat_history') || '[]');
            
            // Clear current chat area
            if (chatArea) {
                chatArea.innerHTML = '';
            }
            
            // Restore all messages
            chatHistory.forEach(msg => {
                const messageDiv = createMessage(msg.content, msg.isUser);
                if (chatArea) {
                    chatArea.appendChild(messageDiv);
                }
            });
            
            // Scroll to bottom
            if (chatArea) {
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            
            console.log(`Loaded ${chatHistory.length} messages from history`);
        } catch (e) {
            console.error('Error loading chat history:', e);
        }
    }
    
    /**
     * Clear chat history from localStorage
     */
    function clearChatHistory() {
        try {
            localStorage.removeItem('jarvis_chat_history');
            console.log('Chat history cleared');
        } catch (e) {
            console.error('Error clearing chat history:', e);
        }
    }

    /**
     * NEW: Save chatbot open/closed state
     */
    function saveChatState(isOpen) {
        try {
            localStorage.setItem('jarvis_chat_open', isOpen ? 'true' : 'false');
        } catch (e) {
            console.error('Error saving chat state:', e);
        }
    }

    /**
     * NEW: Get chatbot open/closed state
     */
    function getChatState() {
        try {
            return localStorage.getItem('jarvis_chat_open') === 'true';
        } catch (e) {
            return false;
        }
    }

    // ============================================
    // CHATBOT UI FUNCTIONS
    // ============================================

    // Toggle chatbot with morphing animation
    function toggleChatbot() {
        console.log("toggleChatbot called, isChatOpen:", isChatOpen);
        
        if (!chatHeader) {
            console.error("chatHeader element not found!");
            return;
        }
        
        isChatOpen = !isChatOpen;
        
        if (isChatOpen) {
            console.log("Morphing chat open...");
            chatHeader.classList.add('morphed');
            if (newMsgBadge) newMsgBadge.style.display = "none";
            
            // Focus on input after animation completes
            setTimeout(() => {
                if (userInput) userInput.focus();
            }, 600);
        } else {
            console.log("Morphing chat closed...");
            chatHeader.classList.remove('morphed');
            
            // Blur input to prevent floating keyboard on mobile
            if (userInput) userInput.blur();
        }

        // NEW: Save the open/closed state
        saveChatState(isChatOpen);
    }

    // Reset chat function - now clears localStorage too
    function resetChat() {
        console.log("Resetting chat...");
        
        // Clear chat area
        if (chatArea) {
            chatArea.innerHTML = '';
        }
        
        // Clear user input
        if (userInput) {
            userInput.value = '';
        }
        
        // Clear chat history from localStorage
        clearChatHistory();
        
        // NEW: Clear chat state (reset to closed)
        saveChatState(false);
        
        // Generate new session ID
        const newSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('jarvis_session_id', newSessionId);
        
        // Close chat
        if (isChatOpen) {
            toggleChatbot();
        }
        
        // Reinitialize with welcome message after a brief delay
        setTimeout(() => {
            initializeChat();
        }, 500);
        
        console.log("Chat reset complete with new session:", newSessionId);
    }

    // Add click event listeners
    if (chatHeader) {
        chatHeader.addEventListener('click', function(e) {
            if (!isChatOpen) {
                console.log("Chat header clicked to open!");
                e.preventDefault();
                e.stopPropagation();
                toggleChatbot();
            }
        });
    }

    if (chatHeaderBar) {
        chatHeaderBar.addEventListener('click', function(e) {
            if (isChatOpen && !e.target.closest('.close-btn')) {
                console.log("Chat header bar clicked to close!");
                e.preventDefault();
                e.stopPropagation();
                toggleChatbot();
            }
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            console.log("Close button clicked!");
            e.preventDefault();
            e.stopPropagation();
            toggleChatbot();
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', function(e) {
            console.log("Send button clicked!");
            e.preventDefault();
            e.stopPropagation();
            sendMessage();
        });
    }

    // Press Enter to send message
    if (userInput) {
        userInput.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });
        
        userInput.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Prevent chat area clicks from closing chat
    if (chatArea) {
        chatArea.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Prevent input area clicks from closing chat
    const inputArea = document.querySelector('.input-area');
    if (inputArea) {
        inputArea.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Create message function
    function createMessage(content, isUser = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        if (isUser) {
            // User messages: No avatar, just content, dynamic width
            messageDiv.innerHTML = content;
            messageDiv.style.marginLeft = 'auto';
            messageDiv.style.marginRight = '0';
            messageDiv.style.textAlign = 'left';
        } else {
            // Bot messages: With avatar and content area
            const avatar = document.createElement("div");
            avatar.className = "msg-avatar bot";
            avatar.textContent = "C";
            
            const messageContent = document.createElement("div");
            messageContent.className = "msg-content";
            messageContent.innerHTML = content;
            
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
            messageDiv.style.marginLeft = '0';
            messageDiv.style.marginRight = 'auto';
        }
        
        return messageDiv;
    }

    // Send message function - NOW SAVES TO LOCALSTORAGE
    async function sendMessage() {
        console.log("sendMessage called");
        
        if (!userInput) {
            console.error("userInput element not found!");
            return;
        }
        
        const input = userInput.value.trim();
        if (!input) return;

        // Display user message
        if (chatArea) {
            const userMessage = createMessage(input, true);
            chatArea.appendChild(userMessage);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        // SAVE USER MESSAGE TO LOCALSTORAGE
        saveMessageToStorage(input, true);
        
        userInput.value = "";

        // Display typing indicator
        const typingMessage = createMessage('<i>typing...</i>', false);
        if (chatArea) {
            chatArea.appendChild(typingMessage);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        // Record start time for minimum delay
        const startTime = Date.now();
        const MINIMUM_TYPING_DELAY = 500; // 2 seconds

        //https://stfrancisbacoor.com/chatbot/api.php?action=chat
        // Call chatbot API
        try {
            const response = await fetch("chatbot/api.php?action=chat", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ 
                    message: input, 
                    session_id: getSessionId() 
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log("API returned:", data);

            // Get bot reply
            let botReply;
            if (data.status === 'rate_limited') {
                botReply = data.error;
            } else if (data.status === 'shutdown') {
                botReply = data.response;
            } else {
                botReply = data.response || "Sorry, no reply from API.";
            }
            
            // Calculate elapsed time and wait if needed
            const elapsedTime = Date.now() - startTime;
            const remainingDelay = Math.max(0, MINIMUM_TYPING_DELAY - elapsedTime);
            
            // Wait for remaining delay before showing response
            await new Promise(resolve => setTimeout(resolve, remainingDelay));
            
            // Remove typing message and add real response
            if (chatArea && typingMessage) {
                chatArea.removeChild(typingMessage);
                const botMessage = createMessage(botReply, false);
                chatArea.appendChild(botMessage);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            
            // SAVE BOT MESSAGE TO LOCALSTORAGE
            saveMessageToStorage(botReply, false);

            // Handle shutdown status
            if (data.status === 'shutdown') {
                console.log("Shutdown detected, resetting chat in 3 seconds...");
                setTimeout(() => {
                    resetChat();
                }, 3000);
                return;
            }

            // Show badge if chat is closed
            if (!isChatOpen && newMsgBadge) {
                newMsgBadge.style.display = "flex";
            }

        } catch (error) {
            console.error("Chat error:", error);
            
            let errorMessage;
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                errorMessage = "Cannot connect to server. Please make sure the API is running.";
            } else if (error.message.includes('429')) {
                errorMessage = "Too many requests. Please wait a moment before trying again.";
            } else {
                errorMessage = "Sorry, something went wrong. Please try again.";
            }
            
            // Calculate elapsed time and wait if needed (for errors too)
            const elapsedTime = Date.now() - startTime;
            const remainingDelay = Math.max(0, MINIMUM_TYPING_DELAY - elapsedTime);
            await new Promise(resolve => setTimeout(resolve, remainingDelay));
            
            // Remove typing message and add error
            if (chatArea && typingMessage) {
                chatArea.removeChild(typingMessage);
                const errorBotMessage = createMessage(errorMessage, false);
                chatArea.appendChild(errorBotMessage);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            
            // SAVE ERROR MESSAGE TO LOCALSTORAGE
            saveMessageToStorage(errorMessage, false);
            
            if (!isChatOpen && newMsgBadge) {
                newMsgBadge.style.display = "flex";
            }
        }
    }

    // Generate or retrieve session ID
    function getSessionId() {
        let sessionId = localStorage.getItem('jarvis_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('jarvis_session_id', sessionId);
        }
        return sessionId;
    }

    console.log("Morphing chatbot initialized successfully!");
    
    // Initialize chat - LOAD HISTORY OR SHOW WELCOME
    initializeChat();
    
    function initializeChat() {
        const existingHistory = localStorage.getItem('jarvis_chat_history');
        
        if (existingHistory && JSON.parse(existingHistory).length > 0) {
            // Load existing chat history
            console.log("Loading existing chat history...");
            loadChatHistory();
        } else {
            // Show welcome message for new chat
            console.log("No history found, showing welcome message...");
            if (chatArea) {
                const welcomeMessage = createMessage("Hello, I'm Ate Claire, your virtual assistant. How can I help you today?", false);
                chatArea.appendChild(welcomeMessage);
                
                // Save welcome message to history
                saveMessageToStorage("Hello, I'm Ate Claire, your virtual assistant. How can I help you today?", false);
            }
        }

        // NEW: Check if chat was open on previous page and reopen it
        if (getChatState()) {
            console.log("Chat was open on previous page, reopening...");
            setTimeout(() => {
                if (!isChatOpen) {
                    toggleChatbot();
                }
            }, 100); // Small delay to ensure DOM is ready
        }
    }
});

// CSS styles for dynamic message sizing
function addMessageStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .message {
            margin: 8px 0;
            padding: 10px 14px;
            border-radius: 18px;
            word-wrap: break-word;
            font-size: 14px;
            line-height: 1.4;
            border: none;
            display: inline-block;
            clear: both;
            position: relative;
            margin-bottom: 12px;
        }
        
        .user-message {
            background: #ed1b24 !important;
            color: white !important;
            float: right;
            max-width: 75%;
            min-width: fit-content;
            width: auto;
            border-bottom-right-radius: 6px;
            text-align: left;
        }
        
        .bot-message {
            background: #f5f5f5 !important;
            color: #333 !important;
            float: left;
            max-width: 80%;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            display: flex !important;
            align-items: flex-start;
            gap: 10px;
            border-bottom-left-radius: 6px;
            padding-left: 8px;
        }
        
        .msg-avatar {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
            margin-top: 2px;
        }
        
        .msg-avatar.bot {
            background: #ed1b24;
            color: white;
            border: 1px solid #ed1b24;
        }
        
        .msg-content {
            flex: 1;
        }
        
        /* Clear floats after messages */
        #chatArea::after {
            content: "";
            display: table;
            clear: both;
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .user-message {
                max-width: 85%;
            }
            
            .bot-message {
                max-width: 90%;
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize message styles when DOM loads
document.addEventListener('DOMContentLoaded', addMessageStyles);