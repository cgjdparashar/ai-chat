# Multilingual Chat Application

A real-time chat application with automatic translation using Python Flask, Socket.IO, and Ollama.

## Features

- 🌍 **Real-time multilingual translation** using Ollama
- 💬 **Instant messaging** with Socket.IO
- 🏠 **Multiple chat rooms** support
- 🎨 **Modern, responsive UI** 
- 👥 **Live user presence** indicators
- 🔄 **Auto-reconnection** on network issues
- 📱 **Mobile-friendly** design

## Supported Languages

- English
- Hindi (हिंदी)  
- Spanish (Español)
- French (Français)
- German (Deutsch)
- Chinese (中文)
- Japanese (日本語)
- Korean (한국어)

## Prerequisites

1. **Python 3.7+** installed
2. **Ollama** installed and running
3. **Ollama model** (e.g., llama3.2) pulled

### Installing Ollama

1. Download and install Ollama from: https://ollama.ai
2. Pull a language model:
   ```bash
   ollama pull llama3.2
   ```
3. Verify Ollama is running:
   ```bash
   ollama list
   ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-chat
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Ollama model (optional):**
   - Edit `app.py` line 19 to change the model:
   ```python
   "model": "llama3.2",  # Change to your preferred model
   ```

## Running the Application

1. **Start Ollama** (if not running):
   ```bash
   ollama serve
   ```

2. **Run the Flask application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - Navigate to: http://localhost:5000
   - Or on your network: http://[your-ip]:5000

## Usage

### Getting Started
1. Enter your **username**
2. Select your **preferred language**
3. Choose or create a **chat room**
4. Click **"Join Chat"**

### Features
- **Send messages**: Type and press Enter or click send
- **Change language**: Use the language selector in the header
- **View online users**: Check the sidebar for active users
- **Translation indicator**: Messages show when they've been translated
- **Room switching**: Leave and join different rooms

### How Translation Works
- Each user sets their preferred language
- Messages are automatically translated to each recipient's language
- Original messages are preserved
- Translation is powered by Ollama AI

## Architecture

```
Frontend (HTML/CSS/JS)
    ↓ Socket.IO
Flask-SocketIO Server
    ↓ HTTP API
Ollama (Translation Engine)
```

### Key Components

- **`app.py`**: Flask server with Socket.IO events
- **`templates/index.html`**: Chat interface
- **`static/style.css`**: Modern UI styling
- **`static/script.js`**: Client-side Socket.IO logic

## Configuration

### Environment Variables (Optional)
```bash
export OLLAMA_URL="http://localhost:11434/api/generate"
export FLASK_DEBUG="True"  # For development
```

### Customization Options

1. **Change Ollama Model:**
   ```python
   # In app.py, line 19
   "model": "your-model-name"
   ```

2. **Add New Languages:**
   - Update language options in `templates/index.html`
   - Add corresponding language codes

3. **Modify Translation Prompts:**
   ```python
   # In app.py, translate_text function
   prompt = f"Your custom translation prompt..."
   ```

## API Endpoints

### Socket.IO Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client → Server | User connects |
| `join_chat` | Client → Server | Join chat room |
| `send_message` | Client → Server | Send message |
| `change_language` | Client → Server | Change language |
| `receive_message` | Server → Client | Receive message |
| `user_joined` | Server → Client | User joined notification |
| `user_left` | Server → Client | User left notification |
| `update_users` | Server → Client | Update user list |

## Troubleshooting

### Common Issues

1. **Ollama not responding:**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama
   ollama serve
   ```

2. **Translation not working:**
   - Verify Ollama model is installed: `ollama list`
   - Check model name in `app.py` matches installed model
   - Check Ollama logs for errors

3. **Connection issues:**
   - Ensure firewall allows port 5000
   - Check if Flask is binding to correct IP
   - Verify WebSocket connections aren't blocked

4. **Performance issues:**
   - Use smaller Ollama models for faster translation
   - Increase timeout values in `app.py`
   - Consider caching translations

### Debug Mode

Run with debug mode for development:
```bash
python app.py
# Debug mode is enabled by default
```

## Development

### Project Structure
```
ai-chat/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies  
├── README.md          # This file
├── templates/
│   └── index.html     # Chat interface
└── static/
    ├── style.css      # UI styling
    └── script.js      # Client-side logic
```

### Adding Features

1. **New Socket.IO Events**: Add to both `app.py` and `script.js`
2. **UI Components**: Modify `templates/index.html` and `static/style.css`
3. **Translation Models**: Update Ollama configuration in `app.py`

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn eventlet
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables for Production
```bash
export FLASK_ENV="production"
export SECRET_KEY="your-secure-secret-key"
export OLLAMA_URL="http://ollama-server:11434/api/generate"
```

## Performance Considerations

- **Ollama Model Size**: Smaller models = faster translation
- **Concurrent Users**: Test with your expected user load
- **Network Latency**: Consider Ollama server placement
- **Message History**: Limit stored messages for memory efficiency

## Security Notes

- Change the default `SECRET_KEY` for production
- Implement rate limiting for message sending
- Validate and sanitize user inputs
- Use HTTPS in production
- Consider authentication for private rooms

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Open an issue on GitHub
- Review Ollama documentation: https://ollama.ai/docs

---

**Built with ❤️ for multilingual communication**