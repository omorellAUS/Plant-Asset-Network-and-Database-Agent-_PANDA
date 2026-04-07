@echo off
echo ================================================
echo   PANDA - Plant Asset Truth Agent Setup
echo   (32GB RAM + 12GB NVIDIA GPU - Windows 10)
echo ================================================

call venv\Scripts\activate.bat 2>nul || (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo Installing required packages...
pip install -r requirements.txt

echo Pulling models (first time may take a few minutes)...
ollama pull llama3.3:8b
ollama pull nomic-embed-text

echo ================================================
echo PANDA is ready! Launching web interface...
echo Open your browser to: http://127.0.0.1:7860
echo ================================================

python app.py
pause
