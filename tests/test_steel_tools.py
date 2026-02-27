"""
Test steel component strength calculation tools
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agent.tools import SteelStrengthCalculator


class TestSteelStrengthCalculator:
    """Steel component strength calculator test class"""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance (without loading model)"""
        return SteelStrengthCalculator()
    
    @pytest.fixture
    def calculator_with_model(self):
        """Create calculator instance with model"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if os.path.exists(model_path):
            return SteelStrengthCalculator(model_path=model_path)
        else:
            pytest.skip("Model file does not exist")
    
    def test_parameter_parsing_standard_format(self, calculator):
        """Test standard format parameter parsing"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "Standard format should parse successfully"
        assert result['A'] == 10.0
        assert result['I'] == 100.0
        assert result['L'] == 120.0
    
    def test_parameter_parsing_chinese_format(self, calculator):
        """Test Chinese format parameter parsing"""
        params = {
            'cross_sectional_area': 10.0,
            'I': 100.0,
            'c': 5.0,
            'length': 120.0,
            'fy': 50.0,
            'initial_imperfection': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "Chinese format should parse successfully"
        assert result['A'] == 10.0
        assert result['L'] == 120.0
        assert result['delta_o'] == 0.1
    
    def test_parameter_parsing_english_full_names(self, calculator):
        """Test English full names format parameter parsing"""
        params = {
            'area': 10.0,
            'inertia': 100.0,
            'c': 5.0,
            'length': 120.0,
            'yield_strength': 50.0,
            'imperfection': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "English full names format should parse successfully"
        assert result['A'] == 10.0
        assert result['I'] == 100.0
        assert result['fy'] == 50.0
    
    def test_parameter_parsing_missing_params(self, calculator):
        """Test missing parameters case"""
        # Missing L, fy, delta_o
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "Should return error when parameters are missing"
        assert 'L' in result['error'] or 'length' in result['error']
    
    def test_parameter_validation_negative_area(self, calculator):
        """Test negative cross-sectional area validation"""
        params = {
            'A': -10.0,  # Negative
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "Should return error for negative cross-sectional area"
    
    def test_parameter_validation_zero_length(self, calculator):
        """Test zero length validation"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 0.0,  # Zero length
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "Should return error for zero length"
    
    def test_calculate_column_strength_without_model(self, calculator):
        """Test calculation without model"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator.calculate_column_strength(params)
        
        assert result['success'] == False, "Should return failure without model"
        assert 'error' in result
    
    def test_calculate_column_strength_with_model(self, calculator_with_model):
        """Test steel column strength calculation using model"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator_with_model.calculate_column_strength(params)
        
        assert result['success'] == True, "Calculation should succeed"
        assert 'nominal_strength_Pn' in result
        assert 'theoretical_strength' in result
        assert 'prediction_ratio' in result
        assert result['component_type'] == 'column'
        assert result['unit'] == 'kip'
    
    def test_calculate_column_strength_different_lengths(self, calculator_with_model):
        """Test steel column calculation with different lengths"""
        lengths = [100.0, 150.0, 200.0]
        results = []
        
        for L in lengths:
            params = {
                'A': 10.0,
                'I': 100.0,
                'c': 5.0,
                'L': L,
                'fy': 50.0,
                'delta_o': 0.1
            }
            result = calculator_with_model.calculate_column_strength(params)
            if result['success']:
                results.append(result['nominal_strength_Pn'])
        
        # Verify strength decreases with increasing length
        if len(results) == 3:
            assert results[0] > results[1] > results[2], "Strength should decrease with increasing length"
    
    def test_calculate_column_strength_different_yield_strengths(self, calculator_with_model):
        """Test steel column calculation with different yield strengths"""
        fy_values = [36.0, 50.0, 60.0]
        results = []
        
        for fy in fy_values:
            params = {
                'A': 10.0,
                'I': 100.0,
                'c': 5.0,
                'L': 120.0,
                'fy': fy,
                'delta_o': 0.1
            }
            result = calculator_with_model.calculate_column_strength(params)
            if result['success']:
                results.append(result['nominal_strength_Pn'])
        
        # Verify strength increases with increasing yield strength
        if len(results) == 3:
            assert results[0] < results[1] < results[2], "Strength should increase with increasing yield strength"
    
    def test_calculate_beam_strength(self, calculator):
        """Test steel beam strength calculation (under development)"""
        params = {'section': 'W12x26'}
        
        result = calculator.calculate_beam_strength(params)
        
        assert result['success'] == False, "Beam functionality should return under development"
        assert 'development' in result['error'].lower()
    
    def test_get_tool_description(self, calculator):
        """Test get tool description"""
        description = calculator.get_tool_description()
        
        assert isinstance(description, str), "Description should be string"
        assert len(description) > 0, "Description should not be empty"
        assert 'calculate_column_strength' in description
        assert 'A' in description and 'I' in description


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
