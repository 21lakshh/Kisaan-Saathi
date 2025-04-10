document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    let chatHistory = [];
    
    function addMessageToChat(message, isUser = false) {
        const messageDiv = `
            <div class="flex items-start ${isUser ? 'justify-end' : ''}">
                <div class="w-8 h-8 rounded-full ${isUser ? 'bg-blue-500/20 text-blue-500 ml-2' : 'bg-[#4caf50]/20 text-[#4caf50] mr-2'} flex items-center justify-center mt-1">
                    <i class="fas ${isUser ? 'fa-user' : 'fa-robot'}"></i>
                </div>
                <div class="${isUser ? 'bg-[#4caf50]/20 rounded-lg rounded-tr-none' : 'bg-[#1a2e1d] rounded-lg rounded-tl-none'} p-3 max-w-[80%]">
                    <p class="text-white">${message}</p>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function showLoadingIndicator() {
        const loadingMessage = `
            <div class="flex items-start">
                <div class="w-8 h-8 rounded-full bg-[#4caf50]/20 flex items-center justify-center text-[#4caf50] mr-2 mt-1">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="bg-[#1a2e1d] rounded-lg rounded-tl-none p-3 max-w-[80%]">
                    <div class="flex items-center space-x-2">
                        <div class="w-2 h-2 bg-[#4caf50] rounded-full animate-bounce"></div>
                        <div class="w-2 h-2 bg-[#4caf50] rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                        <div class="w-2 h-2 bg-[#4caf50] rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                    </div>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', loadingMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return chatMessages.lastChild;
    }
    
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat(message, true);
        
        // Clear input
        messageInput.value = '';
        
        // Show loading indicator
        const loadingElement = showLoadingIndicator();
        
        try {
            // Send message to backend
            const response = await fetch('/api/farmer-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message,
                    chat_history: chatHistory
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Network response was not ok');
            }
            
            // Remove loading message
            chatMessages.removeChild(loadingElement);
            
            // Add bot response
            addMessageToChat(data.response);
            
            // Update chat history with the new interaction
            if (Array.isArray(data.chat_history)) {
                chatHistory = data.chat_history;
            } else {
                // If chat history is not an array, add current interaction
                chatHistory.push(message);
                chatHistory.push(data.response);
            }
            
        } catch (error) {
            console.error('Error:', error);
            // Remove loading message
            chatMessages.removeChild(loadingElement);
            
            // Show error message
            addMessageToChat(`Sorry, I encountered an error: ${error.message}`);
            
            // Add current interaction to history even if there was an error
            chatHistory.push(message);
            chatHistory.push("Sorry, I encountered an error. Please try again.");
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Quick help buttons
    document.querySelectorAll('button.text-gray-300').forEach(button => {
        button.addEventListener('click', function() {
            messageInput.value = this.textContent.trim();
            messageInput.focus();
        });
    });
}); 