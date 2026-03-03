# Quick Start Guide

Welcome to the Steel Structure Design System! This guide will help you get started in minutes.

## 🚀 Installation (One-Time Setup)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   # For Alibaba Cloud DashScope (Recommended for Chinese users)
   DASHSCOPE_API_KEY=your-api-key-here
   LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   LLM_MODEL=qwen-max

   # OR for OpenAI
   # OPENAI_API_KEY=your-openai-key
   # LLM_BASE_URL=https://api.openai.com/v1
   # LLM_MODEL=gpt-4-turbo-preview
   ```

### Step 3: Verify Installation

```bash
# Run tests to verify everything is working
python -m pytest tests/ -v
```

## 🎯 Usage

### Option 1: Use the Startup Scripts (EASIEST - RECOMMENDED)

**Linux/Mac:**
```bash
./start_agent.sh
```

**Windows:**
```bash
start_agent.bat
```

The startup script will:
- ✓ Check all dependencies
- ✓ Verify your configuration
- ✓ Give you a menu of options:
  1. Interactive Design Workflow (recommended for complete designs)
  2. Conversational Agent (recommended for Q&A and calculations)
  3. Quick Examples (recommended for learning)
  4. Run Tests (recommended for verification)

### Option 2: Direct Python Commands

#### Interactive Mode (Complete Design Workflow)
```bash
python integrated_design.py --mode interactive
```

**What it does:** Guide you through building design, structural analysis, and strength verification.

**Example workflow:**
```
Describe your building: A 2-story office building with 4 rooms per floor, each 20x15 feet

Dead load (psf) [default: 50]: 60
Live load (psf) [default: 40]: 50
Number of floors [default: 1]: 2

[System processes the design...]

✓ Blueprint saved to: output/blueprint.svg
✓ Analysis completed: output/opensees_analysis/
✓ Complete report: output/complete_design_report.json
```

#### Conversational Agent Mode
```bash
python -m agent.agent
```

**What it does:** Chat with an AI assistant for step-by-step guidance.

**Example conversation:**
```
User: Design a 3-story office building with 6 rooms per floor
Agent: I'll help you design this building. Let me start by...
      [Generates layout, analyzes loads, recommends sections]

User: What steel section should I use for columns carrying 200 kips?
Agent: For a 200 kip load, I recommend... [provides calculation]
```

#### Run Examples
```bash
python examples/examples_quickstart.py
```

**What it does:** Demonstrates the system capabilities with pre-configured examples.

## 📚 What Can This System Do?

### 1. Building Design (Task 3.1)
- 🏗️ Natural language building descriptions → room layouts
- 📐 Generate 3D blueprint SVG visualizations
- ⚖️ Calculate column loads automatically
- 🔧 Recommend optimal steel sections

### 2. Structural Analysis (Task 3.3)
- 🤖 Multi-agent system for geometry parsing
- 🔧 Automated OpenSeesPy code generation
- ⚡ Run structural analysis (forces, displacements)
- 📊 Generate engineering reports

### 3. Steel Strength Verification (Task 3.2)
- 🧮 PINN-based strength calculation
- 💬 Natural language interaction
- 📋 Multi-turn dialogue support
- ✅ Automated design checks

## 🎓 Learning Path

### For Beginners:
1. Start with **startup scripts** (start_agent.sh or start_agent.bat)
2. Choose option 3 "Run Quick Examples" to see demonstrations
3. Try option 1 "Interactive Design" with a simple building
4. Experiment with option 2 "Conversational Agent" for Q&A

### For Advanced Users:
1. Use `integrated_design.py` directly with Python API
2. Import modules in your own scripts:
   ```python
   from integrated_design import CompleteIntegratedSystem
   from agent.agent import SteelDesignAgent
   from openSeesIntegrate.opensees_integration import OpenSeesIntegrationSystem
   ```
3. Customize workflows by modifying the system modules
4. Extend with your own tools and agents

## 🔧 Troubleshooting

### Issue: "API key not set"
**Solution:** Make sure you've created `.env` and added your API key.

### Issue: "Model file not found"
**Solution:** Ensure `PINN model/normal/model_20250123_165719.pth` exists in the project directory.

### Issue: "Import error" or "Module not found"
**Solution:** Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Tests failing
**Solution:** Check if all dependencies are installed and API key is configured:
```bash
python -c "import openai, pydantic, torch, svgwrite, openseespy"
```

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [examples/](examples/) for more usage patterns
- Review [tests/](tests/) for code examples
- Check individual module documentation in source code

## 💡 Tips

1. **Start simple:** Begin with a single-story, few-room building
2. **Use examples:** Run `examples_quickstart.py` to learn by example
3. **Check outputs:** All results are saved in `output/` directory
4. **Ask questions:** Use conversational agent mode for guidance
5. **Read reports:** Generated JSON reports contain detailed results

## 🆘 Getting Help

- **In-app help:** Type `help` in agent mode
- **Command help:** Run `python integrated_design.py --help`
- **Contact:** kchen137@alumni.jh.edu

---

**Version:** v3.0.0
**Last Updated:** March 3, 2026
