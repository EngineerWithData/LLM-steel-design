"""
测试Steel Component Strength Calculation Tools
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agent.tools import SteelStrengthCalculator


class TestSteelStrengthCalculator:
    """钢构件强度Calculate器测试类"""
    
    @pytest.fixture
    def calculator(self):
        """创建Calculate器实例（Do not load model）"""
        return SteelStrengthCalculator()
    
    @pytest.fixture
    def calculator_with_model(self):
        """创建带模型的Calculate器实例"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if os.path.exists(model_path):
            return SteelStrengthCalculator(model_path=model_path)
        else:
            pytest.skip("Model file does not exist")
    
    def test_parameter_parsing_standard_format(self, calculator):
        """测试标准格式参数解析"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "标准格式应该Parsing successful"
        assert result['A'] == 10.0
        assert result['I'] == 100.0
        assert result['L'] == 120.0
    
    def test_parameter_parsing_chinese_format(self, calculator):
        """测试中文格式参数解析"""
        params = {
            'Cross-sectional area': 10.0,
            'I': 100.0,
            'c': 5.0,
            'Length': 120.0,
            'fy': 50.0,
            'Initial imperfection': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "中文格式应该Parsing successful"
        assert result['A'] == 10.0
        assert result['L'] == 120.0
        assert result['delta_o'] == 0.1
    
    def test_parameter_parsing_english_full_names(self, calculator):
        """测试English full names格式参数解析"""
        params = {
            'area': 10.0,
            'inertia': 100.0,
            'c': 5.0,
            'length': 120.0,
            'yield_strength': 50.0,
            'imperfection': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "English full names格式应该Parsing successful"
        assert result['A'] == 10.0
        assert result['I'] == 100.0
        assert result['fy'] == 50.0
    
    def test_parameter_parsing_missing_params(self, calculator):
        """测试Missing parameters的情况"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0
            # 缺少 L, fy, delta_o
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "Missing parameters应该返回Error"
        assert 'L' in result['error'] or 'Length' in result['error']
    
    def test_parameter_validation_negative_area(self, calculator):
        """测试负数Cross-sectional area验证"""
        params = {
            'A': -10.0,  # 负数
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "负数Cross-sectional area应该返回Error"
    
    def test_parameter_validation_zero_length(self, calculator):
        """测试零Length验证"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 0.0,  # 零Length
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "零Length应该返回Error"
    
    def test_calculate_column_strength_without_model(self, calculator):
        """测试没有模型时的Calculate"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator.calculate_column_strength(params)
        
        assert result['success'] == False, "没有模型时应该返回Failed"
        assert 'error' in result
    
    def test_calculate_column_strength_with_model(self, calculator_with_model):
        """测试使用模型Calculate钢柱强度"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator_with_model.calculate_column_strength(params)
        
        assert result['success'] == True, "Calculate应该Success"
        assert 'nominal_strength_Pn' in result
        assert 'theoretical_strength' in result
        assert 'prediction_ratio' in result
        assert result['component_type'] == 'column'
        assert result['unit'] == 'kip'
    
    def test_calculate_column_strength_different_lengths(self, calculator_with_model):
        """测试不同Length的钢柱Calculate"""
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
        
        # 验证强度随Length增加而减小
        if len(results) == 3:
            assert results[0] > results[1] > results[2], "强度应该随Length增加而减小"
    
    def test_calculate_column_strength_different_yield_strengths(self, calculator_with_model):
        """测试不同Yield strength的钢柱Calculate"""
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
        
        # 验证强度随Yield strength增加而增加
        if len(results) == 3:
            assert results[0] < results[1] < results[2], "强度应该随Yield strength增加而增加"
    
    def test_calculate_beam_strength(self, calculator):
        """测试钢梁强度Calculate（开发中）"""
        params = {'section': 'W12x26'}
        
        result = calculator.calculate_beam_strength(params)
        
        assert result['success'] == False, "钢梁功能应该返回开发中"
        assert '开发中' in result['error']
    
    def test_get_tool_description(self, calculator):
        """测试Get tool description"""
        description = calculator.get_tool_description()
        
        assert isinstance(description, str), "描述应该是字符串"
        assert len(description) > 0, "描述不应该为空"
        assert 'calculate_column_strength' in description
        assert 'A' in description and 'I' in description


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

