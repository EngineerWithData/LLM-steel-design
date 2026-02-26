"""
PINN Model Inference Module
For loading pre-trained PINN models and predicting steel component strength
"""

import torch
import torch.nn as nn
import numpy as np
import pickle
import os
from typing import Dict, Union, Tuple


class PINN(nn.Module):
    """Physics-Informed Neural Network Model"""
    
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
    """Standard Scaler"""
    
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
    """PINN Model Predictor"""
    
    def __init__(self, model_path: str = None, scaler_path: str = None):
        """
        Initialize PINN Predictor
        
        Args:
            model_path: Pre-trained model path
            scaler_path: Scaler path
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler_x = None
        self.scaler_y = None
        self.SHIFT = 0.01  # Logarithmic transformation offset
        
        # Feature names
        self.feature_names = ['A', 'I', 'c', 'L', 'fy', 'delta_o']
        
        if model_path:
            self.load_model(model_path, scaler_path)
    
    def load_model(self, model_path: str, scaler_path: str = None):
        """
        Load pre-trained model and scaler
        
        Args:
            model_path: Model file path
            scaler_path: Scaler file path
        """
        # Load model
        self.model = PINN(in_dim=6, h_dim=64, out_dim=1)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        
        # Automatically find scaler
        if scaler_path is None:
            # Try to find scalers.pkl in the same directory as the model
            model_dir = os.path.dirname(model_path)
            scaler_path = os.path.join(model_dir, 'scalers.pkl')
        
        # Load or initialize scaler
        if scaler_path and os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                scalers = pickle.load(f)
                self.scaler_x = scalers['scaler_x']
                self.scaler_y = scalers['scaler_y']
                if 'SHIFT' in scalers:
                    self.SHIFT = scalers['SHIFT']
            print(f"✓ Scaler loaded: {scaler_path}")
        else:
            # If no saved scaler, use default values
            print("Warning: Scaler file not found, using default parameters")
            self.scaler_x = StandardScaler()
            self.scaler_y = StandardScaler()
    
    def predict(self, input_params: Dict[str, float]) -> Dict[str, Union[float, str]]:
        """
        Predict compressive strength of steel component
        
        Args:
            input_params: Input parameter dictionary containing:
                - A: Cross-sectional area (in²)
                - I: Moment of inertia (in⁴)
                - c: Distance from section center to edge (in)
                - L: Column length (in)
                - fy: Yield strength (ksi)
                - delta_o: Initial imperfection (in)
        
        Returns:
            Prediction result dictionary containing:
                - Pn: Predicted compressive strength (kip)
                - status: Prediction status
                - message: Additional information
        """
        try:
            # Validate input parameters
            missing_params = [p for p in self.feature_names if p not in input_params]
            if missing_params:
                return {
                    'Pn': None,
                    'status': 'error',
                    'message': f'Missing required parameters: {", ".join(missing_params)}'
                }
            
            # Prepare input data
            X = np.array([[input_params[f] for f in self.feature_names]])
            
            # Standardize
            if self.scaler_x.mean_ is not None:
                X_scaled = self.scaler_x.transform(X)
            else:
                X_scaled = X
            
            # Convert to tensor
            X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)
            
            # Predict
            with torch.no_grad():
                y_pred_scaled = self.model(X_tensor)
            
            # Inverse standardization
            y_pred_scaled_np = y_pred_scaled.cpu().numpy()
            
            if self.scaler_y.mean_ is not None:
                y_log = self.scaler_y.inverse_transform(y_pred_scaled_np)
            else:
                y_log = y_pred_scaled_np
            
            # Inverse logarithmic transformation
            Pn = np.exp(y_log[0, 0]) - self.SHIFT
            
            # Calculate Perry-Robertson theoretical value as reference
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
                'message': 'Prediction successful'
            }
            
        except Exception as e:
            return {
                'Pn': None,
                'status': 'error',
                'message': f'Prediction failed: {str(e)}'
            }
    
    def _perry_robertson(self, a: float, i: float, c: float, l: float, 
                        fy: float, d: float) -> float:
        """
        Perry-Robertson formula for theoretical strength calculation
        
        Args:
            a: Cross-sectional area (in²)
            i: Moment of inertia (in⁴)
            c: Distance from section center to edge (in)
            l: Column length (in)
            fy: Yield strength (ksi)
            d: Initial imperfection (in)
        
        Returns:
            Theoretical compressive strength (kip)
        """
        import math
        
        e = 29000  # Steel elastic modulus (ksi)
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
        Batch prediction
        
        Args:
            input_list: List of input parameters
        
        Returns:
            List of prediction results
        """
        results = []
        for input_params in input_list:
            result = self.predict(input_params)
            results.append(result)
        return results
    
    def save_scalers(self, scaler_path: str):
        """
        Save scaler
        
        Args:
            scaler_path: Save path
        """
        with open(scaler_path, 'wb') as f:
            pickle.dump({
                'scaler_x': self.scaler_x,
                'scaler_y': self.scaler_y
            }, f)
        print(f"Scaler saved to: {scaler_path}")


if __name__ == "__main__":
    # Test code
    predictor = PINNPredictor()
    
    # Example input
    test_input = {
        'A': 10.0,      # Cross-sectional area (in²)
        'I': 100.0,     # Moment of inertia (in⁴)
        'c': 5.0,       # Distance from section center to edge (in)
        'L': 120.0,     # Column length (in)
        'fy': 50.0,     # Yield strength (ksi)
        'delta_o': 0.1  # Initial imperfection (in)
    }
    
    result = predictor.predict(test_input)
    print("Prediction result:", result)
