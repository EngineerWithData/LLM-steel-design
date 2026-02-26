"""
创建标准化器
从训练数据中生成标准化器并保存
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler


def create_scalers_from_data(data_path: str, output_path: str):
    """
    从训练数据创建标准化器
    
    Args:
        data_path: 训练数据CSV路径
        output_path: 标准化器保存路径
    """
    # 读取数据
    print(f"读取数据: {data_path}")
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    # 特征和目标
    features = ['A', 'I', 'c', 'L', 'fy', 'delta_o']
    target = 'Pn'
    
    X = df[features].to_numpy()
    y = df[target].to_numpy()
    
    # 添加噪声（与训练时一致）
    noise = np.random.normal(0, 1, y.shape)
    y = y + noise
    
    # 对数变换
    SHIFT = 0.01
    y_log = np.log(y + SHIFT)
    
    # 创建标准化器
    print("创建标准化器...")
    scaler_x = StandardScaler()
    scaler_x.fit(X)
    
    scaler_y = StandardScaler()
    scaler_y.fit(y_log.reshape(-1, 1))
    
    # 保存标准化器
    print(f"保存标准化器到: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump({
            'scaler_x': scaler_x,
            'scaler_y': scaler_y,
            'SHIFT': SHIFT
        }, f)
    
    print("✓ 标准化器创建成功")
    print(f"\nX标准化参数:")
    print(f"  均值: {scaler_x.mean_}")
    print(f"  标准差: {scaler_x.scale_}")
    print(f"\nY标准化参数:")
    print(f"  均值: {scaler_y.mean_}")
    print(f"  标准差: {scaler_y.scale_}")


def create_default_scalers(output_path: str):
    """
    创建默认的标准化器（基于典型参数范围）
    
    Args:
        output_path: 标准化器保存路径
    """
    print("创建默认标准化器...")
    
    # 典型参数范围的中心值和标准差
    # 这些值是基于常见钢柱设计参数估计的
    X_mean = np.array([15.0, 200.0, 5.0, 150.0, 50.0, 0.2])
    X_std = np.array([10.0, 150.0, 3.0, 80.0, 15.0, 0.15])
    
    y_mean = np.array([6.0])  # log(Pn)的均值
    y_std = np.array([1.5])   # log(Pn)的标准差
    
    # 创建标准化器
    scaler_x = StandardScaler()
    scaler_x.mean_ = X_mean
    scaler_x.scale_ = X_std
    scaler_x.var_ = X_std ** 2
    scaler_x.n_features_in_ = 6
    
    scaler_y = StandardScaler()
    scaler_y.mean_ = y_mean
    scaler_y.scale_ = y_std
    scaler_y.var_ = y_std ** 2
    scaler_y.n_features_in_ = 1
    
    SHIFT = 0.01
    
    # 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump({
            'scaler_x': scaler_x,
            'scaler_y': scaler_y,
            'SHIFT': SHIFT
        }, f)
    
    print(f"✓ 默认标准化器已保存到: {output_path}")


if __name__ == "__main__":
    # 尝试从训练数据创建
    data_path = "../../PINN model/merged.csv"
    scaler_path = "../../PINN model/normal/scalers.pkl"
    
    if os.path.exists(data_path):
        create_scalers_from_data(data_path, scaler_path)
    else:
        print(f"⚠ 未找到训练数据: {data_path}")
        print("创建默认标准化器...")
        create_default_scalers(scaler_path)

