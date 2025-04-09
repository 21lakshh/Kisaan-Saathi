// Chat history to maintain context
let chatHistory = [];

// Initialize the chat when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Add welcome message
    addMessage('assistant', 'Hello! I can help you learn about various government schemes for farmers. You can ask about PM-KISAN, PMFBY, PMKSY, KCC, NBHM, or any other scheme. How can I assist you today?');
    
    // Add event listener for Enter key
    document.getElementById('userInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

// Function to ask about a specific scheme
function askAboutScheme(scheme) {
    let question = '';
    switch(scheme) {
        case 'PM-KISAN':
            question = 'Tell me about Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) scheme. What are its benefits and eligibility criteria?';
            break;
        case 'PMFBY':
            question = 'Explain the Pradhan Mantri Fasal Bima Yojana (PMFBY) scheme. How does it help farmers?';
            break;
        case 'PMKSY':
            question = 'What is Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)? How can farmers benefit from it?';
            break;
        case 'KCC':
            question = 'Tell me about the Kisan Credit Card (KCC) scheme. How can I apply for it?';
            break;
        case 'NBHM':
            question = 'What is the National Beekeeping and Honey Mission (NBHM)? How can I participate in it?';
            break;
        case 'general':
            question = 'What are some other important government schemes available for farmers?';
            break;
    }
    
    document.getElementById('userInput').value = question;
    sendMessage();
}

// Function to send message to FastAPI backend
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage('user', message);
    userInput.value = '';
    
    // Show loading indicator
    const loadingId = addMessage('assistant', 'Thinking...', true);
    
    try {
        // Call FastAPI endpoint
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                question: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading message
        document.getElementById(loadingId).remove();
        
        // Add assistant's response to chat
        addMessage('assistant', data.response);
        
        // Add to chat history
        chatHistory.push({
            role: 'user',
            content: message
        });
        chatHistory.push({
            role: 'assistant',
            content: data.response
        });
        
    } catch (error) {
        console.error('Error:', error);
        // Remove loading message
        document.getElementById(loadingId).remove();
        // Show error message
        addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
    }
}

// Function to add a message to the chat container
function addMessage(role, content, isTemp = false) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    const messageId = isTemp ? 'temp-' + Date.now() : '';
    
    messageDiv.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'} mb-4`;
    messageDiv.id = messageId;
    
    const messageContent = document.createElement('div');
    messageContent.className = `max-w-[80%] rounded-lg p-4 ${
        role === 'user' 
            ? 'bg-[#4caf50] text-white' 
            : 'bg-[#1a2e1d] text-white'
    }`;
    
    // Format the content with proper spacing and line breaks
    const formattedContent = content
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\b(https?:\/\/\S+)\b/g, '<a href="$1" target="_blank" class="text-blue-300 hover:text-blue-200">$1</a>');
    
    messageContent.innerHTML = formattedContent;
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return messageId;
} 