@echo off
echo 📄 Image to Word Converter - Windows Launcher
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist "app.py" (
    echo ❌ app.py not found in current directory
    echo Please run this script from the project directory
    pause
    exit /b 1
)

REM Install requirements if needed
echo 🔧 Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing requirements...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

REM Run the application
echo 🚀 Starting Image to Word Converter...
echo 📱 The application will open in your default web browser
echo 🔗 URL: http://localhost:8501
echo.
echo ⚠️  To stop the application, press Ctrl+C in this window
echo.

streamlit run app.py

if errorlevel 1 (
    echo ❌ Failed to run the application
    echo 💡 Try running manually: streamlit run app.py
    pause
)