"""
钢构件强度计算工具
为LLM Agent提供的工具函数
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pinn_predictor import PINNPredictor
from typing import Dict, Any, List
import json


class SteelStrengthCalculator:
    """钢构件强度计算器工具类"""
    
    def __init__(self, model_path: str = None):
        """
        初始化计算器
        
        Args:
            model_path: PINN模型路径
        """
        self.predictor = PINNPredictor(model_path=model_path)
        self.model_loaded = model_path is not None
    
    def calculate_column_strength(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算钢柱抗压强度
        
        Args:
            params: 钢柱参数字典
        
        Returns:
            计算结果
        """
        if not self.model_loaded:
            return {
                'success': False,
                'error': '模型未加载，请先加载PINN模型'
            }
        
        # 参数映射和单位转换
        input_params = self._parse_column_params(params)
        
        if 'error' in input_params:
            return {
                'success': False,
                'error': input_params['error']
            }
        
        # 调用PINN模型预测
        result = self.predictor.predict(input_params)
        
        if result['status'] == 'success':
            return {
                'success': True,
                'component_type': 'column',
                'nominal_strength_Pn': result['Pn'],
                'theoretical_strength': result['Pn_theory'],
                'prediction_ratio': result['ratio'],
                'unit': 'kip',
                'input_parameters': input_params,
                'message': '钢柱强度计算成功'
            }
        else:
            return {
                'success': False,
                'error': result['message']
            }
    
    def calculate_beam_strength(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算钢梁抗弯强度（预留接口）
        
        Args:
            params: 钢梁参数字典
        
        Returns:
            计算结果
        """
        return {
            'success': False,
            'error': '钢梁强度计算功能正在开发中，敬请期待'
        }
    
    def _parse_column_params(self, params: Dict[str, Any]) -> Dict[str, float]:
        """
        解析和验证钢柱参数
        
        Args:
            params: 原始参数字典
        
        Returns:
            标准化的参数字典
        """
        try:
            # 必需参数
            required_params = {
                'A': ['A', 'area', '截面积', 'cross_sectional_area'],
                'I': ['I', 'inertia', '惯性矩', 'moment_of_inertia'],
                'c': ['c', 'distance', '距离', 'distance_to_edge'],
                'L': ['L', 'length', '长度', 'column_length'],
                'fy': ['fy', 'yield_strength', '屈服强度', 'yield_stress'],
                'delta_o': ['delta_o', 'delta', 'imperfection', '初始缺陷', 'initial_imperfection']
            }
            
            parsed = {}
            
            for standard_key, possible_keys in required_params.items():
                value = None
                for key in possible_keys:
                    if key in params:
                        value = float(params[key])
                        break
                
                if value is None:
                    return {'error': f'缺少必要参数: {standard_key} (可用键名: {", ".join(possible_keys)})'}
                
                parsed[standard_key] = value
            
            # 参数验证
            if parsed['A'] <= 0:
                return {'error': '截面积必须大于0'}
            if parsed['I'] <= 0:
                return {'error': '惯性矩必须大于0'}
            if parsed['L'] <= 0:
                return {'error': '柱长度必须大于0'}
            if parsed['fy'] <= 0:
                return {'error': '屈服强度必须大于0'}
            
            return parsed
            
        except ValueError as e:
            return {'error': f'参数类型错误: {str(e)}'}
        except Exception as e:
            return {'error': f'参数解析失败: {str(e)}'}
    
    def get_tool_description(self) -> str:
        """获取工具描述（供LLM理解）"""
        return """
钢构件强度计算工具

功能:
1. 计算钢柱抗压强度 (calculate_column_strength)
2. 计算钢梁抗弯强度 (calculate_beam_strength) - 开发中

钢柱参数说明:
- A (area): 截面积，单位 in²
- I (inertia): 惯性矩，单位 in⁴
- c (distance): 截面中心到边缘距离，单位 in
- L (length): 柱长度，单位 in
- fy (yield_strength): 屈服强度，单位 ksi
- delta_o (imperfection): 初始缺陷，单位 in

返回结果:
- nominal_strength_Pn: 名义抗压强度，单位 kip
- theoretical_strength: 理论强度（Perry-Robertson公式），单位 kip
- prediction_ratio: 预测值与理论值的比值

示例调用:
{
    "A": 10.0,
    "I": 100.0,
    "c": 5.0,
    "L": 120.0,
    "fy": 50.0,
    "delta_o": 0.1
}
"""


# 为LangChain/OpenAI Function Calling定义工具
STEEL_STRENGTH_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_column_strength",
            "description": "计算钢柱的抗压强度。使用预训练的PINN（物理信息神经网络）模型进行预测。",
            "parameters": {
                "type": "object",
                "properties": {
                    "A": {
                        "type": "number",
                        "description": "截面积，单位: in²（平方英寸）"
                    },
                    "I": {
                        "type": "number",
                        "description": "惯性矩，单位: in⁴（四次方英寸）"
                    },
                    "c": {
                        "type": "number",
                        "description": "截面中心到边缘的距离，单位: in（英寸）"
                    },
                    "L": {
                        "type": "number",
                        "description": "柱长度，单位: in（英寸）"
                    },
                    "fy": {
                        "type": "number",
                        "description": "屈服强度，单位: ksi（千磅每平方英寸）"
                    },
                    "delta_o": {
                        "type": "number",
                        "description": "初始缺陷，单位: in（英寸）"
                    }
                },
                "required": ["A", "I", "c", "L", "fy", "delta_o"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_beam_strength",
            "description": "计算钢梁的抗弯强度（功能开发中）",
            "parameters": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "description": "截面类型"
                    }
                },
                "required": ["section"]
            }
        }
    }
]


if __name__ == "__main__":
    # 测试工具
    calculator = SteelStrengthCalculator()
    
    # 测试钢柱计算
    test_params = {
        'A': 10.0,
        'I': 100.0,
        'c': 5.0,
        'L': 120.0,
        'fy': 50.0,
        'delta_o': 0.1
    }
    
    result = calculator.calculate_column_strength(test_params)
    print("钢柱强度计算结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

