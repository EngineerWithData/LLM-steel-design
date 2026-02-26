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
    """示例1: 直接调用计算工具"""
    print("=" * 60)
    print("示例1: 直接调用钢柱强度计算工具")
    print("=" * 60)
    
    # 初始化计算器
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # 定义钢柱参数
    column_params = {
        'A': 10.0,      # 截面积 10 in²
        'I': 100.0,     # 惯性矩 100 in⁴
        'c': 5.0,       # 距离 5 in
        'L': 120.0,     # 长度 120 in (10 ft)
        'fy': 50.0,     # 屈服强度 50 ksi
        'delta_o': 0.1  # 初始缺陷 0.1 in
    }
    
    print("\n钢柱参数:")
    print(f"  截面积 A = {column_params['A']} in²")
    print(f"  惯性矩 I = {column_params['I']} in⁴")
    print(f"  距离 c = {column_params['c']} in")
    print(f"  长度 L = {column_params['L']} in")
    print(f"  屈服强度 fy = {column_params['fy']} ksi")
    print(f"  初始缺陷 δ₀ = {column_params['delta_o']} in")
    
    # 计算强度
    result = calculator.calculate_column_strength(column_params)
    
    if result['success']:
        print("\n计算结果:")
        print(f"  ✓ 名义抗压强度 Pn = {result['nominal_strength_Pn']:.2f} kip")
        print(f"  ✓ 理论强度 = {result['theoretical_strength']:.2f} kip")
        print(f"  ✓ 预测/理论比值 = {result['prediction_ratio']:.3f}")
    else:
        print(f"\n✗ 计算失败: {result['error']}")
    
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
        print("\n⚠ LLM客户端未初始化，请检查.env配置")
        print("跳过此示例\n")
        return
    
    # 模拟对话
    conversations = [
        "你好，我需要计算一个钢柱的强度",
        "钢柱参数：截面积10平方英寸，惯性矩100，c是5英寸，长度120英寸，屈服强度50ksi，初始缺陷0.1英寸",
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
    print(f"{'方案':<20} {'长度(in)':<12} {'Pn(kip)':<12} {'理论(kip)':<12} {'比值':<8}")
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
    print("\n观察: 随着柱长度增加，抗压强度显著降低（细长比效应）\n")


def example_4_parametric_study():
    """示例4: 参数化研究 - 屈服强度影响"""
    print("=" * 60)
    print("示例4: 参数化研究 - 屈服强度对柱强度的影响")
    print("=" * 60)
    
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # 固定其他参数，改变屈服强度
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
    
    print("\n屈服强度影响分析:")
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
    print("\n观察: 屈服强度提高可以显著增加柱的抗压强度\n")


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "钢结构设计Agent - 使用示例" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        # 检查模型文件
        model_path = "../PINN model/normal/model_20250123_165719.pth"
        if not os.path.exists(model_path):
            print(f"⚠ 警告: 未找到模型文件 {model_path}")
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
        print("\n要启动交互式Agent，请运行: python agent.py")
        print()
        
    except KeyboardInterrupt:
        print("\n\n示例演示已中断")
    except Exception as e:
        print(f"\n✗ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

