#!/bin/bash

echo "Starting Multilingual Chat Application..."
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

echo "Python version: $(python3 --version)"

# Check Ollama installation
echo "Checking Ollama installation..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "WARNING: Ollama is not running or not installed"
    echo
    echo "Please:"
    echo "1. Install Ollama from https://ollama.ai"
    echo "2. Pull a model: ollama pull llama3.2"
    echo "3. Start Ollama: ollama serve"
    echo
    read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo
echo "Starting Flask application..."
echo "Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo

python3 app.py