from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for users and messages
users = {}
messages = []
rooms = {}

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"

def translate_text(text, target_language, source_language="auto"):
    """Translate text using Ollama"""
    try:
        prompt = f"""Translate the following text from {source_language} to {target_language}. 
Only return the translated text, nothing else.

Text to translate: {text}

Translation:"""

        payload = {
            "model": "llama3.2",  # You can change this to your preferred model
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translation = result.get('response', '').strip()
            return translation if translation else text
        else:
            print(f"Ollama error: {response.status_code}")
            return text
            
    except Exception as e:
        print(f"Translation error: {e}")
        return text

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print(f'User {request.sid} connected')

@socketio.on('disconnect')
def on_disconnect():
    user_id = request.sid
    if user_id in users:
        username = users[user_id]['username']
        room = users[user_id]['room']
        
        # Leave room and notify others
        leave_room(room)
        del users[user_id]
        
        emit('user_left', {
            'username': username,
            'message': f'{username} left the chat'
        }, room=room)
        
        # Update user list for room
        room_users = [users[uid]['username'] for uid in users if users[uid]['room'] == room]
        emit('update_users', {'users': room_users}, room=room)
    
    print(f'User {user_id} disconnected')

@socketio.on('join_chat')
def on_join_chat(data):
    username = data['username']
    language = data['language']
    room = data.get('room', 'general')
    user_id = request.sid
    
    # Store user info
    users[user_id] = {
        'username': username,
        'language': language,
        'room': room
    }
    
    # Join room
    join_room(room)
    
    # Notify others in room
    emit('user_joined', {
        'username': username,
        'message': f'{username} joined the chat'
    }, room=room)
    
    # Send existing messages to new user (last 50 messages)
    room_messages = [msg for msg in messages if msg['room'] == room][-50:]
    for msg in room_messages:
        # Translate existing messages to user's language if needed
        if msg['original_language'] != language:
            translated_content = translate_text(msg['content'], language, msg['original_language'])
        else:
            translated_content = msg['content']
        
        emit('receive_message', {
            'username': msg['username'],
            'content': translated_content,
            'timestamp': msg['timestamp'],
            'is_translated': msg['original_language'] != language
        })
    
    # Update user list for room
    room_users = [users[uid]['username'] for uid in users if users[uid]['room'] == room]
    emit('update_users', {'users': room_users}, room=room)

@socketio.on('send_message')
def on_send_message(data):
    user_id = request.sid
    if user_id not in users:
        return
    
    user_info = users[user_id]
    username = user_info['username']
    user_language = user_info['language']
    room = user_info['room']
    content = data['content']
    
    # Create message object
    message = {
        'username': username,
        'content': content,
        'original_language': user_language,
        'room': room,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    # Store message
    messages.append(message)
    
    # Send message to all users in room with translation
    for uid, user_data in users.items():
        if user_data['room'] == room:
            target_language = user_data['language']
            
            # Translate if needed
            if user_language != target_language:
                translated_content = translate_text(content, target_language, user_language)
                is_translated = True
            else:
                translated_content = content
                is_translated = False
            
            emit('receive_message', {
                'username': username,
                'content': translated_content,
                'timestamp': message['timestamp'],
                'is_translated': is_translated,
                'is_own': uid == user_id
            }, room=uid)

@socketio.on('change_language')
def on_change_language(data):
    user_id = request.sid
    if user_id in users:
        users[user_id]['language'] = data['language']
        emit('language_changed', {'language': data['language']})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)