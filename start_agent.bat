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
    echo [X] Error: Python not found
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found %PYTHON_VERSION%

REM Check .env file
if not exist ".env" (
    echo.
    echo [!] Warning: .env file not found
    if exist "env.example" (
        echo Creating .env from env.example...
        copy env.example .env
        echo [OK] .env file created
        echo.
        echo Please edit .env and add your API key:
        echo    - For Alibaba Cloud: Set DASHSCOPE_API_KEY
        echo    - For OpenAI: Set OPENAI_API_KEY
        echo.
        pause
    ) else (
        echo [X] Error: env.example file does not exist
        pause
        exit /b 1
    )
)

REM Check dependencies
echo.
echo Checking dependencies...
set MISSING_DEPS=

python -c "import openai" 2>nul || set MISSING_DEPS=%MISSING_DEPS% openai
python -c "import pydantic" 2>nul || set MISSING_DEPS=%MISSING_DEPS% pydantic
python -c "import torch" 2>nul || set MISSING_DEPS=%MISSING_DEPS% torch
python -c "import svgwrite" 2>nul || set MISSING_DEPS=%MISSING_DEPS% svgwrite
python -c "import openseespy.opensees" 2>nul || set MISSING_DEPS=%MISSING_DEPS% openseespy

if not "%MISSING_DEPS%"=="" (
    echo.
    echo [!] Missing dependencies:%MISSING_DEPS%
    echo.
    set /p install="Install missing dependencies? (y/n) [y]: "
    if /i not "%install%"=="n" (
        echo Installing dependencies...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo [X] Failed to install dependencies
            pause
            exit /b 1
        ) else (
            echo [OK] Dependencies installed successfully
        )
    ) else (
        echo [!] Continuing without installing dependencies (some features may not work)
    )
) else (
    echo [OK] All dependencies installed
)

REM Check model file
if not exist "PINN model\normal\model_20250123_165719.pth" (
    echo.
    echo [!] Warning: PINN model file not found
    echo    Path: PINN model\normal\model_20250123_165719.pth
    echo    Note: Task 3.2 (strength calculation) requires this file
    echo.
)

REM Display startup menu
echo.
echo ================================================================
echo How would you like to start the system?
echo ================================================================
echo.
echo 1) Interactive Design Workflow (Recommended)
echo    Best for: Complete building design from description
echo    Features: Building layout + Analysis + Strength check
echo.
echo 2) Conversational Agent Mode
echo    Best for: Chat-based assistance and calculations
echo    Features: Natural language Q&A, step-by-step guidance
echo.
echo 3) Run Quick Examples
echo    Best for: See demonstrations of system capabilities
echo    Features: Pre-configured example workflows
echo.
echo 4) Run Tests
echo    Best for: Verify system installation and functionality
echo.
echo ================================================================
set /p choice="Enter your choice (1-4) [1]: "
if "%choice%"=="" set choice=1
echo.

if "%choice%"=="1" (
    echo Starting Interactive Design Workflow...
    echo.
    python integrated_design.py --mode interactive
) else if "%choice%"=="2" (
    echo Starting Conversational Agent...
    echo.
    echo Example conversations:
    echo    'Design a 2-story office building with 4 rooms'
    echo    'Analyze a portal frame with W14X90 sections'
    echo    'Calculate strength for a steel column'
    echo.
    python -m agent.agent
) else if "%choice%"=="3" (
    echo Running Quick Examples...
    echo.
    python examples\examples_quickstart.py
) else if "%choice%"=="4" (
    echo Running Tests...
    echo.
    python -m pytest tests/ -v --tb=short
) else (
    echo [X] Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Thank you for using Steel Design System!
echo For help: See README.md or run 'python integrated_design.py --help'
echo ================================================================
pause
