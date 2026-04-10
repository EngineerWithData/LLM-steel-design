# Quick Start Guide

This guide covers installation, configuration, and the main ways to run the project.

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the environment

Copy the example environment file:

```bash
cp env.example .env
```

Then edit `.env` and provide an API key.

```bash
# DashScope
DASHSCOPE_API_KEY=your-api-key-here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-max

# Or OpenAI
# OPENAI_API_KEY=your-openai-key
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL=gpt-4-turbo-preview
```

### 3. Verify the setup

```bash
python -m pytest tests/ -v
```

## Running the project

### Option 1: Startup scripts

Linux/macOS:

```bash
./start_agent.sh
```

Windows:

```bash
start_agent.bat
```

The startup script checks dependencies, validates configuration, and offers these options:

1. Interactive design workflow
2. Conversational agent
3. Quick examples
4. Run tests

### Option 2: Direct Python commands

Interactive workflow:

```bash
python integrated_design.py --mode interactive
```

Conversational agent:

```bash
python -m agent.agent
```

Quick examples:

```bash
python examples/examples_quickstart.py
```

## Example workflow

```text
Describe your building: A 2-story office building with 4 rooms per floor, each 20x15 feet

Dead load (psf) [default: 50]: 60
Live load (psf) [default: 40]: 50
Number of floors [default: 1]: 2

[System processes the design...]

Blueprint saved to: output/blueprint.svg
Analysis completed: output/opensees_analysis/
Complete report: output/complete_design_report.json
```

## Capabilities

- Building layout generation from natural-language descriptions
- SVG blueprint generation
- Column load calculation and section recommendation
- Automated OpenSeesPy model generation and analysis
- PINN-based column strength verification
- Multi-turn conversational interaction

## Troubleshooting

### API key not set

Create `.env` and add a valid API key.

### Model file not found

Verify that `PINN model/normal/model_20250123_165719.pth` exists.

### Import or module errors

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Tests failing

Check that required packages are installed:

```bash
python -c "import openai, pydantic, torch, svgwrite, openseespy"
```

## Next steps

- Read [README.md](README.md) for full documentation
- Review the files in [examples/](examples/)
- Review the tests in [tests/](tests/)

## Contact

kchen137@alumni.jh.edu
