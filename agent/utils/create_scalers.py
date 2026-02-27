"""
Create Scalers
Generate scalers from training data and save
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
    Create scalers from training data
    
    Args:
        data_path: Training data CSV path
        output_path: Scaler save path
    """
    # Read data
    print(f"Reading data: {data_path}")
    df = pd.read_csv(data_path)
    df = df.dropna()
    
    # Features and target
    features = ['A', 'I', 'c', 'L', 'fy', 'delta_o']
    target = 'Pn'
    
    X = df[features].to_numpy()
    y = df[target].to_numpy()
    
    # Add noise (consistent with training)
    noise = np.random.normal(0, 1, y.shape)
    y = y + noise
    
    # Logarithmic transformation
    SHIFT = 0.01
    y_log = np.log(y + SHIFT)
    
    # Create scalers
    print("Creating scalers...")
    scaler_x = StandardScaler()
    scaler_x.fit(X)
    
    scaler_y = StandardScaler()
    scaler_y.fit(y_log.reshape(-1, 1))
    
    # Save scalers
    print(f"Saving scalers to: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump({
            'scaler_x': scaler_x,
            'scaler_y': scaler_y,
            'SHIFT': SHIFT
        }, f)
    
    print("✓ Scalers created successfully")
    print(f"\nX scaler parameters:")
    print(f"  Mean: {scaler_x.mean_}")
    print(f"  Std: {scaler_x.scale_}")
    print(f"\nY scaler parameters:")
    print(f"  Mean: {scaler_y.mean_}")
    print(f"  Std: {scaler_y.scale_}")


def create_default_scalers(output_path: str):
    """
    Create default scalers (based on typical parameter ranges)
    
    Args:
        output_path: Scaler save path
    """
    print("Creating default scalers...")
    
    # Center values and standard deviations for typical parameter ranges
    # These values are estimated based on common steel column design parameters
    X_mean = np.array([15.0, 200.0, 5.0, 150.0, 50.0, 0.2])
    X_std = np.array([10.0, 150.0, 3.0, 80.0, 15.0, 0.15])
    
    y_mean = np.array([6.0])  # Mean of log(Pn)
    y_std = np.array([1.5])   # Std of log(Pn)
    
    # Create scalers
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
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump({
            'scaler_x': scaler_x,
            'scaler_y': scaler_y,
            'SHIFT': SHIFT
        }, f)
    
    print(f"✓ Default scalers saved to: {output_path}")


if __name__ == "__main__":
    # Try to create from training data
    data_path = "../../PINN model/merged.csv"
    scaler_path = "../../PINN model/normal/scalers.pkl"
    
    if os.path.exists(data_path):
        create_scalers_from_data(data_path, scaler_path)
    else:
        print(f"⚠ Training data not found: {data_path}")
        print("Creating default scalers...")
        create_default_scalers(scaler_path)
