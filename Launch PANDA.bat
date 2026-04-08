@echo off
title PANDA - Plant Asset and Network Database Agent
echo ================================================
echo   Starting PANDA - Plant Asset Truth Agent
echo   (32GB RAM + 12GB NVIDIA GPU)
echo ================================================

:: Kill any old Ollama instance first
taskkill /F /IM ollama.exe >nul 2>&1

:: Start Ollama in background
start /min ollama serve

:: Wait a few seconds for Ollama to start
timeout /t 5 >nul

:: Activate venv and launch PANDA
call venv\Scripts\activate.bat
echo PANDA is launching...
python app.py

pause
