@echo off
REM Steel Structure Design Agent Startup Script (Windows)

echo ======================================
echo   Steel Structure Design LLM Agent
echo ======================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    pause
    exit /b 1
)

REM Check .env file
if not exist ".env" (
    echo Warning: .env file not found
    if exist "env.example" (
        echo Creating .env from env.example...
        copy env.example .env
        echo .env file created, please edit and fill in your API key
        echo.
        pause
    ) else (
        echo Error: env.example file does not exist
        pause
        exit /b 1
    )
)

REM Check dependencies
echo Checking dependencies...
python -c "import openai" 2>nul
if errorlevel 1 (
    echo Warning: Missing dependency packages
    set /p install="Install dependencies? (y/n): "
    if /i "%install%"=="y" (
        pip install -r requirements.txt
    )
)

REM Check model file
if not exist "PINN model\normal\model_20250123_165719.pth" (
    echo Warning: PINN model file not found
    echo Path: PINN model\normal\model_20250123_165719.pth
    echo.
)

REM Start Agent
echo.
echo Starting Agent...
echo.
python -m agent.agent
pause
