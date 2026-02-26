#!/usr/bin/env python3
"""
Batch convert all Chinese content to English in the project
"""

import os
import sys

def convert_file_to_english(filepath, backup=True):
    """Convert a single file to English"""
    
    # Chinese to English mappings
    replacements = {
        # Common comments
        "钢构件强度计算工具": "Steel Component Strength Calculation Tools",
        "为LLM Agent提供的工具函数": "Tool functions provided for LLM Agent",
        "钢构件强度计算器工具类": "Steel Component Strength Calculator Tool Class",
        "初始化计算器": "Initialize calculator",
        "计算钢柱抗压强度": "Calculate steel column compressive strength",
        "钢柱参数字典": "Steel column parameter dictionary",
        "计算结果": "Calculation result",
        "参数映射和单位转换": "Parameter mapping and unit conversion",
        "调用PINN模型预测": "Call PINN model for prediction",
        "计算钢梁抗弯强度": "Calculate steel beam flexural strength",
        "预留接口": "Reserved interface",
        "钢梁参数字典": "Steel beam parameter dictionary",
        "功能开发中": "Feature under development",
        "敬请期待": "Stay tuned",
        "解析和验证钢柱参数": "Parse and validate steel column parameters",
        "原始参数字典": "Original parameter dictionary",
        "标准化的参数字典": "Standardized parameter dictionary",
        "必需参数": "Required parameters",
        "截面积": "Cross-sectional area",
        "惯性矩": "Moment of inertia",
        "距离": "Distance",
        "长度": "Length",
        "屈服强度": "Yield strength",
        "初始缺陷": "Initial imperfection",
        "可用键名": "Available key names",
        "缺少必要参数": "Missing required parameter",
        "参数验证": "Parameter validation",
        "必须大于": "must be greater than",
        "参数类型错误": "Parameter type error",
        "参数解析失败": "Parameter parsing failed",
        "获取工具描述": "Get tool description",
        "供LLM理解": "For LLM understanding",
        "钢柱参数说明": "Steel column parameter description",
        "单位": "Unit",
        "平方英寸": "square inches",
        "四次方英寸": "to the fourth power inches",
        "英寸": "inches",
        "千磅每平方英寸": "ksi",
        "返回结果": "Return result",
        "名义抗压强度": "Nominal compressive strength",
        "理论强度": "Theoretical strength",
        "预测值与理论值的比值": "Ratio of predicted to theoretical value",
        "示例调用": "Example call",
        "测试工具": "Test tool",
        "钢柱强度计算结果": "Steel column strength calculation result",
        
        # Test related
        "测试脚本": "Test script",
        "验证Agent功能": "Verify Agent functionality",
        "测试PINN模型预测器": "Test PINN model predictor",
        "初始化预测器": "Initialize predictor",
        "不加载模型": "Do not load model",
        "仅测试Perry-Robertson公式": "Only test Perry-Robertson formula",
        "测试数据": "Test data",
        "输入参数": "Input parameters",
        "理论强度": "Theoretical strength",
        "PINN预测器基础功能正常": "PINN predictor basic functionality normal",
        "测试钢构件强度计算器": "Test steel component strength calculator",
        "检查模型文件": "Check model file",
        "模型文件不存在": "Model file does not exist",
        "跳过此测试": "Skip this test",
        "初始化计算器": "Initialize calculator",
        "计算": "Calculate",
        "钢构件强度计算器功能正常": "Steel component strength calculator functionality normal",
        "计算失败": "Calculation failed",
        "测试Agent": "Test Agent",
        "不调用LLM": "Do not call LLM",
        "测试参数解析": "Test parameter parsing",
        "测试不同的参数格式": "Test different parameter formats",
        "标准参数": "Standard parameters",
        "中文参数": "Chinese parameters",
        "英文全称": "English full names",
        "缺少参数": "Missing parameters",
        "解析成功": "Parsing successful",
        "参数解析测试完成": "Parameter parsing test completed",
        "测试多个钢柱计算": "Test multiple steel column calculations",
        "批量计算": "Batch calculation",
        "多个测试案例": "Multiple test cases",
        "短柱": "Short column",
        "中等柱": "Medium column",
        "长柱": "Long column",
        "预测强度": "Predicted strength",
        "比值": "Ratio",
        "批量计算测试完成": "Batch calculation test completed",
        "运行所有测试": "Run all tests",
        "所有测试完成": "All tests completed",
        "提示": "Tip",
        "要测试完整的LLM对话功能": "To test complete LLM dialogue functionality",
        "请运行": "Please run",
        "测试过程中出现错误": "Error occurred during testing",
        
        # Messages
        "警告": "Warning",
        "错误": "Error",
        "成功": "Success",
        "失败": "Failed",
        "已设置": "Set",
        "未设置": "Not set",
        "已初始化": "Initialized",
        "未初始化": "Not initialized",
        "已加载": "Loaded",
        "未加载": "Not loaded",
        "已完成": "Completed",
        "未完成": "Not completed",
        
        # Config
        "项目配置文件": "Project configuration file",
        "默认配置": "Default configuration",
        "模型参数": "Model parameters",
        "物理常数": "Physical constants",
        "钢的弹性模量": "Steel elastic modulus",
        "对数变换偏移量": "Logarithmic transformation offset",
        "参数范围": "Parameter range",
        "用于验证": "For validation",
        "工具描述": "Tool description",
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for chinese, english in replacements.items():
            content = content.replace(chinese, english)
        
        # Only write if content changed
        if content != original_content:
            if backup:
                backup_path = filepath + '.bak'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main conversion function"""
    print("=" * 70)
    print("Converting all Chinese content to English")
    print("=" * 70)
    print()
    
    # Files to convert
    files_to_convert = [
        "agent/tools/steel_strength_tools.py",
        "agent/config.py",
        "agent/utils/create_scalers.py",
        "agent/__init__.py",
        "agent/models/__init__.py",
        "agent/tools/__init__.py",
        "tests/test_agent.py",
        "tests/test_pinn_model.py",
        "tests/test_steel_tools.py",
        "tests/test_llm_agent.py",
        "tests/test_integration.py",
        "tests/test_conversation_features.py",
        "tests/test_multi_turn_dialogue.py",
        "tests/__init__.py",
        "tests/conftest.py",
        "examples/usage_examples.py",
        "examples/multi_turn_demo.py",
    ]
    
    converted_count = 0
    skipped_count = 0
    error_count = 0
    
    for filepath in files_to_convert:
        if os.path.exists(filepath):
            print(f"Processing: {filepath}...", end=" ")
            if convert_file_to_english(filepath):
                print("✓ Converted")
                converted_count += 1
            else:
                print("- No changes")
                skipped_count += 1
        else:
            print(f"✗ Not found: {filepath}")
            error_count += 1
    
    print()
    print("=" * 70)
    print(f"Conversion Summary:")
    print(f"  Converted: {converted_count} files")
    print(f"  Skipped:   {skipped_count} files")
    print(f"  Errors:    {error_count} files")
    print("=" * 70)
    print()
    print("Note: Backup files (.bak) have been created for modified files")
    print()

if __name__ == "__main__":
    main()

