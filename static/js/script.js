const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const modelSelector = document.getElementById('modelSelector')

function addMessage(message, isUser=true){
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message': 'bot-message'}`;
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

}

async function sendMessage() {
    const message = userInput.value.trim()  ;
    if (!message) return;
    
    addMessage(message, true);
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type':'application/json' },
            body: JSON.stringify({
                input: message,
                model: modelSelector.value
            })
        });
        
        const data = await response.json();
        addMessage(data.response, false)
    } catch (error) {
        addMessage("Error communication with the server", false);

        console.error('Error', error);
    }
}

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter'){
        sendMessage();
    }
});