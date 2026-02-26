#!/bin/bash

# 钢结构设计Agent启动脚本

echo "======================================"
echo "  钢结构设计LLM Agent"
echo "======================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到.env文件"
    echo "正在从env.example创建.env..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✓ .env文件已创建，请编辑并填入你的API密钥"
        echo ""
        read -p "按Enter继续..."
    else
        echo "错误: env.example文件不存在"
        exit 1
    fi
fi

# 检查依赖
echo "检查依赖..."
python3 -c "import openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "警告: 缺少依赖包"
    read -p "是否安装依赖? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install -r requirements.txt
    fi
fi

# 检查模型文件
if [ ! -f "PINN model/normal/model_20250123_165719.pth" ]; then
    echo "警告: 未找到PINN模型文件"
    echo "路径: PINN model/normal/model_20250123_165719.pth"
    echo ""
fi

# 启动Agent
echo ""
echo "启动Agent..."
echo ""
cd agent
python3 agent.py

