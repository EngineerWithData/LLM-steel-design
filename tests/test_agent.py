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
    print("Test 1: PINN Model Predictor")
    print("=" * 60)
    
    from agent.models import PINNPredictor
    
    # Initialize predictor (without loading model, only test Perry-Robertson formula)
    predictor = PINNPredictor()
    
    # Test data
    test_input = {
        'A': 10.0,      # Cross-sectional area (in²)
        'I': 100.0,     # Moment of inertia (in⁴)
        'c': 5.0,       # Distance from center to edge (in)
        'L': 120.0,     # Column length (in)
        'fy': 50.0,     # Yield strength (ksi)
        'delta_o': 0.1  # Initial imperfection (in)
    }
    
    print("\nInput parameters:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    
    # Calculate Perry-Robertson theoretical value
    Pn_theory = predictor._perry_robertson(
        test_input['A'],
        test_input['I'],
        test_input['c'],
        test_input['L'],
        test_input['fy'],
        test_input['delta_o']
    )
    
    print(f"\nPerry-Robertson theoretical strength: {Pn_theory:.2f} kip")
    print("✓ PINN predictor basic functionality normal\n")


def test_steel_strength_calculator():
    """Test steel component strength calculator"""
    print("=" * 60)
    print("Test 2: Steel Component Strength Calculator")
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
        print("✓ Steel component strength calculator functionality normal\n")
    else:
        print("✗ Calculation failed\n")


def test_agent_without_llm():
    """Test Agent (without calling LLM)"""
    print("=" * 60)
    print("Test 3: Agent Initialization")
    print("=" * 60)
    
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              "PINN model/normal/model_20250123_165719.pth")
    
    # Initialize Agent
    agent = SteelDesignAgent(model_path=model_path if os.path.exists(model_path) else None)
    
    print("\nAgent configuration:")
    print(f"  Base URL: {agent.base_url}")
    print(f"  Model: {agent.model_name}")
    print(f"  API Key: {'Set' if agent.api_key else 'Not set'}")
    print(f"  Client: {'Initialized' if agent.client else 'Not initialized'}")
    
    print("\n✓ Agent initialization completed\n")


def test_parameter_parsing():
    """Test parameter parsing"""
    print("=" * 60)
    print("Test 4: Parameter Parsing")
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
            'params': {'cross_sectional_area': 10, 'I': 100, 'c': 5, 'length': 120, 'fy': 50, 'initial_imperfection': 0.1}
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
        print(f"\nTest: {case['name']}")
        result = calculator._parse_column_params(case['params'])
        if 'error' in result:
            print(f"  ✗ {result['error']}")
        else:
            print(f"  ✓ Parsing successful")
            print(f"    {result}")
    
    print("\n✓ Parameter parsing test completed\n")


def test_multiple_columns():
    """Test batch calculation of multiple steel columns"""
    print("=" * 60)
    print("Test 5: Batch Calculate Multiple Steel Columns")
    print("=" * 60)
    
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                              "PINN model/normal/model_20250123_165719.pth")
    if not os.path.exists(model_path):
        print(f"⚠ Model file does not exist, skip this test\n")
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
            print(f"\n{name}: Calculation failed - {result['error']}")
    
    print("\n✓ Batch calculation test completed\n")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Steel Structure Design Agent - Functionality Test" + " " * 0 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        test_pinn_predictor()
        test_steel_strength_calculator()
        test_agent_without_llm()
        test_parameter_parsing()
        test_multiple_columns()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
        print("\nTip: To test complete LLM dialogue functionality, please run: python agent.py")
        print()
        
    except Exception as e:
        print(f"\n✗ Error occurred during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

