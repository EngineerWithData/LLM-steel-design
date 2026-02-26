@echo off
REM 钢结构设计Agent启动脚本 (Windows)

echo ======================================
echo   钢结构设计LLM Agent
echo ======================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python
    pause
    exit /b 1
)

REM 检查.env文件
if not exist ".env" (
    echo 警告: 未找到.env文件
    if exist "env.example" (
        echo 正在从env.example创建.env...
        copy env.example .env
        echo 已创建.env文件，请编辑并填入你的API密钥
        echo.
        pause
    ) else (
        echo 错误: env.example文件不存在
        pause
        exit /b 1
    )
)

REM 检查依赖
echo 检查依赖...
python -c "import openai" 2>nul
if errorlevel 1 (
    echo 警告: 缺少依赖包
    set /p install="是否安装依赖? (y/n): "
    if /i "%install%"=="y" (
        pip install -r requirements.txt
    )
)

REM 检查模型文件
if not exist "PINN model\normal\model_20250123_165719.pth" (
    echo 警告: 未找到PINN模型文件
    echo 路径: PINN model\normal\model_20250123_165719.pth
    echo.
)

REM 启动Agent
echo.
echo 启动Agent...
echo.
cd agent
python agent.py
pause

