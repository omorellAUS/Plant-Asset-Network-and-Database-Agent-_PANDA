@echo off
title PANDA - Plant Asset and Network Database Agent
echo ================================================
echo   Starting PANDA - Plant Asset Truth Agent
echo   (32GB RAM + 12GB NVIDIA GPU)
echo ================================================

:: Kill any old Ollama instance to avoid port conflicts
taskkill /F /IM ollama.exe >nul 2>&1

:: Start Ollama in the background
start /min ollama serve

:: Wait a few seconds for Ollama to start
timeout /t 5 >nul

:: Activate venv and launch PANDA
call venv\Scripts\activate.bat

echo.
echo PANDA is launching...
echo Open your browser to: http://127.0.0.1:7860
echo.
echo (Do not close this window while PANDA is running)
echo ================================================

python app.py

pause
