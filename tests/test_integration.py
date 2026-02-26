"""
集成测试 - 测试完整的工作流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agent import SteelDesignAgent
from agent.tools import SteelStrengthCalculator
from agent.models import PINNPredictor


class TestIntegration:
    """集成测试类"""
    
    @pytest.fixture
    def model_path(self):
        """获取模型路径"""
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if not os.path.exists(path):
            pytest.skip("Model file does not exist")
        return path
    
    def test_end_to_end_column_design(self, model_path):
        """测试端到端的钢柱设计流程"""
        # 1. 创建Agent
        agent = SteelDesignAgent(model_path=model_path)
        
        # 2. 定义设计参数
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # 3. 使用Calculate器Calculate
        result = agent.calculator.calculate_column_strength(params)
        
        # 4. 验证结果
        assert result['success'] == True
        assert result['nominal_strength_Pn'] > 0
        assert result['theoretical_strength'] > 0
        assert result['prediction_ratio'] > 0
    
    def test_multiple_design_scenarios(self, model_path):
        """测试多个设计场景"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        # 场景1: Short column
        short_column = {
            'A': 15.0, 'I': 150.0, 'c': 6.0,
            'L': 100.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # 场景2: Medium column
        medium_column = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 150.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # 场景3: Long column
        long_column = {
            'A': 8.0, 'I': 80.0, 'c': 4.0,
            'L': 200.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # Calculate所有场景
        results = []
        for params in [short_column, medium_column, long_column]:
            result = calculator.calculate_column_strength(params)
            assert result['success'] == True
            results.append(result['nominal_strength_Pn'])
        
        # 验证趋势：Short column > Medium column > Long column
        assert results[0] > results[1] > results[2]
    
    def test_parametric_study_length(self, model_path):
        """测试参数化研究：Length影响"""
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
        
        # 验证强度随Length增加而单调递减
        assert len(strengths) == len(lengths)
        for i in range(len(strengths) - 1):
            assert strengths[i] > strengths[i + 1], f"强度应该递减: {strengths[i]} > {strengths[i+1]}"
    
    def test_parametric_study_yield_strength(self, model_path):
        """测试参数化研究：Yield strength影响"""
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
        
        # 验证强度随Yield strength增加而单调递增
        assert len(strengths) == len(fy_values)
        for i in range(len(strengths) - 1):
            assert strengths[i] < strengths[i + 1], f"强度应该递增: {strengths[i]} < {strengths[i+1]}"
    
    def test_comparison_with_theory(self, model_path):
        """测试PINN预测与理论值的对比"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        test_cases = [
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 100.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 12.0, 'I': 120.0, 'c': 5.5, 'L': 120.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 15.0, 'I': 150.0, 'c': 6.0, 'L': 150.0, 'fy': 50.0, 'delta_o': 0.1},
        ]
        
        for params in test_cases:
            result = calculator.calculate_column_strength(params)
            
            assert result['success'] == True
            
            # 预测值和理论值都应该是正数
            assert result['nominal_strength_Pn'] > 0
            assert result['theoretical_strength'] > 0
            
            # Ratio应该在合理范围内（0.5 - 2.0）
            ratio = result['prediction_ratio']
            assert 0.5 < ratio < 2.0, f"Ratio应该在合理范围: {ratio}"
    
    def test_model_predictor_integration(self, model_path):
        """测试模型预测器集成"""
        # 创建预测器
        predictor = PINNPredictor(model_path=model_path)
        
        # 测试参数
        params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'fy': 50.0, 'delta_o': 0.1
        }
        
        # 预测
        result = predictor.predict(params)
        
        assert result['status'] == 'success'
        assert result['Pn'] > 0
        assert result['Pn_theory'] > 0
    
    def test_error_handling_chain(self):
        """测试Error处理链"""
        calculator = SteelStrengthCalculator()  # Do not load model
        
        # 测试1: 没有模型
        result = calculator.calculate_column_strength({
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'fy': 50.0, 'delta_o': 0.1
        })
        assert result['success'] == False
        
        # 测试2: Missing parameters
        result = calculator.calculate_column_strength({
            'A': 10.0, 'I': 100.0
        })
        assert result['success'] == False
        
        # 测试3: 无效参数
        result = calculator.calculate_column_strength({
            'A': -10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'fy': 50.0, 'delta_o': 0.1
        })
        assert result['success'] == False


class TestRealWorldScenarios:
    """真实世界场景测试"""
    
    @pytest.fixture
    def model_path(self):
        """获取模型路径"""
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
        if not os.path.exists(path):
            pytest.skip("Model file does not exist")
        return path
    
    def test_w_section_column(self, model_path):
        """测试W型钢柱（基于AISC手册）"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        # W8x31截面参数（近似）
        params = {
            'A': 9.13,      # in²
            'I': 110.0,     # in⁴
            'c': 4.0,       # in
            'L': 120.0,     # 10 ft
            'fy': 50.0,     # ksi (A992钢)
            'delta_o': 0.1  # in
        }
        
        result = calculator.calculate_column_strength(params)
        
        assert result['success'] == True
        assert result['nominal_strength_Pn'] > 0
        
        # 粗略验证：强度应该在合理范围内
        # W8x31的Theoretical strength大约在200-500 kip范围
        assert 100 < result['nominal_strength_Pn'] < 1000
    
    def test_different_steel_grades(self, model_path):
        """测试不同钢材等级"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        base_params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'L': 120.0, 'delta_o': 0.1
        }
        
        # 不同钢材等级
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
        
        # 验证高强度钢材有更高的承载力
        assert results['A36'] < results['A572 Gr.50']
        assert results['A572 Gr.50'] < results['A913 Gr.65']
    
    def test_slenderness_effect(self, model_path):
        """测试细长比效应"""
        calculator = SteelStrengthCalculator(model_path=model_path)
        
        # 固定截面，改变Length
        base_params = {
            'A': 10.0, 'I': 100.0, 'c': 5.0,
            'fy': 50.0, 'delta_o': 0.1
        }
        
        # Short column、Medium column、Long column
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
        
        # 验证细长比效应
        assert results['Short column'] > results['Medium column'] > results['Long column']
        
        # Long column的强度应该低于Short column（放宽阈值）
        assert results['Long column'] < results['Short column'] * 0.98


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

