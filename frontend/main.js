document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    const addMessage = (message, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        
        if (sender === 'bot') {
            messageElement.innerHTML = marked.parse(message);
        } else {
            messageElement.innerText = message;
        }
        
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const handleUserInput = async () => {
        const prompt = userInput.value.trim();
        if (prompt === '') return;

        addMessage(prompt, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/api/prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt }),
            });

            if (!response.ok) {
                throw new Error('A resposta da rede não foi boa');
            }

            const data = await response.json();
            addMessage(data.resposta, 'bot');

        } catch (error) {
            console.error('Erro ao buscar resposta:', error);
            addMessage('Desculpe, ocorreu um erro ao me comunicar com o servidor.', 'bot');
        }
    };

    sendButton.addEventListener('click', handleUserInput);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            handleUserInput();
        }
    });
});
