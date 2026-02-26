"""
测试钢构件强度计算工具
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agent.tools import SteelStrengthCalculator


class TestSteelStrengthCalculator:
    """钢构件强度计算器测试类"""
    
    @pytest.fixture
    def calculator(self):
        """创建计算器实例（不加载模型）"""
        return SteelStrengthCalculator()
    
    @pytest.fixture
    def calculator_with_model(self):
        """创建带模型的计算器实例"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if os.path.exists(model_path):
            return SteelStrengthCalculator(model_path=model_path)
        else:
            pytest.skip("模型文件不存在")
    
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
        
        assert 'error' not in result, "标准格式应该解析成功"
        assert result['A'] == 10.0
        assert result['I'] == 100.0
        assert result['L'] == 120.0
    
    def test_parameter_parsing_chinese_format(self, calculator):
        """测试中文格式参数解析"""
        params = {
            '截面积': 10.0,
            'I': 100.0,
            'c': 5.0,
            '长度': 120.0,
            'fy': 50.0,
            '初始缺陷': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "中文格式应该解析成功"
        assert result['A'] == 10.0
        assert result['L'] == 120.0
        assert result['delta_o'] == 0.1
    
    def test_parameter_parsing_english_full_names(self, calculator):
        """测试英文全称格式参数解析"""
        params = {
            'area': 10.0,
            'inertia': 100.0,
            'c': 5.0,
            'length': 120.0,
            'yield_strength': 50.0,
            'imperfection': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' not in result, "英文全称格式应该解析成功"
        assert result['A'] == 10.0
        assert result['I'] == 100.0
        assert result['fy'] == 50.0
    
    def test_parameter_parsing_missing_params(self, calculator):
        """测试缺少参数的情况"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0
            # 缺少 L, fy, delta_o
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "缺少参数应该返回错误"
        assert 'L' in result['error'] or '长度' in result['error']
    
    def test_parameter_validation_negative_area(self, calculator):
        """测试负数截面积验证"""
        params = {
            'A': -10.0,  # 负数
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "负数截面积应该返回错误"
    
    def test_parameter_validation_zero_length(self, calculator):
        """测试零长度验证"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 0.0,  # 零长度
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator._parse_column_params(params)
        
        assert 'error' in result, "零长度应该返回错误"
    
    def test_calculate_column_strength_without_model(self, calculator):
        """测试没有模型时的计算"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator.calculate_column_strength(params)
        
        assert result['success'] == False, "没有模型时应该返回失败"
        assert 'error' in result
    
    def test_calculate_column_strength_with_model(self, calculator_with_model):
        """测试使用模型计算钢柱强度"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = calculator_with_model.calculate_column_strength(params)
        
        assert result['success'] == True, "计算应该成功"
        assert 'nominal_strength_Pn' in result
        assert 'theoretical_strength' in result
        assert 'prediction_ratio' in result
        assert result['component_type'] == 'column'
        assert result['unit'] == 'kip'
    
    def test_calculate_column_strength_different_lengths(self, calculator_with_model):
        """测试不同长度的钢柱计算"""
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
        
        # 验证强度随长度增加而减小
        if len(results) == 3:
            assert results[0] > results[1] > results[2], "强度应该随长度增加而减小"
    
    def test_calculate_column_strength_different_yield_strengths(self, calculator_with_model):
        """测试不同屈服强度的钢柱计算"""
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
        
        # 验证强度随屈服强度增加而增加
        if len(results) == 3:
            assert results[0] < results[1] < results[2], "强度应该随屈服强度增加而增加"
    
    def test_calculate_beam_strength(self, calculator):
        """测试钢梁强度计算（开发中）"""
        params = {'section': 'W12x26'}
        
        result = calculator.calculate_beam_strength(params)
        
        assert result['success'] == False, "钢梁功能应该返回开发中"
        assert '开发中' in result['error']
    
    def test_get_tool_description(self, calculator):
        """测试获取工具描述"""
        description = calculator.get_tool_description()
        
        assert isinstance(description, str), "描述应该是字符串"
        assert len(description) > 0, "描述不应该为空"
        assert 'calculate_column_strength' in description
        assert 'A' in description and 'I' in description


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

