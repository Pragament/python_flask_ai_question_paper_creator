:: setup.bat
@echo off
echo Installing Python dependencies...
pip install .
echo Checking for Ollama...
where ollama >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Ollama not found. Please install it from https://ollama.ai/
    exit /b 1
)
echo Installing Ollama models...
ollama pull llama3
ollama pull gemma3:1b
ollama pull gemma2:2b
echo Setup complete. Run the app with: run-your-flask-app