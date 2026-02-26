"""
使用示例脚本
演示如何使用Agent进行钢结构设计
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent
from agent.tools import SteelStrengthCalculator


def example_1_direct_calculation():
    """示例1: 直接调用Calculate工具"""
    print("=" * 60)
    print("示例1: 直接调用钢柱强度Calculate工具")
    print("=" * 60)
    
    # Initialize calculator
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # 定义钢柱参数
    column_params = {
        'A': 10.0,      # Cross-sectional area 10 in²
        'I': 100.0,     # Moment of inertia 100 in⁴
        'c': 5.0,       # Distance 5 in
        'L': 120.0,     # Length 120 in (10 ft)
        'fy': 50.0,     # Yield strength 50 ksi
        'delta_o': 0.1  # Initial imperfection 0.1 in
    }
    
    print("\n钢柱参数:")
    print(f"  Cross-sectional area A = {column_params['A']} in²")
    print(f"  Moment of inertia I = {column_params['I']} in⁴")
    print(f"  Distance c = {column_params['c']} in")
    print(f"  Length L = {column_params['L']} in")
    print(f"  Yield strength fy = {column_params['fy']} ksi")
    print(f"  Initial imperfection δ₀ = {column_params['delta_o']} in")
    
    # Calculate强度
    result = calculator.calculate_column_strength(column_params)
    
    if result['success']:
        print("\nCalculation result:")
        print(f"  ✓ Nominal compressive strength Pn = {result['nominal_strength_Pn']:.2f} kip")
        print(f"  ✓ Theoretical strength = {result['theoretical_strength']:.2f} kip")
        print(f"  ✓ 预测/理论Ratio = {result['prediction_ratio']:.3f}")
    else:
        print(f"\n✗ CalculateFailed: {result['error']}")
    
    print()


def example_2_agent_chat():
    """示例2: 使用Agent进行对话"""
    print("=" * 60)
    print("示例2: 使用LLM Agent进行对话式设计")
    print("=" * 60)
    
    # 初始化Agent
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("\n⚠ LLM客户端Not initialized，请检查.env配置")
        print("跳过此示例\n")
        return
    
    # 模拟对话
    conversations = [
        "你好，我需要Calculate一个钢柱的强度",
        "钢柱参数：Cross-sectional area10square inches，Moment of inertia100，c是5inches，Length120inches，Yield strength50ksi，Initial imperfection0.1inches",
    ]
    
    print("\n开始对话:")
    print("-" * 60)
    
    for user_msg in conversations:
        print(f"\n用户: {user_msg}")
        response = agent.chat(user_msg)
        print(f"\nAgent: {response}")
        print("-" * 60)
    
    print()


def example_3_batch_design():
    """示例3: 批量设计多个钢柱"""
    print("=" * 60)
    print("示例3: 批量设计不同规格的钢柱")
    print("=" * 60)
    
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # 定义多个钢柱设计方案
    design_cases = [
        {
            'name': 'W8x31 - 10ft',
            'A': 9.13,
            'I': 110.0,
            'c': 4.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        },
        {
            'name': 'W8x31 - 15ft',
            'A': 9.13,
            'I': 110.0,
            'c': 4.0,
            'L': 180.0,
            'fy': 50.0,
            'delta_o': 0.1
        },
        {
            'name': 'W8x31 - 20ft',
            'A': 9.13,
            'I': 110.0,
            'c': 4.0,
            'L': 240.0,
            'fy': 50.0,
            'delta_o': 0.1
        },
    ]
    
    print("\n设计方案对比:")
    print("-" * 80)
    print(f"{'方案':<20} {'Length(in)':<12} {'Pn(kip)':<12} {'理论(kip)':<12} {'Ratio':<8}")
    print("-" * 80)
    
    for case in design_cases:
        name = case.pop('name')
        result = calculator.calculate_column_strength(case)
        
        if result['success']:
            print(f"{name:<20} {case['L']:<12.1f} "
                  f"{result['nominal_strength_Pn']:<12.2f} "
                  f"{result['theoretical_strength']:<12.2f} "
                  f"{result['prediction_ratio']:<8.3f}")
    
    print("-" * 80)
    print("\n观察: 随着柱Length增加，抗压强度显著降低（细长比效应）\n")


def example_4_parametric_study():
    """示例4: 参数化研究 - Yield strength影响"""
    print("=" * 60)
    print("示例4: 参数化研究 - Yield strength对柱强度的影响")
    print("=" * 60)
    
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # 固定其他参数，改变Yield strength
    base_params = {
        'A': 10.0,
        'I': 100.0,
        'c': 5.0,
        'L': 120.0,
        'delta_o': 0.1
    }
    
    fy_values = [36, 42, 50, 60, 70]  # ksi
    
    print("\n固定参数:")
    print(f"  A = {base_params['A']} in²")
    print(f"  I = {base_params['I']} in⁴")
    print(f"  L = {base_params['L']} in")
    
    print("\nYield strength影响分析:")
    print("-" * 60)
    print(f"{'fy (ksi)':<12} {'Pn (kip)':<15} {'增长率':<12}")
    print("-" * 60)
    
    prev_pn = None
    for fy in fy_values:
        params = base_params.copy()
        params['fy'] = fy
        
        result = calculator.calculate_column_strength(params)
        
        if result['success']:
            pn = result['nominal_strength_Pn']
            growth = f"{((pn - prev_pn) / prev_pn * 100):.1f}%" if prev_pn else "-"
            print(f"{fy:<12} {pn:<15.2f} {growth:<12}")
            prev_pn = pn
    
    print("-" * 60)
    print("\n观察: Yield strength提高可以显著增加柱的抗压强度\n")


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "钢结构设计Agent - 使用示例" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        # Check model file
        model_path = "../PINN model/normal/model_20250123_165719.pth"
        if not os.path.exists(model_path):
            print(f"⚠ Warning: 未找到模型文件 {model_path}")
            print("某些示例可能无法运行\n")
        
        # 运行示例
        example_1_direct_calculation()
        input("按Enter继续下一个示例...")
        
        example_2_agent_chat()
        input("按Enter继续下一个示例...")
        
        example_3_batch_design()
        input("按Enter继续下一个示例...")
        
        example_4_parametric_study()
        
        print("=" * 60)
        print("所有示例演示完成！")
        print("=" * 60)
        print("\n要启动交互式Agent，Please run: python agent.py")
        print()
        
    except KeyboardInterrupt:
        print("\n\n示例演示已中断")
    except Exception as e:
        print(f"\n✗ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

