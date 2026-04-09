@echo off
title PANDA - Fix & Run
echo ================================================
echo   PANDA - Killing ports + Running
echo ================================================

echo Killing port 7860...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :7860') do taskkill /F /PID %%a >nul 2>&1

echo Killing Ollama...
taskkill /F /IM ollama.exe >nul 2>&1

echo Activating venv...
call venv\Scripts\activate.bat

echo Starting Gradio...
python app.py

pause
