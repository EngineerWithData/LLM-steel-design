@echo off
REM Steel Structure Design Complete System Startup Script (Windows)
REM Integrated system with Task 3.1 (Building Design) + 3.2 (Strength) + 3.3 (Analysis)

echo =========================================================
echo   Steel Structure Design Complete System (v3.0)
echo =========================================================
echo   Task 3.1: Building Design (Natural Language to Layout)
echo   Task 3.2: Steel Strength (PINN Model)
echo   Task 3.3: Structural Analysis (OpenSeesPy Integration)
echo =========================================================
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
python -c "import openai, pydantic, torch" 2>nul
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
    echo Note: Task 3.2 (strength calculation) requires this file
    echo.
)

REM Display menu
echo.
echo =========================================================
echo Select mode:
echo   1) Complete Integrated System (Recommended)
echo   2) Steel Strength Calculation Only (Task 3.2)
echo   3) Exit
echo =========================================================
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting Complete Integrated System...
    echo This includes all three tasks: Building Design, Analysis, and Strength Verification
    echo.
    python integrated_design.py --mode interactive
    pause
) else if "%choice%"=="2" (
    echo.
    echo Starting Steel Strength Calculator (Task 3.2 only)...
    echo.
    python -m agent.agent
    pause
) else if "%choice%"=="3" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Exiting...
    pause
    exit /b 1
)
