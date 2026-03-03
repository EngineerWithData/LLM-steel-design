#!/bin/bash

# Steel Structure Design Complete System Startup Script
# Integrated system with Task 3.1 (Building Design) + 3.2 (Strength) + 3.3 (Analysis)

echo "========================================================="
echo "  Steel Structure Design Complete System (v3.0)"
echo "========================================================="
echo "  Task 3.1: Building Design (Natural Language → Layout)"
echo "  Task 3.2: Steel Strength (PINN Model)"
echo "  Task 3.3: Structural Analysis (OpenSeesPy Integration)"
echo "========================================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 not found"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Show Python version
PYTHON_VERSION=$(python3 --version 2>&1)
echo "✓ Found $PYTHON_VERSION"

# Check .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠ Warning: .env file not found"
    if [ -f "env.example" ]; then
        echo "Creating .env from env.example..."
        cp env.example .env
        echo "✓ .env file created"
        echo ""
        echo "📝 Please edit .env and add your API key:"
        echo "   - For Alibaba Cloud: Set DASHSCOPE_API_KEY"
        echo "   - For OpenAI: Set OPENAI_API_KEY"
        echo ""
        read -p "Press Enter after editing .env to continue..." -r
    else
        echo "❌ Error: env.example file does not exist"
        exit 1
    fi
fi

# Check dependencies
echo ""
echo "Checking dependencies..."
MISSING_DEPS=()

python3 -c "import openai" 2>/dev/null || MISSING_DEPS+=("openai")
python3 -c "import pydantic" 2>/dev/null || MISSING_DEPS+=("pydantic")
python3 -c "import torch" 2>/dev/null || MISSING_DEPS+=("torch")
python3 -c "import svgwrite" 2>/dev/null || MISSING_DEPS+=("svgwrite")
python3 -c "import openseespy.opensees" 2>/dev/null || MISSING_DEPS+=("openseespy")

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo "⚠ Missing dependencies: ${MISSING_DEPS[*]}"
    echo ""
    read -p "Install missing dependencies? (y/n) [y]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "✓ Dependencies installed successfully"
        else
            echo "❌ Failed to install dependencies"
            exit 1
        fi
    else
        echo "⚠ Continuing without installing dependencies (some features may not work)"
    fi
else
    echo "✓ All dependencies installed"
fi

# Check model file
if [ ! -f "PINN model/normal/model_20250123_165719.pth" ]; then
    echo ""
    echo "⚠ Warning: PINN model file not found"
    echo "   Path: PINN model/normal/model_20250123_165719.pth"
    echo "   Note: Task 3.2 (strength calculation) requires this file"
    echo ""
fi

# Display startup menu
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "How would you like to start the system?"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1) 🎯 Interactive Design Workflow (Recommended)"
echo "   Best for: Complete building design from description"
echo "   Features: Building layout + Analysis + Strength check"
echo ""
echo "2) 💬 Conversational Agent Mode"
echo "   Best for: Chat-based assistance and calculations"
echo "   Features: Natural language Q&A, step-by-step guidance"
echo ""
echo "3) 📚 Run Quick Examples"
echo "   Best for: See demonstrations of system capabilities"
echo "   Features: Pre-configured example workflows"
echo ""
echo "4) ✅ Run Tests"
echo "   Best for: Verify system installation and functionality"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "Enter your choice (1-4) [1]: " choice
choice=${choice:-1}
echo ""

case $choice in
    1)
        echo "Starting Interactive Design Workflow..."
        echo ""
        python3 integrated_design.py --mode interactive
        ;;
    2)
        echo "Starting Conversational Agent..."
        echo ""
        echo "💡 Example conversations:"
        echo "   'Design a 2-story office building with 4 rooms'"
        echo "   'Analyze a portal frame with W14X90 sections'"
        echo "   'Calculate strength for a steel column'"
        echo ""
        python3 -m agent.agent
        ;;
    3)
        echo "Running Quick Examples..."
        echo ""
        python3 examples/examples_quickstart.py
        ;;
    4)
        echo "Running Tests..."
        echo ""
        python3 -m pytest tests/ -v --tb=short
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Thank you for using Steel Design System!"
echo "For help: See README.md or run 'python3 integrated_design.py --help'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
