// Socket.IO connection
const socket = io();

// Global variables
let username = '';
let currentLanguage = '';
let currentRoom = '';

// DOM elements
const loginModal = document.getElementById('loginModal');
const chatContainer = document.getElementById('chatContainer');
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const languageSelect = document.getElementById('language');
const roomInput = document.getElementById('room');
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const usersList = document.getElementById('usersList');
const currentUserSpan = document.getElementById('currentUser');
const roomNameSpan = document.getElementById('roomName');
const languageSelector = document.getElementById('languageSelector');
const leaveBtn = document.getElementById('leaveBtn');
const connectionStatus = document.getElementById('connectionStatus');
const statusText = document.getElementById('statusText');
const translationStatus = document.getElementById('translationStatus');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    showLoginModal();
    setupEventListeners();
});

function showLoginModal() {
    loginModal.style.display = 'flex';
    chatContainer.classList.add('hidden');
}

function hideLoginModal() {
    loginModal.style.display = 'none';
    chatContainer.classList.remove('hidden');
}

function setupEventListeners() {
    // Login form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const usernameValue = usernameInput.value.trim();
        const languageValue = languageSelect.value;
        const roomValue = roomInput.value.trim() || 'general';
        
        if (!usernameValue || !languageValue) {
            alert('Please fill in all required fields');
            return;
        }
        
        username = usernameValue;
        currentLanguage = languageValue;
        currentRoom = roomValue;
        
        joinChat(username, currentLanguage, currentRoom);
    });
    
    // Message sending
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Language change
    languageSelector.addEventListener('change', function(e) {
        const newLanguage = e.target.value;
        if (newLanguage !== currentLanguage) {
            currentLanguage = newLanguage;
            socket.emit('change_language', { language: newLanguage });
        }
    });
    
    // Leave chat
    leaveBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to leave the chat?')) {
            socket.disconnect();
            location.reload();
        }
    });
}

function joinChat(username, language, room) {
    socket.emit('join_chat', {
        username: username,
        language: language,
        room: room
    });
    
    // Update UI
    currentUserSpan.textContent = username;
    roomNameSpan.textContent = `Room: ${room}`;
    languageSelector.value = language;
    
    hideLoginModal();
}

function sendMessage() {
    const content = messageInput.value.trim();
    
    if (!content) return;
    
    socket.emit('send_message', {
        content: content
    });
    
    messageInput.value = '';
    sendBtn.disabled = true;
    
    setTimeout(() => {
        sendBtn.disabled = false;
    }, 500); // Prevent spam
}

function addMessage(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${data.is_own ? 'own' : ''}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageHeader = document.createElement('div');
    messageHeader.className = 'message-header';
    messageHeader.textContent = data.username;
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = data.content;
    
    const messageFooter = document.createElement('div');
    messageFooter.className = 'message-footer';
    
    const timestamp = document.createElement('span');
    timestamp.textContent = data.timestamp;
    messageFooter.appendChild(timestamp);
    
    if (data.is_translated) {
        const translationBadge = document.createElement('span');
        translationBadge.className = 'translation-badge';
        translationBadge.textContent = '🌐 Translated';
        messageFooter.appendChild(translationBadge);
    }
    
    messageContent.appendChild(messageHeader);
    messageContent.appendChild(messageText);
    messageContent.appendChild(messageFooter);
    messageDiv.appendChild(messageContent);
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function addSystemMessage(message) {
    const systemDiv = document.createElement('div');
    systemDiv.className = 'system-message';
    systemDiv.textContent = message;
    
    messagesDiv.appendChild(systemDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function updateUsersList(users) {
    usersList.innerHTML = '';
    
    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'user-item';
        
        const onlineIndicator = document.createElement('div');
        onlineIndicator.className = 'user-online';
        
        const userName = document.createElement('span');
        userName.textContent = user;
        
        userDiv.appendChild(onlineIndicator);
        userDiv.appendChild(userName);
        usersList.appendChild(userDiv);
    });
}

function showConnectionStatus(message, isConnected = false) {
    statusText.textContent = message;
    connectionStatus.classList.remove('hidden');
    
    if (isConnected) {
        connectionStatus.classList.add('connected');
    } else {
        connectionStatus.classList.remove('connected');
    }
    
    // Hide after 3 seconds if connected
    if (isConnected) {
        setTimeout(() => {
            connectionStatus.classList.add('hidden');
        }, 3000);
    }
}

function updateTranslationStatus(isActive) {
    const statusDot = translationStatus.querySelector('.status-dot');
    const statusText = translationStatus.querySelector('span:last-child');
    
    if (isActive) {
        statusDot.classList.add('active');
        statusText.textContent = 'Ollama Ready';
    } else {
        statusDot.classList.remove('active');
        statusText.textContent = 'Ollama Offline';
    }
}

// Socket.IO event listeners
socket.on('connect', function() {
    console.log('Connected to server');
    showConnectionStatus('Connected!', true);
    updateTranslationStatus(true);
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
    showConnectionStatus('Connection lost. Reconnecting...', false);
    updateTranslationStatus(false);
});

socket.on('reconnect', function() {
    console.log('Reconnected to server');
    showConnectionStatus('Reconnected!', true);
    updateTranslationStatus(true);
    
    // Rejoin chat if we were in one
    if (username && currentLanguage && currentRoom) {
        socket.emit('join_chat', {
            username: username,
            language: currentLanguage,
            room: currentRoom
        });
    }
});

socket.on('receive_message', function(data) {
    addMessage(data);
});

socket.on('user_joined', function(data) {
    addSystemMessage(`✅ ${data.message}`);
});

socket.on('user_left', function(data) {
    addSystemMessage(`❌ ${data.message}`);
});

socket.on('update_users', function(data) {
    updateUsersList(data.users);
});

socket.on('language_changed', function(data) {
    addSystemMessage(`🌐 Your language has been changed to ${data.language}`);
});

socket.on('connect_error', function(error) {
    console.error('Connection error:', error);
    showConnectionStatus('Connection failed. Please check if the server is running.', false);
    updateTranslationStatus(false);
});

// Auto-resize message input
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
});

// Focus message input when page loads
window.addEventListener('load', function() {
    if (!loginModal.style.display || loginModal.style.display === 'none') {
        messageInput.focus();
    }
});