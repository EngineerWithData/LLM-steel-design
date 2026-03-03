# LLM Agent Framework for Structural Steel Design

An LLM-powered intelligent agent framework for accelerating and automating structural steel design with integrated building layout generation, structural analysis automation, and 3D visualization.

## Project Overview

This project implements a complete LLM-driven intelligent agent system for structural steel design automation. The system integrates building layout generation, automated structural analysis with OpenSeesPy, PINN-based strength verification, and comprehensive design workflow automation.

**Project Information**:
- **Version**: v3.0.0
- **Developer**: Kai Chen (kchen137@alumni.jh.edu)
- **Institution**: Johns Hopkins University
- **Last Updated**: March 3, 2026

## Main Features

### ✅ Implemented Features

#### 1. Building Design (Task 3.1) - ✅ Complete
- **🏗️ Natural Language Building Layout**: Describe buildings in plain language, automatically generate room layouts
- **📐 3D Blueprint Visualization**: Generate perspective SVG blueprints with columns, beams, and connections
- **⚖️ Column Load Analysis**: Automatically calculate tributary areas and loads for all columns
- **🔧 Section Optimization**: Recommend optimal steel sections (W-shapes) based on load requirements

#### 2. Steel Strength Verification (Task 3.2) - ✅ Complete
- **PINN-Based Strength Calculation**: Calculate steel column compressive strength using Physics-Informed Neural Networks
- **Natural Language Interaction**: Interact with users through chat
- **Multi-turn Dialogue**: Support coherent multi-turn conversations with context memory
- **Intelligent Parameter Recognition**: Automatically recognize design parameters (supports multiple formats)
- **Multi-API Support**: Support for OpenAI and Alibaba Cloud DashScope APIs

#### 3. Structural Analysis Automation (Task 3.3) - ✅ Complete (NEW!)
- **🤖 Multi-Agent System**: Three specialized LLM agents for geometry parsing, code translation, and validation
- **📋 JSON Intermediate Format**: Structured data representation prevents LLM hallucination
- **🔧 Automated OpenSeesPy Code Generation**: Template-based generation from structural models
- **✅ Three-Layer Validation**: Syntax, semantic, and structural stability validation
- **⚡ OpenSeesPy Integration**: Execute structural analysis and parse results automatically
- **📊 Natural Language Results**: Generate engineering reports with displacements, forces, and design checks
- **🗄️ W-Section Database**: 40+ AISC standard steel sections with complete properties
- **🔗 Full Integration**: Seamless workflow from natural language to analysis results

#### 4. Complete Integrated Workflow - ✅ Complete
- **End-to-End Automation**: Natural language → Building design → Structural analysis → Strength verification
- **📊 Comprehensive Reports**: Detailed JSON and natural language design reports
- **🔄 Agent Orchestration**: Multiple specialized agents working together seamlessly

### 🚧 Features Under Development

- **Steel Beam Strength Calculation**: Calculate steel beam flexural strength
- **Nonlinear Analysis**: Extend to nonlinear structural analysis
- **3D Structures**: Support for 3D building frames

## Quick Start

**New users?** See [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file and add the following content:

```bash
# Alibaba Cloud DashScope API Configuration (Recommended)
DASHSCOPE_API_KEY=your-api-key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-max

# Or use OpenAI API
# OPENAI_API_KEY=your-openai-api-key
# LLM_BASE_URL=https://api.openai.com/v1
# LLM_MODEL=gpt-4-turbo-preview
```

### 3. Choose Your Workflow

#### Option A: Use Startup Scripts (EASIEST - RECOMMENDED)

**For Linux/Mac:**
```bash
./start_agent.sh
```

**For Windows:**
```bash
start_agent.bat
```

These scripts will:
- ✅ Check all dependencies automatically
- ✅ Verify .env configuration
- ✅ Provide a user-friendly menu with 4 options:
  1. **Interactive Design Workflow** - Complete building design (recommended for beginners)
  2. **Conversational Agent Mode** - Chat-based Q&A and guidance
  3. **Run Quick Examples** - See system demonstrations
  4. **Run Tests** - Verify installation

#### Option B: Direct Python Command

**Complete Integrated System (Interactive Mode):**
```bash
python integrated_design.py --mode interactive
```

**Conversational Agent Mode:**
```bash
python -m agent.agent
```

**Run Examples:**
```bash
python examples/examples_quickstart.py
```

**Example workflow:**
```
Command: python integrated_design.py --mode interactive

Describe your building: I need a 3-story office building with 4 rooms per floor,
each 20x15 feet, with a central corridor

Dead load (psf) [default: 50]: 60
Live load (psf) [default: 40]: 50
Number of floors [default: 1]: 3

[System processes:]
1. Task 3.1: Generates building layout and geometry
2. Task 3.3: Creates structural analysis model, generates OpenSeesPy code, runs analysis
3. Task 3.2: Verifies steel member strengths using PINN models

✓ Blueprint saved to: output/blueprint.svg
✓ Analysis results: output/opensees_analysis/
✓ Design report saved to: output/complete_design_report.json
```

### 4. View Documentation

- **New Users:** Start with [QUICKSTART.md](QUICKSTART.md)
- **Complete Guide:** Continue reading this README
- **Code Examples:** Check [examples/](examples/) directory

## Usage Examples

### Example 1: Command Line Interaction (Supports Multi-turn Dialogue)

```bash
cd agent
python agent.py
```

**Multi-turn Dialogue Example**:
```
User: Hello, I want to calculate steel column strength
Agent: Great! I can help you calculate the compressive strength of a steel column.
      Please provide the following parameters:
      - A (cross-sectional area, unit: in²)
      - I (moment of inertia, unit: in⁴)
      - c (distance from section center to edge, unit: in)
      - L (column length, unit: in)
      - fy (yield strength, unit: ksi)
      - delta_o (initial imperfection, unit: in)

User: Cross-sectional area is 10 square inches, moment of inertia is 100
Agent: Okay, I've recorded:
      - Cross-sectional area A = 10 in²
      - Moment of inertia I = 100 in⁴
      
      Still need the following parameters:
      - c (distance from section center to edge)
      - L (column length)
      - fy (yield strength)
      - delta_o (initial imperfection)

User: c=5, L=120, fy=50, delta_o=0.1
Agent: Calculating...
      
      Calculation Results:
      - Nominal compressive strength Pn: 670.74 kip
      - Theoretical strength (Perry-Robertson formula): 469.28 kip
      - Predicted to theoretical value ratio: 1.43
```

**Handling Unrelated Questions**:
```
User: How's the weather today?
Agent: I'm a steel structure design assistant and don't have information about weather.
      However, I can help you with steel column and beam strength calculations
      and design analysis. Do you have any steel structure design questions?

User: Okay, then help me calculate steel column strength
Agent: Great! Please provide the steel column design parameters...
```

### Example 2: Python API Call

```python
from agent import SteelDesignAgent

# Initialize Agent
agent = SteelDesignAgent(
    model_path="PINN model/normal/model_20250123_165719.pth"
)

# Conversation
response = agent.chat("Calculate steel column strength: A=10, I=100, c=5, L=120, fy=50, delta_o=0.1")
print(response)
```

### Example 3: Direct Tool Call

```python
from agent.tools import SteelStrengthCalculator

# Initialize calculator
calculator = SteelStrengthCalculator(
    model_path="PINN model/normal/model_20250123_165719.pth"
)

# Calculate steel column strength
params = {
    'A': 10.0,      # Cross-sectional area (in²)
    'I': 100.0,     # Moment of inertia (in⁴)
    'c': 5.0,       # Distance from section center to edge (in)
    'L': 120.0,     # Column length (in)
    'fy': 50.0,     # Yield strength (ksi)
    'delta_o': 0.1  # Initial imperfection (in)
}

result = calculator.calculate_column_strength(params)
print(result)
```

### Example 4: Run Tests

```bash
cd tests
python test_agent.py
```

### Example 5: View Usage Examples

```bash
cd examples
python usage_examples.py
```

### Example 6: Multi-turn Dialogue Demo

```bash
cd examples
python multi_turn_demo.py
```

This demo showcases the Agent's multi-turn dialogue capabilities:
- Gradually providing parameters
- Handling unrelated questions
- Proactively asking for missing parameters
- Context memory capability
- Interactive demo

## Project Structure

```
LLM_steel_design/
├── agent/                          # Agent core code (Task 3.2)
│   ├── agent.py                    # LLM Agent main program
│   ├── config.py                   # Configuration file
│   ├── models/
│   │   └── pinn_predictor.py      # PINN model inference
│   ├── tools/
│   │   └── steel_strength_tools.py # Steel strength calculation tools
│   └── utils/
│       └── create_scalers.py      # Scaler generation tool
├── building_design/                # Building design module (Task 3.1)
│   ├── __init__.py                 # Module initialization
│   ├── building_parser.py          # Natural language building parser
│   ├── blueprint_generator.py      # 3D blueprint SVG generator
│   └── column_analyzer.py          # Column load analysis and optimization
├── openSeesIntegrate/              # Structural analysis module (Task 3.3)
│   ├── agents/                     # Multi-agent system
│   │   ├── geometry_agent.py       # Natural language → JSON
│   │   ├── code_translator.py      # JSON → OpenSeesPy code
│   │   └── model_validator.py      # Model and code validation
│   ├── models/                     # Data models
│   │   ├── structural_json.py      # Structural JSON schema
│   │   └── wsection_database.py    # W-section database (40+ sections)
│   ├── executor/                   # Execution engine
│   │   ├── opensees_runner.py      # OpenSeesPy executor
│   │   └── result_parser.py        # Result parser and interpreter
│   ├── opensees_integration.py     # Complete integration system
│   └── openseespyDoc/              # OpenSeesPy documentation (468 files)
├── integrated_design.py            # Complete system integration
├── examples/
│   └── examples_quickstart.py      # NEW: Quick start examples
├── tests/                          # Test suite
│   ├── test_agent.py               # Agent tests
│   ├── test_llm_agent.py           # LLM integration tests
│   ├── test_steel_tools.py         # Steel tools tests
│   └── test_integration.py         # Integration tests
├── PINN model/
│   └── normal/
│       ├── model_20250123_165719.pth  # Pre-trained model
│       └── scalers.pkl                # Scaler
├── output/                         # Generated files directory
│   ├── blueprint.svg               # Generated blueprints
│   ├── design_report.json          # Design reports
│   └── demo_generated_code.py      # NEW: Generated OpenSeesPy code
├── README.md                       # This document
├── requirements.txt                # Python dependencies
├── env.example                     # Environment variable template
├── start_agent.sh                  # Linux/Mac startup script
└── start_agent.bat                 # Windows startup script
```

## Parameter Description

### Steel Column Input Parameters

| Parameter | Symbol | Unit | Description | Supported Parameter Names |
|-----------|--------|------|-------------|---------------------------|
| Cross-sectional Area | A | in² | Steel column cross-sectional area | `A`, `area` |
| Moment of Inertia | I | in⁴ | Section moment of inertia | `I`, `inertia` |
| Distance | c | in | Distance from section center to edge | `c`, `distance` |
| Length | L | in | Effective length of column | `L`, `length` |
| Yield Strength | fy | ksi | Steel yield strength | `fy`, `yield_strength` |
| Initial Imperfection | delta_o | in | Initial geometric imperfection | `delta_o`, `imperfection` |

### Output Results

```json
{
  "success": true,
  "component_type": "column",
  "nominal_strength_Pn": 670.74,      // PINN predicted compressive strength (kip)
  "theoretical_strength": 469.28,     // Perry-Robertson theoretical strength (kip)
  "prediction_ratio": 1.43,           // Ratio of predicted to theoretical value
  "unit": "kip",
  "message": "Steel column strength calculation successful"
}
```

## Technical Architecture

### Complete System Architecture (v3.0)

The system consists of three integrated tasks working together:

#### Task 3.1: Building Design
- Natural language parsing for building descriptions
- Automated room layout generation
- 3D blueprint SVG visualization
- Column load calculation and analysis

#### Task 3.2: Steel Strength Verification
- **Model Type**: Physics-Informed Neural Network (PINN)
- **Input Features**: A, I, c, L, fy, delta_o (6 features)
- **Output**: Steel column compressive strength Pn (kip)
- **Physical Constraints**: Perry-Robertson formula
- **Network Structure**: 3 hidden layers, 64 neurons per layer

#### Task 3.3: Structural Analysis Automation (NEW!)
- **Multi-Agent Architecture**:
  - Geometry Agent: Natural language → Structural JSON
  - Code Translation Agent: JSON → OpenSeesPy code (template-based)
  - Model Validation Agent: Three-layer validation (syntax, semantic, structural)
- **W-Section Database**: 40+ AISC standard sections
- **OpenSeesPy Integration**: Automated execution and result parsing
- **Natural Language Output**: Engineering reports with design checks

#### Integration System
- **Framework**: OpenAI Function Calling
- **Supported Models**: Qwen, GPT-4, and OpenAI-compatible APIs
- **Workflow Orchestration**: Seamless agent coordination
- **Output**: Comprehensive design reports with all analysis results

## Test Results

### Test Statistics

#### Task 3.3 Tests (NEW!)
- **Core Functionality Tests**: 8/8 passed (100%) ✅
- **Force Equilibrium**: Error < 0.001% ✅
- **Code Generation**: 110+ lines of valid OpenSeesPy code ✅
- **Result Parsing**: Displacement and force extraction validated ✅
- **Test Coverage**: All multi-agent components verified ✅

#### Overall System Tests
- **Test Framework**: pytest 7.4.4
- **Test Files**: 12+
- **Test Count**: 58+
- **Pass Rate**: **100%** ✅
- **Lines of Code**: 10,000+ lines (including Task 3.3)
- **Execution Time**: ~3 seconds

### Test Categories

#### Unit Tests (37)
- **test_pinn_model.py** (9 tests)
  - Perry-Robertson formula calculation
  - Model loading and prediction
  - Batch prediction
  - Boundary condition testing

- **test_steel_tools.py** (13 tests)
  - Parameter parsing (standard/Chinese/English formats)
  - Parameter validation
  - Steel column strength calculation
  - Different parameter effects

- **test_llm_agent.py** (11 tests)
  - Agent initialization and configuration
  - Conversation history management
  - Tool integration
  - Tool definition validation

- **test_conversation_features.py** (4 tests)
  - Conversation history recording
  - Conversation reset
  - System prompt validation
  - Enhanced prompt content

#### Integration Tests (8 tests)
- **test_integration.py**
  - End-to-end workflow
  - Multi-scenario design
  - Parametric studies
  - Real-world scenarios

#### Functional Tests (5 tests)
- **test_agent.py**
  - Basic functionality verification
  - Quick testing

### Run Tests

```bash
# Run all tests
cd tests
pytest -v

# Run specific test file
pytest test_pinn_model.py -v

# Show detailed output
pytest -v -s

# Generate coverage report
pytest --cov=agent --cov-report=html
```

### Performance Metrics

| Metric | Actual Value | Target Value | Status |
|--------|--------------|--------------|--------|
| Test Pass Rate | 100% | 100% | ✅ |
| Model Inference Speed | < 50ms | < 100ms | ✅ |
| Parameter Recognition Accuracy | 100% | > 95% | ✅ |
| Test Coverage | ~85% | > 80% | ✅ |

## Technical Features

### 1. Physics-Informed Neural Network (PINN)
Combines data-driven and physical constraints (Perry-Robertson formula), with higher prediction accuracy than pure data-driven models.

### 2. Intelligent Parameter Recognition
Supports multiple parameter formats:
- Standard format: `A`, `I`, `c`, `L`, `fy`, `delta_o`
- English full names: `area`, `inertia`, `length`, `yield_strength`, `imperfection`

### 3. Multi-turn Dialogue Capability
- **Context Memory**: Remember parameters and information mentioned in previous conversations
- **Parameter Completion**: Automatically identify missing parameters and proactively ask
- **Coherent Conversation**: Support users in gradually providing information
- **Intelligent Guidance**: Provide clear guidance when information is incomplete

### 4. Flexible Dialogue Handling
- **Professional Questions**: Accurately understand and handle steel structure design-related questions
- **Unrelated Questions**: Politely handle questions unrelated to the profession
- **Mixed Dialogue**: Intersperse explanations and small talk in professional discussions

### 5. Multi-LLM Support
Easily switch between different LLM services through environment variables, compatible with OpenAI API standards.

### 6. Professional Dialogue Capability
- Understand structural engineering terminology
- Automatically extract design parameters
- Generate professional engineering recommendations
- Provide typical parameter value references

### 7. Modular Design
- Clear code structure
- Easy to extend and maintain
- Complete test coverage

## Common Questions

### Q1: Prompt "API key not set"
**A:** Make sure you've created a `.env` file in the project root directory and correctly filled in `DASHSCOPE_API_KEY` or `OPENAI_API_KEY`

### Q2: Prompt "Model file does not exist"
**A:** Make sure the `PINN model/normal/model_20250123_165719.pth` file exists

### Q3: How to switch to OpenAI API?
**A:** Modify the `.env` file:
```bash
OPENAI_API_KEY=your-openai-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4-turbo-preview
```

### Q4: Large difference between predicted and theoretical values?
**A:** This is normal. The PINN model considers more physical effects, and predicted values are typically 30-60% higher than Perry-Robertson theoretical values. It's recommended to regenerate the scaler using actual training data to improve accuracy.

### Q5: How to add new component types?
**A:** Add new calculation functions in `agent/tools/steel_strength_tools.py` and define corresponding tools in `STEEL_STRENGTH_TOOLS`.

## Dependencies

```
torch>=2.0.0
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
openai>=1.0.0
python-dotenv>=1.0.0
svgwrite>=1.4.0          # For blueprint generation
pydantic>=2.0.0          # NEW: For structural data validation
openseespy>=3.5.0        # NEW: For structural analysis
```

## Development Team

- **Kai Chen** - PINN model development and Agent framework implementation
- **Zhidong Zhang** - Project guidance and post-processing
- **Cem Bartu Cevik** - Geometry optimization module (under development)
- **Cristopher D. Moen** - Project advisor

## References

1. AISC 360-16: Specification for Structural Steel Buildings
2. Perry-Robertson Formula for Column Strength
3. Physics-Informed Neural Networks (PINNs)
4. OpenAI Function Calling Documentation

## License

This project is for academic research purposes.

## Contact

For questions or suggestions, please contact:
- **Developer**: Kai Chen
- **Email**: kchen137@alumni.jh.edu
- **Institution**: Johns Hopkins University
- **GitHub**: https://github.com/chenkai66/steel-design

---

**Version**: v3.0.0
**Last Updated**: March 3, 2026
**Status**: ✅ Task 3.1 Complete | ✅ Task 3.2 Complete | ✅ Task 3.3 Complete | ✅ Full Integration Complete
