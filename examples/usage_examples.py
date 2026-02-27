"""
Usage Example Script
Demonstrates how to use Agent for steel structure design
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SteelDesignAgent
from agent.tools import SteelStrengthCalculator


def example_1_direct_calculation():
    """Example 1: Direct call to calculation tool"""
    print("=" * 60)
    print("Example 1: Direct call to steel column strength calculation tool")
    print("=" * 60)
    
    # Initialize calculator
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # Define steel column parameters
    column_params = {
        'A': 10.0,      # Cross-sectional area 10 in²
        'I': 100.0,     # Moment of inertia 100 in⁴
        'c': 5.0,       # Distance 5 in
        'L': 120.0,     # Length 120 in (10 ft)
        'fy': 50.0,     # Yield strength 50 ksi
        'delta_o': 0.1  # Initial imperfection 0.1 in
    }
    
    print("\nSteel column parameters:")
    print(f"  Cross-sectional area A = {column_params['A']} in²")
    print(f"  Moment of inertia I = {column_params['I']} in⁴")
    print(f"  Distance c = {column_params['c']} in")
    print(f"  Length L = {column_params['L']} in")
    print(f"  Yield strength fy = {column_params['fy']} ksi")
    print(f"  Initial imperfection δ₀ = {column_params['delta_o']} in")
    
    # Calculate strength
    result = calculator.calculate_column_strength(column_params)
    
    if result['success']:
        print("\nCalculation result:")
        print(f"  ✓ Nominal compressive strength Pn = {result['nominal_strength_Pn']:.2f} kip")
        print(f"  ✓ Theoretical strength = {result['theoretical_strength']:.2f} kip")
        print(f"  ✓ Prediction/Theory ratio = {result['prediction_ratio']:.3f}")
    else:
        print(f"\n✗ Calculation failed: {result['error']}")
    
    print()


def example_2_agent_chat():
    """Example 2: Using Agent for conversation"""
    print("=" * 60)
    print("Example 2: Using LLM Agent for conversational design")
    print("=" * 60)
    
    # Initialize Agent
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    agent = SteelDesignAgent(model_path=model_path)
    
    if not agent.client:
        print("\n⚠ LLM client not initialized, please check .env configuration")
        print("Skip this example\n")
        return
    
    # Simulate conversation
    conversations = [
        "Hello, I need to calculate the strength of a steel column",
        "Column parameters: cross-sectional area 10 square inches, moment of inertia 100, c is 5 inches, length 120 inches, yield strength 50 ksi, initial imperfection 0.1 inches",
    ]
    
    print("\nStart conversation:")
    print("-" * 60)
    
    for user_msg in conversations:
        print(f"\nUser: {user_msg}")
        response = agent.chat(user_msg)
        print(f"\nAgent: {response}")
        print("-" * 60)
    
    print()


def example_3_batch_design():
    """Example 3: Batch design of multiple steel columns"""
    print("=" * 60)
    print("Example 3: Batch design of steel columns with different specifications")
    print("=" * 60)
    
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # Define multiple steel column design cases
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
    
    print("\nDesign case comparison:")
    print("-" * 80)
    print(f"{'Case':<20} {'Length(in)':<12} {'Pn(kip)':<12} {'Theory(kip)':<12} {'Ratio':<8}")
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
    print("\nObservation: As column length increases, compressive strength decreases significantly (slenderness ratio effect)\n")


def example_4_parametric_study():
    """Example 4: Parametric study - Effect of yield strength"""
    print("=" * 60)
    print("Example 4: Parametric study - Effect of yield strength on column strength")
    print("=" * 60)
    
    model_path = "../PINN model/normal/model_20250123_165719.pth"
    calculator = SteelStrengthCalculator(model_path=model_path)
    
    # Fix other parameters, vary yield strength
    base_params = {
        'A': 10.0,
        'I': 100.0,
        'c': 5.0,
        'L': 120.0,
        'delta_o': 0.1
    }
    
    fy_values = [36, 42, 50, 60, 70]  # ksi
    
    print("\nFixed parameters:")
    print(f"  A = {base_params['A']} in²")
    print(f"  I = {base_params['I']} in⁴")
    print(f"  L = {base_params['L']} in")
    
    print("\nYield strength effect analysis:")
    print("-" * 60)
    print(f"{'fy (ksi)':<12} {'Pn (kip)':<15} {'Growth rate':<12}")
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
    print("\nObservation: Increasing yield strength can significantly increase column compressive strength\n")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "Steel Structure Design Agent - Usage Examples" + " " * 0 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        # Check model file
        model_path = "../PINN model/normal/model_20250123_165719.pth"
        if not os.path.exists(model_path):
            print(f"⚠ Warning: Model file not found {model_path}")
            print("Some examples may not run\n")
        
        # Run examples
        example_1_direct_calculation()
        input("Press Enter to continue to next example...")
        
        example_2_agent_chat()
        input("Press Enter to continue to next example...")
        
        example_3_batch_design()
        input("Press Enter to continue to next example...")
        
        example_4_parametric_study()
        
        print("=" * 60)
        print("All example demonstrations completed!")
        print("=" * 60)
        print("\nTo start interactive Agent, please run: python agent.py")
        print()
        
    except KeyboardInterrupt:
        print("\n\nExample demonstration interrupted")
    except Exception as e:
        print(f"\n✗ Example execution error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
