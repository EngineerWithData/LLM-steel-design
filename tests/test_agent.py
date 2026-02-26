"""
Test script - Verify Agent functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent
from agent.tools import SteelStrengthCalculator
import json


def test_pinn_predictor():
    """Test PINN model predictor"""
    print("=" * 60)
    print("测试1: PINN模型预测器")
    print("=" * 60)
    
    from agent.models import PINNPredictor
    
    # Initialize predictor（Do not load model，Only test Perry-Robertson formula）
    predictor = PINNPredictor()
    
    # Test data
    test_input = {
        'A': 10.0,      # Cross-sectional area (in²)
        'I': 100.0,     # Moment of inertia (in⁴)
        'c': 5.0,       # 截面中心到边缘Distance (in)
        'L': 120.0,     # 柱Length (in)
        'fy': 50.0,     # Yield strength (ksi)
        'delta_o': 0.1  # Initial imperfection (in)
    }
    
    print("\nInput parameters:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    
    # CalculatePerry-Robertson理论值
    Pn_theory = predictor._perry_robertson(
        test_input['A'],
        test_input['I'],
        test_input['c'],
        test_input['L'],
        test_input['fy'],
        test_input['delta_o']
    )
    
    print(f"\nPerry-RobertsonTheoretical strength: {Pn_theory:.2f} kip")
    print("✓ PINN predictor basic functionality normal\n")


def test_steel_strength_calculator():
    """Test steel component strength calculator"""
    print("=" * 60)
    print("测试2: 钢构件强度Calculate器")
    print("=" * 60)
    
    # Check model file
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              "PINN model/normal/model_20250123_165719.pth")
    if not os.path.exists(model_path):
        print(f"⚠ Model file does not exist: {model_path}")
        print("Skip this test\n")
        return
    
    # Initialize calculator
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # Test data
    test_params = {
        'A': 10.0,
        'I': 100.0,
        'c': 5.0,
        'L': 120.0,
        'fy': 50.0,
        'delta_o': 0.1
    }
    
    print("\nInput parameters:")
    for key, value in test_params.items():
        print(f"  {key}: {value}")
    
    # Calculate
    result = calculator.calculate_column_strength(test_params)
    
    print("\nCalculation result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result['success']:
        print("✓ 钢构件强度Calculate器功能正常\n")
    else:
        print("✗ CalculateFailed\n")


def test_agent_without_llm():
    """Test Agent（Do not call LLM）"""
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
    print(f"  API Key: {'Set' if agent.api_key else 'Not set'}")
    print(f"  Client: {'Initialized' if agent.client else 'Not initialized'}")
    
    print("\n✓ Agent初始化完成\n")


def test_parameter_parsing():
    """Test parameter parsing"""
    print("=" * 60)
    print("测试4: 参数解析")
    print("=" * 60)
    
    calculator = SteelStrengthCalculator()
    
    # Test different parameter formats
    test_cases = [
        {
            'name': 'Standard parameters',
            'params': {'A': 10, 'I': 100, 'c': 5, 'L': 120, 'fy': 50, 'delta_o': 0.1}
        },
        {
            'name': 'Chinese parameters',
            'params': {'Cross-sectional area': 10, 'I': 100, 'c': 5, 'Length': 120, 'fy': 50, 'Initial imperfection': 0.1}
        },
        {
            'name': 'English full names',
            'params': {'area': 10, 'inertia': 100, 'c': 5, 'length': 120, 'yield_strength': 50, 'imperfection': 0.1}
        },
        {
            'name': 'Missing parameters',
            'params': {'A': 10, 'I': 100, 'c': 5}
        }
    ]
    
    for case in test_cases:
        print(f"\n测试: {case['name']}")
        result = calculator._parse_column_params(case['params'])
        if 'error' in result:
            print(f"  ✗ {result['error']}")
        else:
            print(f"  ✓ Parsing successful")
            print(f"    {result}")
    
    print("\n✓ Parameter parsing test completed\n")


def test_multiple_columns():
    """测试多个钢柱Calculate"""
    print("=" * 60)
    print("测试5: 批量Calculate多个钢柱")
    print("=" * 60)
    
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              "PINN model/normal/model_20250123_165719.pth")
    if not os.path.exists(model_path):
        print(f"⚠ Model file does not exist，Skip this test\n")
        return
    
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # Multiple test cases
    test_columns = [
        {'name': 'Short column', 'A': 15.0, 'I': 150.0, 'c': 6.0, 'L': 100.0, 'fy': 50.0, 'delta_o': 0.1},
        {'name': 'Medium column', 'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 150.0, 'fy': 50.0, 'delta_o': 0.1},
        {'name': 'Long column', 'A': 8.0, 'I': 80.0, 'c': 4.0, 'L': 200.0, 'fy': 50.0, 'delta_o': 0.1},
    ]
    
    print("\nCalculation result:")
    print("-" * 60)
    
    for col in test_columns:
        name = col.pop('name')
        result = calculator.calculate_column_strength(col)
        
        if result['success']:
            print(f"\n{name}:")
            print(f"  Length: {col['L']} in")
            print(f"  Predicted strength: {result['nominal_strength_Pn']:.2f} kip")
            print(f"  Theoretical strength: {result['theoretical_strength']:.2f} kip")
            print(f"  Ratio: {result['prediction_ratio']:.3f}")
        else:
            print(f"\n{name}: CalculateFailed - {result['error']}")
    
    print("\n✓ 批量Calculate测试完成\n")


def main():
    """Run all tests"""
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
        print("All tests completed！")
        print("=" * 60)
        print("\nTip: To test complete LLM dialogue functionality，Please run: python agent.py")
        print()
        
    except Exception as e:
        print(f"\n✗ Error occurred during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

