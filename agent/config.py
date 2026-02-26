"""
项目配置文件
"""

PROJECT_NAME = "LLM Agent Framework for Structural Steel Design"
VERSION = "1.0.0"
AUTHOR = "Kai Chen"
EMAIL = "kchen137@alumni.jh.edu"

# 默认配置
DEFAULT_MODEL_PATH = "PINN model/normal/model_20250123_165719.pth"
DEFAULT_LLM_MODEL = "qwen-max"
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 模型参数
PINN_INPUT_DIM = 6
PINN_HIDDEN_DIM = 64
PINN_OUTPUT_DIM = 1

# 物理常数
STEEL_ELASTIC_MODULUS = 29000  # ksi
LOG_SHIFT = 0.01  # 对数变换偏移量

# 参数范围（用于验证）
PARAM_RANGES = {
    'A': (0.1, 100.0),      # in²
    'I': (1.0, 1000.0),     # in⁴
    'c': (0.1, 20.0),       # in
    'L': (12.0, 600.0),     # in
    'fy': (30.0, 100.0),    # ksi
    'delta_o': (0.01, 2.0)  # in
}

# 工具描述
TOOLS_DESCRIPTION = {
    'calculate_column_strength': '计算钢柱抗压强度',
    'calculate_beam_strength': '计算钢梁抗弯强度（开发中）'
}

