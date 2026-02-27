# Steel Structure Design System - Complete User Guide

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [Features](#features)
5. [Tutorials](#tutorials)
6. [Example Scenarios](#example-scenarios)
7. [FAQ](#faq)
8. [Technical Support](#technical-support)

---

## 🎯 System Overview

An integrated intelligent steel structure design system that combines artificial intelligence with structural engineering expertise to help you complete the entire design workflow from building layout to steel member strength calculation.

### Core Features

✅ **Natural Language Building Design** - Describe buildings in plain language, system generates layout automatically  
✅ **3D Blueprint Visualization** - Automatically generate 3D perspective views  
✅ **Column Load Analysis** - Intelligently calculate loads on each column  
✅ **Section Optimization** - Automatically recommend most economical steel sections  
✅ **PINN Strength Calculation** - Use Physics-Informed Neural Networks for precise strength calculations  
✅ **Multi-turn Dialogue** - Intelligent assistant guides you through the design process  

### Target Users

- 🏗️ Structural Engineers
- 🎓 Civil Engineering Students
- 🏢 Architects
- 📐 Engineering Consultants
- 💡 Anyone interested in steel structure design

---

## ⚡ Quick Start

### Simplest Way to Use

1. **Open Terminal/Command Prompt**

2. **Navigate to Project Directory**
   ```bash
   cd /path/to/LLM_steel_design
   ```

3. **Run Startup Script**
   
   **Mac/Linux:**
   ```bash
   ./start_agent.sh
   ```
   
   **Windows:**
   ```cmd
   start_agent.bat
   ```

4. **Start Conversation**
   ```
   User: Hello, I want to calculate steel column strength
   Agent: Hello! I can help you calculate the compressive strength of a steel column. Please provide the following parameters...
   ```

---

## 🔧 Installation

### Step 1: Check Python Environment

Ensure Python 3.8 or higher is installed on your computer.

**Check method:**
```bash
python --version
# or
python3 --version
```

If Python is not installed, visit [python.org](https://www.python.org/downloads/) to download and install.

### Step 2: Download Project

**Method 1: Using Git (Recommended)**
```bash
git clone https://github.com/your-repo/LLM_steel_design.git
cd LLM_steel_design
```

**Method 2: Direct Download**
- Download ZIP file from GitHub
- Extract to your chosen directory
- Navigate to that directory in terminal

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you encounter network issues, use a mirror:**
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Step 4: Configure API Key

1. **Copy Configuration Template**
   ```bash
   cp env.example .env
   ```

2. **Edit .env File**
   
   Open `.env` file with any text editor and fill in your API key:
   
   ```bash
   # Using Alibaba Cloud DashScope (recommended for China)
   DASHSCOPE_API_KEY=your-dashscope-api-key-here
   LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   LLM_MODEL=qwen-max
   
   # Or using OpenAI
   # OPENAI_API_KEY=your-openai-api-key-here
   # LLM_BASE_URL=https://api.openai.com/v1
   # LLM_MODEL=gpt-4
   ```

3. **Get API Key**
   
   - **Alibaba Cloud DashScope**: Visit [dashscope.aliyun.com](https://dashscope.aliyun.com)
   - **OpenAI**: Visit [platform.openai.com](https://platform.openai.com)

### Step 5: Verify Installation

```bash
python -m agent.agent
```

If you see the following message, installation is successful:
```
====================================
Steel Structure Design LLM Agent
====================================

✓ LLM client initialized
✓ PINN model loaded
Agent started! Enter 'quit' or 'exit' to exit
```

---

## 🎨 Features

### Module 1: Steel Column Strength Calculation (Basic Feature)

**Description:** Calculate compressive strength of steel columns using PINN model

**Usage:**
```bash
./start_agent.sh
```

**Dialogue Example:**
```
User: Calculate column strength with A=10, I=100, c=5, L=120, fy=50, delta_o=0.1

Agent: I'll calculate the compressive strength for this steel column.

Parameter confirmation:
- Cross-sectional area A = 10 in²
- Moment of inertia I = 100 in⁴
- Distance c = 5 in
- Length L = 120 in
- Yield strength fy = 50 ksi
- Initial imperfection delta_o = 0.1 in

[Calling PINN model...]

Results:
- Predicted compressive strength: 450.2 kips
- Slenderness ratio: λ = 85.3
- Design recommendation: This column meets AISC specification requirements...
```

### Module 2: Building Layout Design (Integrated Feature)

**Description:** Describe building in natural language, automatically generate layout and 3D blueprint

**Usage:**
```bash
python integrated_design.py --mode interactive
```

**Dialogue Example:**
```
Command: design

Describe your building: I need an office building with 4 rooms, each 20x15 feet,
with a corridor connecting all rooms

Dead load (psf) [default: 50]: 60
Live load (psf) [default: 40]: 50
Number of floors [default: 1]: 2

[System processing...]

✓ Parsed 5 rooms (4 rooms + 1 corridor)
✓ Blueprint saved to: output/blueprint.svg
✓ Analyzed 20 columns
  Total load: 156,000 lbs
  Total steel weight: 8,450 lbs
✓ Complete design report saved to: output/design_report.json
```

### Module 3: Column Load Analysis

**Description:** Automatically calculate loads on each column and recommend sections

**Python API Usage:**
```python
from building_design import (
    parse_building_description,
    calculate_all_column_loads,
    optimize_column_section
)

# Parse building description
blueprint = parse_building_description("Building with 4 rooms, each 20x15 feet")

# Calculate column loads
column_loads = calculate_all_column_loads(
    blueprint,
    dead_load_psf=50,
    live_load_psf=40,
    num_floors=2
)

# Optimize section for each column
for col_name, load in column_loads.items():
    section = optimize_column_section(load)
    print(f"{col_name}: {section['type']} (capacity: {section['capacity']:.0f} lbs)")
```

---

## 📚 Tutorials

### Tutorial 1: First Time Use - Calculate Single Column Strength

**Scenario:** You have a steel column and need to know how much load it can support.

**Steps:**

1. **Start System**
   ```bash
   ./start_agent.sh
   ```

2. **Ask About Required Parameters**
   ```
   User: I want to calculate column strength, what parameters do I need?
   ```

3. **Agent Will Reply:**
   ```
   Agent: I need the following parameters to calculate column strength:
   
   1. A (cross-sectional area) - unit: in², typical: 5-50
   2. I (moment of inertia) - unit: in⁴, typical: 50-500
   3. c (distance) - from section center to edge, unit: in, typical: 2-10
   4. L (length) - effective column length, unit: in, typical: 60-300
   5. fy (yield strength) - steel yield strength, unit: ksi, typical: 36-70
   6. delta_o (initial imperfection) - unit: in, typical: 0.05-0.5
   
   You can provide all parameters at once or tell me one by one.
   ```

4. **Provide Parameters (Method 1: All at Once)**
   ```
   User: A=10, I=100, c=5, L=120, fy=50, delta_o=0.1
   ```

5. **Provide Parameters (Method 2: Step by Step)**
   ```
   User: A=10, I=100
   Agent: Recorded: cross-sectional area A=10 in², moment of inertia I=100 in⁴
         Still need: c, L, fy, delta_o
   
   User: c=5, L=120
   Agent: Continuing: c=5 in, L=120 in
         Still need: fy, delta_o
   
   User: fy=50, delta_o=0.1
   Agent: All parameters received, calculating...
   ```

6. **View Results**
   ```
   Agent: Calculation complete!
   
   Steel Column Strength Analysis:
   - Predicted compressive strength: 450.2 kips
   - Euler critical load: 523.6 kips
   - Slenderness ratio: 85.3
   - Utilization: 0.86
   
   Design Recommendations:
   ✓ Column meets AISC specification requirements
   ✓ Slenderness ratio within reasonable range
   ✓ Recommended safety factor: 1.67
   ```

### Tutorial 2: Design a Complete Building

**Scenario:** You need to design a small office building with multiple rooms.

**Steps:**

1. **Start Integrated System**
   ```bash
   python integrated_design.py --mode interactive
   ```

2. **Select Design Mode**
   ```
   Command: design
   ```

3. **Describe Your Building**
   ```
   Describe your building: 
   I need an office building with:
   - 4 offices, each 20x15 feet
   - 1 conference room, 30x20 feet
   - 1 corridor connecting all rooms
   Building height 10 feet
   ```

4. **Input Load Parameters**
   ```
   Dead load (psf) [default: 50]: 60
   Live load (psf) [default: 40]: 50
   Number of floors [default: 1]: 1
   ```

5. **System Processes Automatically**
   ```
   [Step 1/4] Parsing building description...
   ✓ Parsed 6 rooms
   
   [Step 2/4] Generating 3D blueprint...
   ✓ Blueprint saved to: output/blueprint.svg
   
   [Step 3/4] Analyzing column loads and designing sections...
   ✓ Analyzed 24 columns
     Total load: 132,000 lbs
     Total steel weight: 6,780 lbs
   
   [Step 4/4] Calculating detailed steel member strengths...
   
   Calculating strength for Column_(0.0,0.0) (W10x60)...
   Parameters: A=17.6 in², I=341.7 in⁴, L=120.0 in
   
   Agent: Based on PINN model calculation, this column's compressive strength is 792.0 kips...
   ```

6. **View Generated Files**
   ```
   output/
   ├── blueprint.svg          # 3D blueprint
   └── design_report.json     # Complete design report
   ```

7. **Open Blueprint**
   - Double-click `blueprint.svg` file
   - Or open in browser
   - You'll see the 3D perspective view of the building

### Tutorial 3: Batch Design Using Python API

**Scenario:** You need to compare multiple building design alternatives.

**Create Python Script:**

```python
# batch_design.py
from integrated_design import IntegratedDesignSystem

# Initialize system
system = IntegratedDesignSystem()

# Define multiple design alternatives
designs = [
    {
        "name": "Option A - Compact",
        "description": "4 rooms, each 15x15 feet, central corridor",
        "dead_load": 50,
        "live_load": 40,
        "floors": 1
    },
    {
        "name": "Option B - Spacious",
        "description": "4 rooms, each 25x20 feet, central corridor",
        "dead_load": 50,
        "live_load": 40,
        "floors": 1
    },
    {
        "name": "Option C - Multi-story",
        "description": "4 rooms, each 20x15 feet, central corridor",
        "dead_load": 60,
        "live_load": 50,
        "floors": 2
    }
]

# Batch processing
results = []
for design in designs:
    print(f"\nProcessing {design['name']}...")
    
    report = system.design_building(
        description=design['description'],
        dead_load_psf=design['dead_load'],
        live_load_psf=design['live_load'],
        num_floors=design['floors'],
        output_dir=f"output/{design['name']}"
    )
    
    results.append({
        "name": design['name'],
        "total_load": report['column_analysis']['summary']['total_load'],
        "steel_weight": report['column_analysis']['summary']['total_steel_weight'],
        "num_columns": report['column_analysis']['summary']['total_columns']
    })

# Comparison analysis
print("\n" + "="*60)
print("Design Comparison")
print("="*60)
for r in results:
    print(f"\n{r['name']}:")
    print(f"  Total load: {r['total_load']:,.0f} lbs")
    print(f"  Steel weight: {r['steel_weight']:,.0f} lbs")
    print(f"  Number of columns: {r['num_columns']}")
```

**Run Script:**
```bash
python batch_design.py
```

---

## 💡 Example Scenarios

### Scenario 1: Residential Design

```
User: Design a residence with:
- Living room 25x20 feet
- 3 bedrooms, each 15x12 feet
- Kitchen 15x12 feet
- 2 bathrooms, each 8x6 feet
- Corridor connecting all rooms

Dead load: 40 psf (lighter residential)
Live load: 40 psf (ASCE residential standard)
Floors: 2
```

### Scenario 2: Warehouse Design

```
User: Design a warehouse with:
- Main storage area 60x40 feet
- Office area 20x15 feet
- Loading dock 30x20 feet
Building height 15 feet

Dead load: 80 psf (heavy structure)
Live load: 125 psf (warehouse load)
Floors: 1
```

### Scenario 3: School Building

```
User: Design a school building with:
- 6 classrooms, each 30x25 feet
- 2 laboratories, each 35x30 feet
- 1 hall 40x30 feet
- Corridor connecting all rooms
Building height 12 feet

Dead load: 70 psf
Live load: 100 psf (classroom load standard)
Floors: 3
```

---

## ❓ FAQ

### Q1: What if I get "API key not set" error on startup?

**A:** You need to configure your API key:
1. Copy `env.example` to `.env`
2. Edit `.env` file and fill in your API key
3. Save and restart

### Q2: How do I get an API key?

**A:** 
- **Alibaba Cloud DashScope (recommended for China)**:
  1. Visit https://dashscope.aliyun.com
  2. Register/login
  3. Get API Key from console
  
- **OpenAI**:
  1. Visit https://platform.openai.com
  2. Register/login
  3. Create key in API Keys page

### Q3: What if dependency installation fails?

**A:** Try these methods:
```bash
# Method 1: Upgrade pip
python -m pip install --upgrade pip

# Method 2: Use mirror
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Method 3: Install individually
pip install torch numpy pandas scikit-learn matplotlib seaborn openai python-dotenv svgwrite
```

### Q4: What if PINN model file is not found?

**A:** 
- System will automatically detect model file
- Without model file, system can still run but won't use high-precision PINN calculations
- Model file should be at: `PINN model/normal/model_20250123_165719.pth`

### Q5: Can't open generated blueprint?

**A:** 
- Blueprint is in SVG format, can be opened in browser
- Can also use Adobe Illustrator, Inkscape, etc.
- For PDF format, open in browser and print to PDF

### Q6: How do I understand parameter meanings?

**A:** Main parameter descriptions:

| Parameter | Symbol | Unit | Description | Typical Range |
|-----------|--------|------|-------------|---------------|
| Cross-sectional Area | A | in² | Steel column cross-section | 5-50 |
| Moment of Inertia | I | in⁴ | Section moment of inertia | 50-500 |
| Distance | c | in | Center to edge distance | 2-10 |
| Length | L | in | Effective column length | 60-300 |
| Yield Strength | fy | ksi | Steel yield strength | 36-70 |
| Initial Imperfection | delta_o | in | Initial geometric imperfection | 0.05-0.5 |

### Q7: How reliable are the calculation results?

**A:** 
- PINN model trained on physics laws and extensive data
- Results comply with AISC specifications
- Recommendation: Important projects should be reviewed by professional engineers

### Q8: Can it be used for actual engineering?

**A:** 
- ✅ Can be used for preliminary design and alternative comparison
- ✅ Can be used for teaching and learning
- ⚠️ Actual engineering requires professional engineer review
- ⚠️ Need to consider more practical factors (seismic, wind loads, etc.)

### Q9: How to save conversation history?

**A:** 
```python
# In Python
from agent.agent import SteelDesignAgent

agent = SteelDesignAgent()
agent.chat("Calculate column strength...")

# Get conversation history
history = agent.get_conversation_history()

# Save to file
import json
with open('conversation.json', 'w') as f:
    json.dump(history, f, indent=2)
```

### Q10: What languages does the system support?

**A:** 
- System interface and documentation: Chinese and English
- LLM dialogue: Supports Chinese and English
- Technical terms: Follow international standards (AISC, ASCE, etc.)

---

## 🔬 Technical Support

### Report Issues

If you encounter problems, please provide:

1. **System Information**
   ```bash
   python --version
   pip list | grep -E "torch|openai|numpy"
   ```

2. **Error Information**
   - Complete error stack trace
   - Command you executed
   - Input parameters

3. **Submission Methods**
   - GitHub Issues
   - Email contact

### Advanced Usage

**Custom PINN Model:**
```python
from agent.agent import SteelDesignAgent

# Use custom model
agent = SteelDesignAgent(model_path="path/to/your/model.pth")
```

**Extend Functionality:**
```python
from building_design import column_analyzer

# Custom section library
custom_sections = [
    {"type": "Custom-1", "area": 30, "fy": 60, "cost_factor": 1.2},
    {"type": "Custom-2", "area": 40, "fy": 60, "cost_factor": 1.5}
]

section = column_analyzer.optimize_column_section(
    required_load=100000,
    available_sections=custom_sections
)
```

### Learning Resources

- **AISC Specifications**: [aisc.org](https://www.aisc.org)
- **Steel Structure Design**: Recommended textbook "Steel Design"
- **Python Programming**: [python.org/doc](https://docs.python.org)
- **Machine Learning**: [pytorch.org/tutorials](https://pytorch.org/tutorials)

---

## 📝 Changelog

### v2.0.0 (2025-02-27)
- ✨ Added building layout design feature
- ✨ Added 3D blueprint visualization
- ✨ Added column load analysis
- ✨ Added integrated design system
- 🌐 Complete English translation
- 📚 Added detailed user documentation

### v1.0.0 (2025-01-23)
- 🎉 Initial release
- ✅ PINN steel column strength calculation
- ✅ Multi-turn dialogue feature
- ✅ Intelligent parameter prompts

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Contributors

Thanks to all developers who contributed to this project!

---

## 📞 Contact

- **Project Homepage**: [GitHub Repository]
- **Issue Reporting**: [GitHub Issues]
- **Email**: your-email@example.com

---

**Enjoy using the system! Feel free to contact us with any questions.** 🎉

