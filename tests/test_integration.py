"""
Integration tests - Test complete workflows
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agent import SteelDesignAgent
from agent.tools import SteelStrengthCalculator
from agent.models import PINNPredictor


class TestIntegration:
    """Integration test class"""
    
    @pytest.fixture
    def model_path(self):
        """Get model path"""
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if not os.path.exists(path):
            pytest.skip("Model file does not exist")
        return path
    
    def test_end_to_end_column_design(self, model_path):
        """Test end-to-end steel column design workflow"""
        # 1. Create Agent
        agent = SteelDesignAgent(model_path=model_path)
        
        # 2. Define design parameters
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # 3. Calculate using calculator
        result = agent.calculator.calculate_column_strength(params)
        
        # 4. Verify results
        assert result['success'] == True
        assert result['nominal_strength_Pn'] > 0
        assert result['theoretical_strength'] > 0
        assert result['prediction_ratio'] > 0
    
    def test_multiple_design_scenarios(self, model_path):
        """Test multiple design scenarios"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        # Scenario 1: Short column
        short_column = {
            'A': 15.0, 'I': 150.0, 'c': 6.0,
            'L': 100.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # Scenario 2: Medium column
        medium_column = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 150.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # Scenario 3: Long column
        long_column = {
            'A': 8.0, 'I': 80.0, 'c': 4.0,
            'L': 200.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # Calculate all scenarios
        results = []
        for params in [short_column, medium_column, long_column]:
            result = calculator.calculate_column_strength(params)
            assert result['success'] == True
            results.append(result['nominal_strength_Pn'])
        
        # Verify trend: Short column > Medium column > Long column
        assert results[0] > results[1] > results[2]
    
    def test_parametric_study_length(self, model_path):
        """Test parametric study: Length effect"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        base_params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'fy': 50.0, 'delta_o': 0.1
        }
        
        lengths = [80, 100, 120, 150, 180, 200]
        strengths = []
        
        for L in lengths:
            params = base_params.copy()
            params['L'] = float(L)
            result = calculator.calculate_column_strength(params)
            
            if result['success']:
                strengths.append(result['nominal_strength_Pn'])
        
        # Verify strength decreases monotonically with increasing length
        assert len(strengths) == len(lengths)
        for i in range(len(strengths) - 1):
            assert strengths[i] > strengths[i + 1], f"Strength should decrease: {strengths[i]} > {strengths[i+1]}"
    
    def test_parametric_study_yield_strength(self, model_path):
        """Test parametric study: Yield strength effect"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        base_params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'delta_o': 0.1
        }
        
        fy_values = [36, 42, 50, 60, 70]
        strengths = []
        
        for fy in fy_values:
            params = base_params.copy()
            params['fy'] = float(fy)
            result = calculator.calculate_column_strength(params)
            
            if result['success']:
                strengths.append(result['nominal_strength_Pn'])
        
        # Verify strength increases monotonically with increasing yield strength
        assert len(strengths) == len(fy_values)
        for i in range(len(strengths) - 1):
            assert strengths[i] < strengths[i + 1], f"Strength should increase: {strengths[i]} < {strengths[i+1]}"
    
    def test_comparison_with_theory(self, model_path):
        """Test PINN prediction vs theoretical values"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        test_cases = [
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 100.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 12.0, 'I': 120.0, 'c': 5.5, 'L': 120.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 15.0, 'I': 150.0, 'c': 6.0, 'L': 150.0, 'fy': 50.0, 'delta_o': 0.1},
        ]
        
        for params in test_cases:
            result = calculator.calculate_column_strength(params)
            
            assert result['success'] == True
            
            # Predicted and theoretical values should both be positive
            assert result['nominal_strength_Pn'] > 0
            assert result['theoretical_strength'] > 0
            
            # Ratio should be within reasonable range (0.5 - 2.0)
            ratio = result['prediction_ratio']
            assert 0.5 < ratio < 2.0, f"Ratio should be in reasonable range: {ratio}"
    
    def test_model_predictor_integration(self, model_path):
        """Test model predictor integration"""
        # Create predictor
        predictor = PINNPredictor(model_path=model_path)
        
        # Test parameters
        params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # Predict
        result = predictor.predict(params)
        
        assert result['status'] == 'success'
        assert result['Pn'] > 0
        assert result['Pn_theory'] > 0
    
    def test_error_handling_chain(self):
        """Test error handling chain"""
        calculator = SteelStrengthCalculator()  # Without loading model
        
        # Test 1: No model
        result = calculator.calculate_column_strength({
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'fy': 50.0, 'delta_o': 0.1
        })
        assert result['success'] == False
        
        # Test 2: Missing parameters
        result = calculator.calculate_column_strength({
            'A': 10.0, 'I': 100.0
        })
        assert result['success'] == False
        
        # Test 3: Invalid parameters
        result = calculator.calculate_column_strength({
            'A': -10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'fy': 50.0, 'delta_o': 0.1
        })
        assert result['success'] == False


class TestRealWorldScenarios:
    """Real world scenario tests"""
    
    @pytest.fixture
    def model_path(self):
        """Get model path"""
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if not os.path.exists(path):
            pytest.skip("Model file does not exist")
        return path
    
    def test_w_section_column(self, model_path):
        """Test W-section column (based on AISC manual)"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        # W8x31 section parameters (approximate)
        params = {
            'A': 9.13,      # in²
            'I': 110.0,     # in⁴
            'c': 4.0,       # in
            'L': 120.0,     # 10 ft
            'fy': 50.0,     # ksi (A992 steel)
            'delta_o': 0.1  # in
        }
        
        result = calculator.calculate_column_strength(params)
        
        assert result['success'] == True
        assert result['nominal_strength_Pn'] > 0
        
        # Rough verification: strength should be in reasonable range
        # W8x31 theoretical strength approximately in 200-500 kip range
        assert 100 < result['nominal_strength_Pn'] < 1000
    
    def test_different_steel_grades(self, model_path):
        """Test different steel grades"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        base_params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'delta_o': 0.1
        }
        
        # Different steel grades
        steel_grades = {
            'A36': 36.0,
            'A572 Gr.50': 50.0,
            'A992': 50.0,
            'A913 Gr.65': 65.0
        }
        
        results = {}
        for grade, fy in steel_grades.items():
            params = base_params.copy()
            params['fy'] = fy
            result = calculator.calculate_column_strength(params)
            
            if result['success']:
                results[grade] = result['nominal_strength_Pn']
        
        # Verify higher strength steel has higher capacity
        assert results['A36'] < results['A572 Gr.50']
        assert results['A572 Gr.50'] < results['A913 Gr.65']
    
    def test_slenderness_effect(self, model_path):
        """Test slenderness ratio effect"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        # Fixed section, vary length
        base_params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'fy': 50.0, 'delta_o': 0.1
        }
        
        # Short column, Medium column, Long column
        lengths = {
            'Short column': 60.0,
            'Medium column': 120.0,
            'Long column': 240.0
        }
        
        results = {}
        for name, L in lengths.items():
            params = base_params.copy()
            params['L'] = L
            result = calculator.calculate_column_strength(params)
            
            if result['success']:
                results[name] = result['nominal_strength_Pn']
        
        # Verify slenderness effect
        assert results['Short column'] > results['Medium column'] > results['Long column']
        
        # Long column strength should be less than short column (relaxed threshold)
        assert results['Long column'] < results['Short column'] * 0.98


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
