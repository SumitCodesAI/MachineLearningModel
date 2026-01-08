"""
Unit tests for the ML Housing Prediction project.
"""

import pytest
import os
import json
import numpy as np
from src.predict import ModelPredictor
from src.data_preprocessing import DataProcessor

class TestDataProcessor:
    """Test data preprocessing functionality."""
    
    @pytest.fixture
    def sample_data_path(self):
        """Provide path to sample data."""
        return 'data/house_data.csv'
    
    def test_load_data(self, sample_data_path):
        """Test loading data from CSV."""
        if os.path.exists(sample_data_path):
            processor = DataProcessor(sample_data_path)
            df = processor.load_data()
            assert df is not None
            assert len(df) > 0

class TestPredictor:
    """Test prediction functionality."""
    
    @pytest.fixture
    def predictor(self):
        """Provide ModelPredictor instance if models exist."""
        model_dir = 'models'
        if os.path.exists(os.path.join(model_dir, 'linear_regression_model.pkl')):
            return ModelPredictor(model_dir)
        return None
    
    def test_predict_single(self, predictor):
        """Test single house prediction."""
        if predictor is None:
            pytest.skip("Model not trained")
        
        features = {
            'square_feet': 2500,
            'num_bedrooms': 4,
            'num_bathrooms': 2.5,
            'year_built': 2010,
            'distance_to_city': 5.0
        }
        
        prediction = predictor.predict(features)
        assert isinstance(prediction, (float, np.floating))
        assert prediction > 0

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
