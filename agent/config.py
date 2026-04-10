"""
Project configuration file
"""

PROJECT_NAME = "LLM Agent Framework for Structural Steel Design"
VERSION = "3.0.0"
AUTHOR = "Kai Chen"
EMAIL = "kchen137@alumni.jh.edu"

# Default configuration
DEFAULT_MODEL_PATH = "PINN model/normal/model_20250123_165719.pth"
DEFAULT_LLM_MODEL = "qwen-max"
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# Model parameters
PINN_INPUT_DIM = 6
PINN_HIDDEN_DIM = 64
PINN_OUTPUT_DIM = 1

# Physical constants
STEEL_ELASTIC_MODULUS = 29000  # ksi
LOG_SHIFT = 0.01  # Logarithmic transformation offset

# Parameter range (for validation)
PARAM_RANGES = {
    'A': (0.1, 100.0),      # in²
    'I': (1.0, 1000.0),     # in⁴
    'c': (0.1, 20.0),       # in
    'L': (12.0, 600.0),     # in
    'fy': (30.0, 100.0),    # ksi
    'delta_o': (0.01, 2.0)  # in
}

# Tool description
TOOLS_DESCRIPTION = {
    'calculate_column_strength': 'Calculate steel column compressive strength',
    'calculate_beam_strength': 'Calculate steel beam flexural strength (under development)',
    'design_building': 'Design a complete building from natural language description',
    'analyze_structure': 'Perform structural analysis using OpenSeesPy'
}

# User-friendly error messages
ERROR_MESSAGES = {
    'api_key_missing': """
API key not configured.

The system requires an API key.

1. Create a .env file in the project root if it does not exist:
   cp env.example .env

2. Edit .env and add your API key:

   For DashScope:
   DASHSCOPE_API_KEY=your-api-key-here
   LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   LLM_MODEL=qwen-max

   Or for OpenAI:
   OPENAI_API_KEY=your-openai-key
   LLM_BASE_URL=https://api.openai.com/v1
   LLM_MODEL=gpt-4-turbo-preview

3. Restart the application.

See QUICKSTART.md or README.md for more information.
""",

    'model_not_found': """
PINN model file not found.

The PINN model file is required for steel strength calculations.

Expected location: {model_path}

Please ensure:
1. The model file exists in the expected location.
2. You have downloaded the complete project files.

The system can still run in limited mode without this file,
but Task 3.2 will not be available.

See QUICKSTART.md or README.md for more information.
""",

    'dependency_missing': """
Required Python dependencies are missing.

To install all dependencies, run:
   pip install -r requirements.txt

Or install individual packages:
   pip install {missing_packages}

See QUICKSTART.md for more information.
"""
}

