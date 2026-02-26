"""
PINN模型推理模块
用于加载预训练的PINN模型并进行钢构件强度预测
"""

import torch
import torch.nn as nn
import numpy as np
import pickle
import os
from typing import Dict, Union, Tuple


class PINN(nn.Module):
    """物理信息神经网络模型"""
    
    def __init__(self, in_dim: int, h_dim: int, out_dim: int):
        super(PINN, self).__init__()
        self.fc1 = nn.Linear(in_dim, h_dim)
        self.act1 = nn.LeakyReLU(0.01)
        self.bn1 = nn.BatchNorm1d(h_dim)
        self.dropout1 = nn.Dropout(p=0.2)
        self.fc2 = nn.Linear(h_dim, h_dim)
        self.act2 = nn.LeakyReLU(0.01)
        self.bn2 = nn.BatchNorm1d(h_dim)
        self.dropout2 = nn.Dropout(p=0.2)
        self.fc3 = nn.Linear(h_dim, h_dim)
        self.act3 = nn.LeakyReLU(0.01)
        self.bn3 = nn.BatchNorm1d(h_dim)
        self.dropout3 = nn.Dropout(p=0.2)
        self.fc4 = nn.Linear(h_dim, out_dim)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.act1(x)
        x = self.bn1(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.act2(x)
        x = self.bn2(x)
        x = self.dropout2(x)
        x = self.fc3(x)
        x = self.act3(x)
        x = self.bn3(x)
        x = self.dropout3(x)
        x = self.fc4(x)
        return x


class StandardScaler:
    """标准化缩放器"""
    
    def __init__(self):
        self.mean_ = None
        self.scale_ = None
    
    def fit(self, X):
        self.mean_ = np.mean(X, axis=0)
        self.scale_ = np.std(X, axis=0)
        return self
    
    def transform(self, X):
        return (X - self.mean_) / self.scale_
    
    def inverse_transform(self, X):
        return X * self.scale_ + self.mean_


class PINNPredictor:
    """PINN模型预测器"""
    
    def __init__(self, model_path: str = None, scaler_path: str = None):
        """
        初始化PINN预测器
        
        Args:
            model_path: 预训练模型路径
            scaler_path: 标准化器路径
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler_x = None
        self.scaler_y = None
        self.SHIFT = 0.01  # 对数变换的偏移量
        
        # 特征名称
        self.feature_names = ['A', 'I', 'c', 'L', 'fy', 'delta_o']
        
        if model_path:
            self.load_model(model_path, scaler_path)
    
    def load_model(self, model_path: str, scaler_path: str = None):
        """
        加载预训练模型和标准化器
        
        Args:
            model_path: 模型文件路径
            scaler_path: 标准化器文件路径
        """
        # 加载模型
        self.model = PINN(in_dim=6, h_dim=64, out_dim=1)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        
        # 自动查找标准化器
        if scaler_path is None:
            # 尝试在模型同目录下查找scalers.pkl
            model_dir = os.path.dirname(model_path)
            scaler_path = os.path.join(model_dir, 'scalers.pkl')
        
        # 加载或初始化标准化器
        if scaler_path and os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                scalers = pickle.load(f)
                self.scaler_x = scalers['scaler_x']
                self.scaler_y = scalers['scaler_y']
                if 'SHIFT' in scalers:
                    self.SHIFT = scalers['SHIFT']
            print(f"✓ 标准化器已加载: {scaler_path}")
        else:
            # 如果没有保存的标准化器，使用默认值（需要根据训练数据调整）
            print("警告: 未找到标准化器文件，使用默认参数")
            self.scaler_x = StandardScaler()
            self.scaler_y = StandardScaler()
    
    def predict(self, input_params: Dict[str, float]) -> Dict[str, Union[float, str]]:
        """
        预测钢构件的抗压强度
        
        Args:
            input_params: 输入参数字典，包含:
                - A: 截面积 (in²)
                - I: 惯性矩 (in⁴)
                - c: 截面中心到边缘距离 (in)
                - L: 柱长度 (in)
                - fy: 屈服强度 (ksi)
                - delta_o: 初始缺陷 (in)
        
        Returns:
            预测结果字典，包含:
                - Pn: 预测的抗压强度 (kip)
                - status: 预测状态
                - message: 附加信息
        """
        try:
            # 验证输入参数
            missing_params = [p for p in self.feature_names if p not in input_params]
            if missing_params:
                return {
                    'Pn': None,
                    'status': 'error',
                    'message': f'缺少必要参数: {", ".join(missing_params)}'
                }
            
            # 准备输入数据
            X = np.array([[input_params[f] for f in self.feature_names]])
            
            # 标准化
            if self.scaler_x.mean_ is not None:
                X_scaled = self.scaler_x.transform(X)
            else:
                X_scaled = X
            
            # 转换为张量
            X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)
            
            # 预测
            with torch.no_grad():
                y_pred_scaled = self.model(X_tensor)
            
            # 反标准化
            y_pred_scaled_np = y_pred_scaled.cpu().numpy()
            
            if self.scaler_y.mean_ is not None:
                y_log = self.scaler_y.inverse_transform(y_pred_scaled_np)
            else:
                y_log = y_pred_scaled_np
            
            # 反对数变换
            Pn = np.exp(y_log[0, 0]) - self.SHIFT
            
            # 计算Perry-Robertson理论值作为参考
            Pn_theory = self._perry_robertson(
                input_params['A'],
                input_params['I'],
                input_params['c'],
                input_params['L'],
                input_params['fy'],
                input_params['delta_o']
            )
            
            return {
                'Pn': float(Pn),
                'Pn_theory': float(Pn_theory),
                'ratio': float(Pn / Pn_theory) if Pn_theory > 0 else None,
                'status': 'success',
                'message': '预测成功'
            }
            
        except Exception as e:
            return {
                'Pn': None,
                'status': 'error',
                'message': f'预测失败: {str(e)}'
            }
    
    def _perry_robertson(self, a: float, i: float, c: float, l: float, 
                        fy: float, d: float) -> float:
        """
        Perry-Robertson公式计算理论强度
        
        Args:
            a: 截面积 (in²)
            i: 惯性矩 (in⁴)
            c: 截面中心到边缘距离 (in)
            l: 柱长度 (in)
            fy: 屈服强度 (ksi)
            d: 初始缺陷 (in)
        
        Returns:
            理论抗压强度 (kip)
        """
        import math
        
        e = 29000  # 钢的弹性模量 (ksi)
        py = fy * a
        pcre = (math.pi ** 2) * e * i / (l ** 2)
        se = pcre / a
        sy = fy
        eta = (d * c) / (i / a)
        
        val = 0.5 * (1 + (se / sy) * (eta + 1) - 
                    math.sqrt((1 + (se / sy) * (eta + 1)) ** 2 - 4 * (se / sy))) * py
        
        return val
    
    def batch_predict(self, input_list: list) -> list:
        """
        批量预测
        
        Args:
            input_list: 输入参数列表
        
        Returns:
            预测结果列表
        """
        results = []
        for input_params in input_list:
            result = self.predict(input_params)
            results.append(result)
        return results
    
    def save_scalers(self, scaler_path: str):
        """
        保存标准化器
        
        Args:
            scaler_path: 保存路径
        """
        with open(scaler_path, 'wb') as f:
            pickle.dump({
                'scaler_x': self.scaler_x,
                'scaler_y': self.scaler_y
            }, f)
        print(f"标准化器已保存到: {scaler_path}")


if __name__ == "__main__":
    # 测试代码
    predictor = PINNPredictor()
    
    # 示例输入
    test_input = {
        'A': 10.0,      # 截面积 (in²)
        'I': 100.0,     # 惯性矩 (in⁴)
        'c': 5.0,       # 截面中心到边缘距离 (in)
        'L': 120.0,     # 柱长度 (in)
        'fy': 50.0,     # 屈服强度 (ksi)
        'delta_o': 0.1  # 初始缺陷 (in)
    }
    
    result = predictor.predict(test_input)
    print("预测结果:", result)

