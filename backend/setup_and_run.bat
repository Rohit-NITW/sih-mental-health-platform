@echo off
echo Setting up MindWell AI Chatbot Backend...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install -r requirements.txt

echo.
echo Dependencies installed successfully!
echo.

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file...
    echo # Add your Groq API key here > .env
    echo GROQ_API_KEY=your_groq_api_key_here >> .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your GROQ API key!
    echo You can get a free API key from: https://console.groq.com/
    echo.
    pause
)

echo Starting MindWell AI Chatbot Backend Server...
echo Server will be available at: http://localhost:8000
echo.
python mental_health_chatbot.py