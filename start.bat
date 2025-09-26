@echo off
echo Starting Multilingual Chat Application...
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Checking Ollama installation...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama is not running or not installed
    echo.
    echo Please:
    echo 1. Install Ollama from https://ollama.ai
    echo 2. Pull a model: ollama pull llama3.2
    echo 3. Start Ollama: ollama serve
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
)

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask application...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py