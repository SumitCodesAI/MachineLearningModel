"""
Prediction Module
This module handles making predictions with the trained model.
"""

import os
import pickle
import json
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelPredictor:
    """Handles model predictions."""
    
    def __init__(self, model_dir='models'):
        """
        Initialize the ModelPredictor.
        
        Args:
            model_dir: Directory containing the saved model files
        """
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.load_model()
    
    def load_model(self):
        """Load the saved model, scaler, and feature names."""
        logger.info(f"Loading model from {self.model_dir}")
        
        # Load model
        model_path = os.path.join(self.model_dir, 'linear_regression_model.pkl')
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        logger.info("✓ Model loaded")
        
        # Load scaler
        scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        logger.info("✓ Scaler loaded")
        
        # Load feature names
        features_path = os.path.join(self.model_dir, 'features.json')
        with open(features_path, 'r') as f:
            self.feature_names = json.load(f)
        logger.info(f"✓ Features loaded: {self.feature_names}")
    
    def predict(self, features):
        """
        Make a prediction.
        
        Args:
            features: Dict or list with feature values in correct order
            
        Returns:
            Predicted price
        """
        if isinstance(features, dict):
            # Convert dict to array in correct order
            features_array = np.array([features[f] for f in self.feature_names]).reshape(1, -1)
        else:
            features_array = np.array(features).reshape(1, -1)
        
        # Scale features
        scaled_features = self.scaler.transform(features_array)
        
        # Predict
        prediction = self.model.predict(scaled_features)[0]
        
        return prediction
    
    def predict_batch(self, data_dict):
        """
        Make predictions for multiple samples.
        
        Args:
            data_dict: Dictionary with lists of feature values
            
        Returns:
            Array of predictions
        """
        df = pd.DataFrame(data_dict)
        features = df[self.feature_names].values
        scaled_features = self.scaler.transform(features)
        predictions = self.model.predict(scaled_features)
        return predictions
    
    def predict_with_confidence(self, features):
        """
        Make a prediction and provide model confidence information.
        
        Args:
            features: Dict or list with feature values
            
        Returns:
            Dictionary with prediction and metadata
        """
        prediction = self.predict(features)
        
        # Load metrics for context
        metrics_path = os.path.join(self.model_dir, 'metrics.json')
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        
        return {
            'prediction': float(prediction),
            'confidence': metrics['test']['r2'],  # Model R² score
            'model_rmse': metrics['test']['rmse']
        }

def predict_single_house(features_dict, model_dir='models'):
    """
    Convenience function to predict for a single house.
    
    Args:
        features_dict: Dictionary with feature names and values
        model_dir: Directory containing the model
        
    Returns:
        Predicted price
    """
    predictor = ModelPredictor(model_dir)
    return predictor.predict(features_dict)

def predict_batch_houses(csv_path, model_dir='models'):
    """
    Convenience function to predict for multiple houses from CSV.
    
    Args:
        csv_path: Path to CSV file with feature data
        model_dir: Directory containing the model
        
    Returns:
        Array of predictions
    """
    predictor = ModelPredictor(model_dir)
    data = pd.read_csv(csv_path)
    return predictor.predict_batch(data.to_dict(orient='list'))

if __name__ == "__main__":
    # Example usage
    predictor = ModelPredictor()
    
    # Example 1: Predict for a single house
    example_house = {
        'square_feet': 2500,
        'num_bedrooms': 4,
        'num_bathrooms': 2.5,
        'year_built': 2010,
        'distance_to_city': 5.0
    }
    
    logger.info("Making prediction for example house:")
    logger.info(example_house)
    prediction = predictor.predict(example_house)
    logger.info(f"Predicted price: ${prediction:,.2f}")
    
    # Example 2: Prediction with confidence
    result = predictor.predict_with_confidence(example_house)
    logger.info(f"Prediction result: {result}")
