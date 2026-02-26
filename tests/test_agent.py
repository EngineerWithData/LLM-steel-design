"""
测试脚本 - 验证Agent功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent
from agent.tools import SteelStrengthCalculator
import json


def test_pinn_predictor():
    """测试PINN模型预测器"""
    print("=" * 60)
    print("测试1: PINN模型预测器")
    print("=" * 60)
    
    from agent.models import PINNPredictor
    
    # 初始化预测器（不加载模型，仅测试Perry-Robertson公式）
    predictor = PINNPredictor()
    
    # 测试数据
    test_input = {
        'A': 10.0,      # 截面积 (in²)
        'I': 100.0,     # 惯性矩 (in⁴)
        'c': 5.0,       # 截面中心到边缘距离 (in)
        'L': 120.0,     # 柱长度 (in)
        'fy': 50.0,     # 屈服强度 (ksi)
        'delta_o': 0.1  # 初始缺陷 (in)
    }
    
    print("\n输入参数:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    
    # 计算Perry-Robertson理论值
    Pn_theory = predictor._perry_robertson(
        test_input['A'],
        test_input['I'],
        test_input['c'],
        test_input['L'],
        test_input['fy'],
        test_input['delta_o']
    )
    
    print(f"\nPerry-Robertson理论强度: {Pn_theory:.2f} kip")
    print("✓ PINN预测器基础功能正常\n")


def test_steel_strength_calculator():
    """测试钢构件强度计算器"""
    print("=" * 60)
    print("测试2: 钢构件强度计算器")
    print("=" * 60)
    
    # 检查模型文件
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              "PINN model/normal/model_20250123_165719.pth")
    if not os.path.exists(model_path):
        print(f"⚠ 模型文件不存在: {model_path}")
        print("跳过此测试\n")
        return
    
    # 初始化计算器
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # 测试数据
    test_params = {
        'A': 10.0,
        'I': 100.0,
        'c': 5.0,
        'L': 120.0,
        'fy': 50.0,
        'delta_o': 0.1
    }
    
    print("\n输入参数:")
    for key, value in test_params.items():
        print(f"  {key}: {value}")
    
    # 计算
    result = calculator.calculate_column_strength(test_params)
    
    print("\n计算结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result['success']:
        print("✓ 钢构件强度计算器功能正常\n")
    else:
        print("✗ 计算失败\n")


def test_agent_without_llm():
    """测试Agent（不调用LLM）"""
    print("=" * 60)
    print("测试3: Agent初始化")
    print("=" * 60)
    
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              "PINN model/normal/model_20250123_165719.pth")
    
    # 初始化Agent
    agent = SteelDesignAgent(model_path=model_path if os.path.exists(model_path) else None)
    
    print("\nAgent配置:")
    print(f"  Base URL: {agent.base_url}")
    print(f"  Model: {agent.model_name}")
    print(f"  API Key: {'已设置' if agent.api_key else '未设置'}")
    print(f"  Client: {'已初始化' if agent.client else '未初始化'}")
    
    print("\n✓ Agent初始化完成\n")


def test_parameter_parsing():
    """测试参数解析"""
    print("=" * 60)
    print("测试4: 参数解析")
    print("=" * 60)
    
    calculator = SteelStrengthCalculator()
    
    # 测试不同的参数格式
    test_cases = [
        {
            'name': '标准参数',
            'params': {'A': 10, 'I': 100, 'c': 5, 'L': 120, 'fy': 50, 'delta_o': 0.1}
        },
        {
            'name': '中文参数',
            'params': {'截面积': 10, 'I': 100, 'c': 5, '长度': 120, 'fy': 50, '初始缺陷': 0.1}
        },
        {
            'name': '英文全称',
            'params': {'area': 10, 'inertia': 100, 'c': 5, 'length': 120, 'yield_strength': 50, 'imperfection': 0.1}
        },
        {
            'name': '缺少参数',
            'params': {'A': 10, 'I': 100, 'c': 5}
        }
    ]
    
    for case in test_cases:
        print(f"\n测试: {case['name']}")
        result = calculator._parse_column_params(case['params'])
        if 'error' in result:
            print(f"  ✗ {result['error']}")
        else:
            print(f"  ✓ 解析成功")
            print(f"    {result}")
    
    print("\n✓ 参数解析测试完成\n")


def test_multiple_columns():
    """测试多个钢柱计算"""
    print("=" * 60)
    print("测试5: 批量计算多个钢柱")
    print("=" * 60)
    
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              "PINN model/normal/model_20250123_165719.pth")
    if not os.path.exists(model_path):
        print(f"⚠ 模型文件不存在，跳过此测试\n")
        return
    
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # 多个测试案例
    test_columns = [
        {'name': '短柱', 'A': 15.0, 'I': 150.0, 'c': 6.0, 'L': 100.0, 'fy': 50.0, 'delta_o': 0.1},
        {'name': '中等柱', 'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 150.0, 'fy': 50.0, 'delta_o': 0.1},
        {'name': '长柱', 'A': 8.0, 'I': 80.0, 'c': 4.0, 'L': 200.0, 'fy': 50.0, 'delta_o': 0.1},
    ]
    
    print("\n计算结果:")
    print("-" * 60)
    
    for col in test_columns:
        name = col.pop('name')
        result = calculator.calculate_column_strength(col)
        
        if result['success']:
            print(f"\n{name}:")
            print(f"  长度: {col['L']} in")
            print(f"  预测强度: {result['nominal_strength_Pn']:.2f} kip")
            print(f"  理论强度: {result['theoretical_strength']:.2f} kip")
            print(f"  比值: {result['prediction_ratio']:.3f}")
        else:
            print(f"\n{name}: 计算失败 - {result['error']}")
    
    print("\n✓ 批量计算测试完成\n")


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "钢结构设计Agent - 功能测试" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        test_pinn_predictor()
        test_steel_strength_calculator()
        test_agent_without_llm()
        test_parameter_parsing()
        test_multiple_columns()
        
        print("=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        print("\n提示: 要测试完整的LLM对话功能，请运行: python agent.py")
        print()
        
    except Exception as e:
        print(f"\n✗ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

