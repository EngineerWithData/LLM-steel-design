"""
Convert all Chinese content to English
This script will convert comments, docstrings, and prompts to English
"""

import os
import re

# Translation mappings
translations = {
    # File headers
    "LLM Agent主程序": "LLM Agent Main Program",
    "集成OpenAI API和钢构件强度计算工具": "Integrating OpenAI API and Steel Component Strength Calculation Tools",
    "PINN模型推理模块": "PINN Model Inference Module",
    "用于加载预训练的PINN模型并进行钢构件强度预测": "For loading pre-trained PINN models and predicting steel component strength",
    "钢构件强度计算工具": "Steel Component Strength Calculation Tools",
    "为LLM Agent提供的工具函数": "Tool functions provided for LLM Agent",
    
    # Common terms
    "加载环境变量": "Load environment variables",
    "钢结构设计LLM Agent": "Steel Structure Design LLM Agent",
    "初始化Agent": "Initialize Agent",
    "初始化API配置": "Initialize API configuration",
    "初始化OpenAI客户端": "Initialize OpenAI client",
    "兼容阿里云DashScope": "Compatible with Alibaba Cloud DashScope",
    "初始化工具": "Initialize tools",
    "对话历史": "Conversation history",
    "系统提示词": "System prompt",
    
    # Messages
    "警告": "Warning",
    "未设置API密钥": "API key not set",
    "请在.env文件中设置DASHSCOPE_API_KEY": "Please set DASHSCOPE_API_KEY in .env file",
    "LLM客户端已初始化": "LLM client initialized",
    "LLM客户端初始化失败": "LLM client initialization failed",
    "错误": "Error",
    "未配置": "not configured",
    "请设置": "Please set",
    "环境变量": "environment variable",
    
    # Function descriptions
    "与Agent对话": "Chat with Agent",
    "用户消息": "User message",
    "回复": "Response",
    "添加用户消息到历史": "Add user message to history",
    "构建消息列表": "Build message list",
    "调用LLM API": "Call LLM API",
    "如果需要调用工具": "If tool call is needed",
    "添加助手的响应到历史": "Add assistant response to history",
    "执行工具调用": "Execute tool call",
    "调用相应的工具": "Call corresponding tool",
    "未知的工具": "Unknown tool",
    "添加工具响应到历史": "Add tool response to history",
    "再次调用API获取最终响应": "Call API again to get final response",
    "没有工具调用，直接返回响应": "No tool call, return response directly",
    "发生错误": "Error occurred",
    "重置对话历史": "Reset conversation history",
    "获取对话历史": "Get conversation history",
    "加载PINN模型": "Load PINN model",
    "模型路径": "Model path",
    "模型已加载": "Model loaded",
    
    # Main function
    "主函数": "Main function",
    "命令行交互界面": "Command line interactive interface",
    "检查模型路径": "Check model path",
    "找到预训练模型": "Found pre-trained model",
    "未找到预训练模型": "Pre-trained model not found",
    "部分功能将不可用": "Some features will be unavailable",
    "Agent已启动": "Agent started",
    "输入": "Enter",
    "退出": "exit",
    "重置对话": "Reset conversation",
    "查看帮助": "View help",
    "对话已重置": "Conversation reset",
    "再见": "Goodbye",
    
    # Parameters
    "截面积": "Cross-sectional area",
    "惯性矩": "Moment of inertia",
    "距离": "Distance",
    "长度": "Length",
    "屈服强度": "Yield strength",
    "初始缺陷": "Initial imperfection",
    "钢柱": "Steel column",
    "钢梁": "Steel beam",
    "抗压强度": "Compressive strength",
    "抗弯强度": "Flexural strength",
    
    # Units
    "单位": "Unit",
    "平方英寸": "square inches",
    "英寸": "inches",
    "千磅每平方英寸": "ksi",
    
    # Test related
    "测试": "Test",
    "通过": "Passed",
    "失败": "Failed",
    "跳过": "Skipped",
    "所有测试完成": "All tests completed",
    "功能测试": "Functional test",
    "集成测试": "Integration test",
    "单元测试": "Unit test",
}

def convert_file(filepath):
    """Convert a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply translations
        for chinese, english in translations.items():
            content = content.replace(chinese, english)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main conversion function"""
    print("Starting conversion of Chinese content to English...")
    print("=" * 60)
    
    # Files to convert
    files_to_convert = [
        "agent/agent.py",
        "agent/models/pinn_predictor.py",
        "agent/tools/steel_strength_tools.py",
        "agent/config.py",
        "agent/utils/create_scalers.py",
    ]
    
    converted_count = 0
    for filepath in files_to_convert:
        if os.path.exists(filepath):
            if convert_file(filepath):
                print(f"✓ Converted: {filepath}")
                converted_count += 1
            else:
                print(f"- No changes: {filepath}")
        else:
            print(f"✗ Not found: {filepath}")
    
    print("=" * 60)
    print(f"Conversion completed. {converted_count} files modified.")

if __name__ == "__main__":
    main()

