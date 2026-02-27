#!/bin/bash

# Steel Structure Design Agent Startup Script

echo "======================================"
echo "  Steel Structure Design LLM Agent"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found"
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found"
    echo "Creating .env from env.example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✓ .env file created, please edit and fill in your API key"
        echo ""
        read -p "Press Enter to continue..."
    else
        echo "Error: env.example file does not exist"
        exit 1
    fi
fi

# Check dependencies
echo "Checking dependencies..."
python3 -c "import openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: Missing dependency packages"
    read -p "Install dependencies? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install -r requirements.txt
    fi
fi

# Check model file
if [ ! -f "PINN model/normal/model_20250123_165719.pth" ]; then
    echo "Warning: PINN model file not found"
    echo "Path: PINN model/normal/model_20250123_165719.pth"
    echo ""
fi

# Start Agent
echo ""
echo "Starting Agent..."
echo ""
cd agent
python3 agent.py
