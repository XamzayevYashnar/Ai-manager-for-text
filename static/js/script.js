// Проверяем, что скрипт вообще запустился
console.log("Chat script initialized...");

const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatWindow = document.getElementById('chat-window');

// Берем CSRF токен (обязательно для Django POST запросов)
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || !csrfToken) return;

    console.log("Sending message:", text);

    // 1. Показываем сообщение пользователя
    chatWindow.innerHTML += `<div class="message user">${text}</div>`;
    userInput.value = ''; 
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // 2. Блок для ответа AI
    const aiDiv = document.createElement('div');
    aiDiv.className = 'message ai';
    aiDiv.innerText = '...'; 
    chatWindow.appendChild(aiDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `message=${encodeURIComponent(text)}&ajax=true`
        });

        const data = await response.json();

        if (data.status === 'ok') {
            aiDiv.innerText = data.answer;
            // Если начали новый чат на главной, меняем URL
            if (window.location.pathname === '/' && data.page_slug) {
                window.history.pushState({}, '', `/chat/${data.page_slug}/`);
            }
        } else {
            aiDiv.innerText = "Ошибка: " + (data.error || "неизвестно");
        }
    } catch (e) {
        console.error("Fetch error:", e);
        aiDiv.innerText = "Ошибка соединения с сервером.";
    }
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Привязываем события только если элементы найдены
if (sendBtn) {
    sendBtn.onclick = sendMessage;
}

if (userInput) {
    userInput.onkeydown = (e) => { 
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    };
}
