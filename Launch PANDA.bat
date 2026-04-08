@echo off
title PANDA - Plant Asset Truth Agent
echo ================================================
echo   Starting PANDA Desktop Application
echo   (32GB RAM + 12GB NVIDIA GPU)
echo ================================================

:: Kill any old Ollama instance
taskkill /F /IM ollama.exe >nul 2>&1

:: Start Ollama in background
start /min ollama serve

:: Wait for Ollama
timeout /t 5 >nul

:: Activate venv and start Gradio backend
call venv\Scripts\activate.bat

echo Starting Gradio backend...
start /min python app.py

:: Wait for Gradio to start
timeout /t 8 >nul

echo.
echo PANDA is launching...
echo ================================================

:: Launch the Tauri desktop app
cd src-tauri
cargo tauri dev

pause
