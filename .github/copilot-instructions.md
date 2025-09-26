# AI Chat Application - Copilot Instructions

## Architecture Overview

This is a **real-time multilingual chat application** with automatic translation via Ollama. The architecture follows a client-server pattern with WebSocket communication for real-time messaging and REST APIs for testing compatibility.

### Core Components

- **Flask + Socket.IO Server** (`app.py`): Handles real-time WebSocket events and REST API endpoints
- **Frontend** (`templates/index.html`, `static/`): Socket.IO client with modal-based UI
- **Ollama Integration**: External AI service for text translation (configurable model)
- **In-Memory Storage**: Users, messages, and room data (no database)

### Data Flow

1. User joins via modal → Socket.IO `join_chat` event → Server stores user in `users` dict
2. Message sent → `send_message` event → Server translates for each user's language → Broadcast to room
3. Language change → `change_language` event → Updates user preference → Future messages auto-translated

## Key Development Patterns

### Dual API Design
**Critical**: Every Socket.IO event has a corresponding REST endpoint for TestSprite compatibility:
```python
# Socket.IO event handler
@socketio.on('join_chat')
def on_join_chat(data): ...

# Corresponding REST endpoint
@app.route('/api/join_chat', methods=['POST'])
def api_join_chat(): ...

# TestSprite compatibility (no /api prefix)
@app.route('/join_chat', methods=['POST'])
def join_chat(): return api_join_chat()
```

### Translation Service Integration
All translation goes through `translate_text()` function with graceful fallback:
```python
def translate_text(text, target_language, source_language="auto"):
    # Returns original text if Ollama unavailable or errors
    # Always validate language codes against valid_languages list
```

### Error Handling Pattern
- **Socket.IO**: Emit `error` events with descriptive messages
- **REST APIs**: Return JSON with `{'error': 'message'}` and appropriate HTTP status
- **Translation**: Always fallback to original text, never fail requests

### User State Management
```python
users = {
    'socket_id': {
        'username': str,
        'language': str,  # lowercase from valid_languages
        'room': str,
        'joined_at': ISO_timestamp
    }
}
```

## Development Workflows

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama (required for translation)
ollama serve
ollama pull llama3.2  # or gemma3:4b (current default)

# Run application
python app.py  # Auto-starts on localhost:5000
```

### Environment Configuration
```bash
export OLLAMA_URL="http://localhost:11434/api/generate"
export OLLAMA_MODEL="gemma3:4b"  # Change model here
export SECRET_KEY="your-secret-key"
export DEBUG="True"
```

### Testing Integration
The `testsprite_tests/` directory contains automated tests that expect:
- REST endpoints without `/api` prefix (compatibility layer)
- Specific response formats with `username` at root level for TC004/TC005
- HTTP 200 status codes for successful operations
- Language validation against the 8 supported languages

## Project-Specific Conventions

### Language Handling
- **Validation**: Always check against `valid_languages` list (8 languages: english, hindi, spanish, french, german, chinese, japanese, korean)
- **Storage**: Languages stored in lowercase in user objects
- **Frontend**: Display names with native scripts in `index.html` select options

### Message Structure
```python
message = {
    'id': f"{user_id}_{len(messages)}",
    'username': str,
    'content': str,  # Original content
    'original_language': str,
    'room': str,
    'timestamp': 'HH:MM:SS',
    'created_at': ISO_timestamp
}
```

### Socket.IO Event Naming
- **Incoming**: `join_chat`, `send_message`, `change_language`
- **Outgoing**: `receive_message`, `user_joined`, `user_left`, `update_users`, `error`
- **System**: Always emit to rooms, never broadcast globally

### Frontend State Management
Global variables in `script.js`:
- `username`, `currentLanguage`, `currentRoom` - Track user state
- Modal-based login flow - Must validate all fields before joining
- Auto-reconnection logic - Rejoin same room on reconnect

## Integration Points

### Ollama Service
- **Health Check**: `test_ollama_connection()` at startup
- **Model Configuration**: Via `OLLAMA_MODEL` environment variable
- **Timeout Handling**: 30-second timeout with fallback to original text
- **Error Tolerance**: Application continues running if Ollama unavailable

### TestSprite Compatibility
- Additional REST endpoints without `/api` prefix
- Response format expectations (username at root level for some tests)
- Specific status codes and error messages
- Test configuration in `testsprite_backend_test_plan.json`

## File Organization

- `app.py`: **All server logic** - Socket.IO events, REST APIs, translation
- `templates/index.html`: **Complete UI** - Modal, chat interface, language selector
- `static/script.js`: **Client logic** - Socket.IO client, DOM manipulation, reconnection
- `static/style.css`: **Styling** - Modern chat UI with mobile responsiveness
- `requirements.txt`: **Dependencies** - Flask-SocketIO, requests for Ollama
- `testsprite_tests/`: **Test suite** - Backend test plans and generated test files

## Common Gotchas

1. **Language Case Sensitivity**: Always use lowercase for internal storage and comparison
2. **Translation Fallback**: Never let translation errors break the chat flow
3. **Room Management**: Users must join rooms before sending messages
4. **TestSprite URLs**: Some tests expect endpoints without `/api` prefix
5. **Socket.IO Rooms**: Use `room=uid` for individual user targeting, `room=room_name` for broadcast
6. **Ollama Model Names**: Must match exactly with pulled models (`ollama list`)