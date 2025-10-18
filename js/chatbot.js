// Morphing Chatbot JavaScript
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
    }

    // NEW: Reset chat function
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
            // When chat is closed, clicking anywhere on the header opens it
            if (!isChatOpen) {
                console.log("Chat header clicked to open!");
                e.preventDefault();
                e.stopPropagation();
                toggleChatbot();
            }
            // When chat is open, only the header bar should be clickable to close
        });
    }

    // Make chat header bar clickable to close (when chat is open)
    if (chatHeaderBar) {
        chatHeaderBar.addEventListener('click', function(e) {
            // Only close if clicking the header bar itself (not the close button)
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
        
        // Prevent input clicks from closing chat
        userInput.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Prevent chat area clicks from closing chat, but allow header clicks
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

    // Updated createMessage function for dynamic sizing
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
            avatar.textContent = "J";
            
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

    // ENHANCED: Send message function with reset handling
    async function sendMessage() {
        console.log("sendMessage called");
        
        if (!userInput) {
            console.error("userInput element not found!");
            return;
        }
        
        const input = userInput.value.trim();
        if (!input) return;

        // Display user message with dynamic sizing
        if (chatArea) {
            const userMessage = createMessage(input, true);
            chatArea.appendChild(userMessage);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        userInput.value = "";

        // Display typing indicator with avatar
        const typingMessage = createMessage('<i>typing...</i>', false);
        if (chatArea) {
            chatArea.appendChild(typingMessage);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        try {
            const response = await fetch("http://localhost:5000/chat", {
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

            // Replace typing message with actual response
            let botReply;
            if (data.status === 'rate_limited') {
                botReply = data.error;
            } else if (data.status === 'shutdown') {
                botReply = data.response;
            } else {
                botReply = data.response || "Sorry, no reply from API.";
            }
            
            // Remove typing message and add real response
            if (chatArea && typingMessage) {
                chatArea.removeChild(typingMessage);
                const botMessage = createMessage(botReply, false);
                chatArea.appendChild(botMessage);
                chatArea.scrollTop = chatArea.scrollHeight;
            }

            // NEW: Handle shutdown status - reset chat after showing goodbye message
            if (data.status === 'shutdown') {
                console.log("Shutdown detected, resetting chat in 3 seconds...");
                setTimeout(() => {
                    resetChat();
                }, 3000); // Wait 3 seconds to let user read the goodbye message
                return; // Exit early, don't show badge
            }

            // Show badge if chat is closed (only for non-shutdown messages)
            if (!isChatOpen && newMsgBadge) {
                newMsgBadge.style.display = "flex";
            }

        } catch (error) {
            console.error("Chat error:", error);
            
            let errorMessage;
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                errorMessage = "Cannot connect to server. Please make sure the API is running on localhost:5000.";
            } else if (error.message.includes('429')) {
                errorMessage = "Too many requests. Please wait a moment before trying again.";
            } else {
                errorMessage = "Sorry, something went wrong. Please try again.";
            }
            
            // Replace typing message with error message
            if (chatArea && typingMessage) {
                chatArea.removeChild(typingMessage);
                const errorBotMessage = createMessage(errorMessage, false);
                chatArea.appendChild(errorBotMessage);
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            
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
    
    // Initialize chat with welcome message
    initializeChat();
    
    function initializeChat() {
        if (chatArea) {
            const welcomeMessage = createMessage("Hello, I'm J.A.R.V.I.S. your virtual assistant. How can I help you today?", false);
            chatArea.appendChild(welcomeMessage);
        }
    }
});

// Updated CSS styles for dynamic message sizing
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