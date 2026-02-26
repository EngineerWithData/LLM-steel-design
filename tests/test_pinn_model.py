"""
测试PINN模型推理功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from agent.models import PINNPredictor


class TestPINNPredictor:
    """PINN预测器测试类"""
    
    @pytest.fixture
    def predictor(self):
        """创建预测器实例"""
        return PINNPredictor()
    
    @pytest.fixture
    def model_path(self):
        """获取模型路径"""
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
    
    def test_perry_robertson_formula(self, predictor):
        """测试Perry-Robertson公式计算"""
        # 测试数据
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # 计算理论强度
        Pn = predictor._perry_robertson(
            params['A'], params['I'], params['c'],
            params['L'], params['fy'], params['delta_o']
        )
        
        # 验证结果
        assert Pn > 0, "Perry-Robertson强度应该大于0"
        assert Pn < params['A'] * params['fy'], "强度不应超过截面屈服强度"
        assert isinstance(Pn, float), "返回值应该是浮点数"
    
    def test_perry_robertson_edge_cases(self, predictor):
        """测试Perry-Robertson公式的边界情况"""
        # 测试短柱（高强度）
        Pn_short = predictor._perry_robertson(10.0, 100.0, 5.0, 50.0, 50.0, 0.1)
        
        # 测试长柱（低强度）
        Pn_long = predictor._perry_robertson(10.0, 100.0, 5.0, 300.0, 50.0, 0.1)
        
        # 长柱强度应该小于短柱
        assert Pn_long < Pn_short, "长柱强度应该小于短柱"
    
    def test_model_loading(self, predictor, model_path):
        """测试模型加载"""
        if not os.path.exists(model_path):
            pytest.skip("模型文件不存在")
        
        # 加载模型
        predictor.load_model(model_path)
        
        # 验证模型已加载
        assert predictor.model is not None, "模型应该已加载"
        assert predictor.scaler_x is not None, "X标准化器应该已加载"
        assert predictor.scaler_y is not None, "Y标准化器应该已加载"
    
    def test_prediction_with_model(self, predictor, model_path):
        """测试使用模型进行预测"""
        if not os.path.exists(model_path):
            pytest.skip("模型文件不存在")
        
        # 加载模型
        predictor.load_model(model_path)
        
        # 测试数据
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # 预测
        result = predictor.predict(params)
        
        # 验证结果
        assert result['status'] == 'success', "预测应该成功"
        assert 'Pn' in result, "结果应该包含Pn"
        assert result['Pn'] > 0, "预测强度应该大于0"
        assert 'Pn_theory' in result, "结果应该包含理论值"
        assert 'ratio' in result, "结果应该包含比值"
    
    def test_prediction_without_model(self, predictor):
        """测试没有加载模型时的预测"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = predictor.predict(params)
        
        # 没有模型时应该返回错误
        assert result['status'] == 'error', "没有模型时应该返回错误"
    
    def test_missing_parameters(self, predictor):
        """测试缺少参数的情况"""
        # 缺少delta_o参数
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0
        }
        
        result = predictor.predict(params)
        
        # 应该返回错误
        assert result['status'] == 'error', "缺少参数时应该返回错误"
        assert 'message' in result, "错误信息应该包含message"
    
    def test_invalid_parameters(self, predictor, model_path):
        """测试无效参数"""
        if not os.path.exists(model_path):
            pytest.skip("模型文件不存在")
        
        predictor.load_model(model_path)
        
        # 负数参数
        params = {
            'A': -10.0,  # 负数
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # 预测应该仍然执行（参数验证在工具层）
        result = predictor.predict(params)
        assert 'Pn' in result or result['status'] == 'error'
    
    def test_batch_prediction(self, predictor, model_path):
        """测试批量预测"""
        if not os.path.exists(model_path):
            pytest.skip("模型文件不存在")
        
        predictor.load_model(model_path)
        
        # 多个测试案例
        test_cases = [
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 100.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 150.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 200.0, 'fy': 50.0, 'delta_o': 0.1},
        ]
        
        # 批量预测
        results = predictor.batch_predict(test_cases)
        
        # 验证结果
        assert len(results) == len(test_cases), "结果数量应该与输入相同"
        
        # 验证强度随长度增加而减小
        strengths = [r['Pn'] for r in results if r['status'] == 'success']
        if len(strengths) == 3:
            assert strengths[0] > strengths[1] > strengths[2], "强度应该随长度增加而减小"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

