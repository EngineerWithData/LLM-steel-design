"""
Test PINN model inference functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from agent.models import PINNPredictor


class TestPINNPredictor:
    """PINN predictor test class"""
    
    @pytest.fixture
    def predictor(self):
        """Create predictor instance"""
        return PINNPredictor()
    
    @pytest.fixture
    def model_path(self):
        """Get model path"""
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "PINN model/normal/model_20250123_165719.pth"
        )
    
    def test_perry_robertson_formula(self, predictor):
        """Test Perry-Robertson formula calculation"""
        # Test data
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # Calculate theoretical strength
        Pn = predictor._perry_robertson(
            params['A'], params['I'], params['c'],
            params['L'], params['fy'], params['delta_o']
        )
        
        # Verify result
        assert Pn > 0, "Perry-Robertson strength should be greater than 0"
        assert Pn < params['A'] * params['fy'], "Strength should not exceed section yield strength"
        assert isinstance(Pn, float), "Return value should be float"
    
    def test_perry_robertson_edge_cases(self, predictor):
        """Test Perry-Robertson formula edge cases"""
        # Test short column (high strength)
        Pn_short = predictor._perry_robertson(10.0, 100.0, 5.0, 50.0, 50.0, 0.1)
        
        # Test long column (low strength)
        Pn_long = predictor._perry_robertson(10.0, 100.0, 5.0, 300.0, 50.0, 0.1)
        
        # Long column strength should be less than short column
        assert Pn_long < Pn_short, "Long column strength should be less than short column"
    
    def test_model_loading(self, predictor, model_path):
        """Test model loading"""
        if not os.path.exists(model_path):
            pytest.skip("Model file does not exist")
        
        # Load model
        predictor.load_model(model_path)
        
        # Verify model loaded
        assert predictor.model is not None, "Model should be loaded"
        assert predictor.scaler_x is not None, "X scaler should be loaded"
        assert predictor.scaler_y is not None, "Y scaler should be loaded"
    
    def test_prediction_with_model(self, predictor, model_path):
        """Test prediction using model"""
        if not os.path.exists(model_path):
            pytest.skip("Model file does not exist")
        
        # Load model
        predictor.load_model(model_path)
        
        # Test data
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # Predict
        result = predictor.predict(params)
        
        # Verify result
        assert result['status'] == 'success', "Prediction should succeed"
        assert 'Pn' in result, "Result should contain Pn"
        assert result['Pn'] > 0, "Predicted strength should be greater than 0"
        assert 'Pn_theory' in result, "Result should contain theoretical value"
        assert 'ratio' in result, "Result should contain ratio"
    
    def test_prediction_without_model(self, predictor):
        """Test prediction without loading model"""
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        result = predictor.predict(params)
        
        # Should return error without model
        assert result['status'] == 'error', "Should return error without model"
    
    def test_missing_parameters(self, predictor):
        """Test missing parameters case"""
        # Missing delta_o parameter
        params = {
            'A': 10.0,
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0
        }
        
        result = predictor.predict(params)
        
        # Should return error
        assert result['status'] == 'error', "Should return error when parameters are missing"
        assert 'message' in result, "Error message should contain message"
    
    def test_invalid_parameters(self, predictor, model_path):
        """Test invalid parameters"""
        if not os.path.exists(model_path):
            pytest.skip("Model file does not exist")
        
        predictor.load_model(model_path)
        
        # Negative parameter
        params = {
            'A': -10.0,  # Negative
            'I': 100.0,
            'c': 5.0,
            'L': 120.0,
            'fy': 50.0,
            'delta_o': 0.1
        }
        
        # Prediction should still execute (parameter validation is at tool layer)
        result = predictor.predict(params)
        assert 'Pn' in result or result['status'] == 'error'
    
    def test_batch_prediction(self, predictor, model_path):
        """Test batch prediction"""
        if not os.path.exists(model_path):
            pytest.skip("Model file does not exist")
        
        predictor.load_model(model_path)
        
        # Multiple test cases
        test_cases = [
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 100.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 150.0, 'fy': 50.0, 'delta_o': 0.1},
            {'A': 10.0, 'I': 100.0, 'c': 5.0, 'L': 200.0, 'fy': 50.0, 'delta_o': 0.1},
        ]
        
        # Batch prediction
        results = predictor.batch_predict(test_cases)
        
        # Verify results
        assert len(results) == len(test_cases), "Result count should match input"
        
        # Verify strength decreases with increasing length
        strengths = [r['Pn'] for r in results if r['status'] == 'success']
        if len(strengths) == 3:
            assert strengths[0] > strengths[1] > strengths[2], "Strength should decrease with increasing length"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
