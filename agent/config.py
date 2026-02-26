"""
Project configuration file
"""

PROJECT_NAME = "LLM Agent Framework for Structural Steel Design"
VERSION = "1.0.0"
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

# Parameter range（For validation）
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
    'calculate_beam_strength': 'Calculate steel beam flexural strength（开发中）'
}

