"""
Model Training Module
This module handles training the linear regression model.
"""

import os
import pickle
import json
import logging
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from src.data_preprocessing import preprocess_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Handles model training and evaluation."""
    
    def __init__(self):
        """Initialize the ModelTrainer."""
        self.model = None
        self.metrics = {}
        self.processor = None
        
    def train(self, X_train, y_train):
        """
        Train the linear regression model.
        
        Args:
            X_train: Training features
            y_train: Training target values
            
        Returns:
            Trained model
        """
        logger.info("Training linear regression model...")
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        logger.info("✓ Model trained successfully!")
        return self.model
    
    def evaluate(self, X_train, y_train, X_test, y_test):
        """
        Evaluate model on both training and test sets.
        
        Args:
            X_train: Training features
            y_train: Training target values
            X_test: Test features
            y_test: Test target values
            
        Returns:
            Dictionary with metrics
        """
        logger.info("Evaluating model performance...")
        
        # Predictions
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Calculate metrics for training set
        train_mse = mean_squared_error(y_train, y_train_pred)
        train_rmse = np.sqrt(train_mse)
        train_mae = mean_absolute_error(y_train, y_train_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        
        # Calculate metrics for test set
        test_mse = mean_squared_error(y_test, y_test_pred)
        test_rmse = np.sqrt(test_mse)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        
        self.metrics = {
            'train': {
                'mse': float(train_mse),
                'rmse': float(train_rmse),
                'mae': float(train_mae),
                'r2': float(train_r2)
            },
            'test': {
                'mse': float(test_mse),
                'rmse': float(test_rmse),
                'mae': float(test_mae),
                'r2': float(test_r2)
            }
        }
        
        # Print metrics
        logger.info("=== Model Performance ===")
        logger.info(f"Training R² Score: {train_r2:.4f}")
        logger.info(f"Test R² Score: {test_r2:.4f}")
        logger.info(f"Test RMSE: ${test_rmse:,.2f}")
        logger.info(f"Test MAE: ${test_mae:,.2f}")
        
        return self.metrics
    
    def get_model_info(self, feature_names):
        """
        Get model coefficients and information.
        
        Args:
            feature_names: List of feature names
            
        Returns:
            Dictionary with model information
        """
        model_info = {
            'coefficients': {},
            'intercept': float(self.model.intercept_)
        }
        
        for feature, coef in zip(feature_names, self.model.coef_):
            model_info['coefficients'][feature] = float(coef)
        
        return model_info
    
    def save_model(self, model_dir='models'):
        """
        Save the trained model and metrics.
        
        Args:
            model_dir: Directory to save the model
        """
        os.makedirs(model_dir, exist_ok=True)
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model
        model_path = os.path.join(model_dir, 'linear_regression_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        logger.info(f"✓ Model saved to {model_path}")
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.processor.scaler, f)
        logger.info(f"✓ Scaler saved to {scaler_path}")
        
        # Save metrics
        metrics_path = os.path.join(model_dir, 'metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=4)
        logger.info(f"✓ Metrics saved to {metrics_path}")
        
        # Save feature names
        features_path = os.path.join(model_dir, 'features.json')
        features = self.processor.get_feature_names()
        with open(features_path, 'w') as f:
            json.dump(features, f)
        logger.info(f"✓ Features saved to {features_path}")
        
        return model_path, scaler_path, metrics_path, features_path

def train_pipeline(data_filepath='data/house_data.csv', model_dir='models'):
    """
    Complete training pipeline: preprocess data -> train model -> save model.
    
    Args:
        data_filepath: Path to the CSV file
        model_dir: Directory to save the model
        
    Returns:
        Trained ModelTrainer object
    """
    logger.info("=" * 50)
    logger.info("Starting ML Training Pipeline")
    logger.info("=" * 50)
    
    # Preprocessing
    X_train, X_test, y_train, y_test, processor = preprocess_pipeline(data_filepath)
    
    # Training
    trainer = ModelTrainer()
    trainer.processor = processor
    trainer.train(X_train, y_train)
    
    # Evaluation
    trainer.evaluate(X_train, y_train, X_test, y_test)
    
    # Model info
    feature_names = processor.get_feature_names()
    model_info = trainer.get_model_info(feature_names)
    logger.info("\n=== Model Coefficients ===")
    logger.info(f"Intercept: ${model_info['intercept']:,.2f}")
    for feature, coef in model_info['coefficients'].items():
        logger.info(f"{feature}: {coef:.2f}")
    
    # Save
    trainer.save_model(model_dir)
    
    logger.info("=" * 50)
    logger.info("Training pipeline completed successfully!")
    logger.info("=" * 50)
    
    return trainer

if __name__ == "__main__":
    train_pipeline()
