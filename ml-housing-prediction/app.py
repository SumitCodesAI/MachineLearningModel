"""
Flask API for ML Model Serving
This module provides REST endpoints to serve predictions from the trained model.
"""

import os
import json
from flask import Flask, request, jsonify
from src.predict import ModelPredictor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize predictor globally
try:
    predictor = ModelPredictor(model_dir='models')
    logger.info("✓ Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    predictor = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'ML Housing Prediction API is running'
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction for a single house.
    
    Expected JSON:
    {
        "square_feet": 2500,
        "num_bedrooms": 4,
        "num_bathrooms": 2.5,
        "year_built": 2010,
        "distance_to_city": 5.0
    }
    """
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['square_feet', 'num_bedrooms', 'num_bathrooms', 'year_built', 'distance_to_city']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            return jsonify({'error': f'Missing fields: {missing_fields}'}), 400
        
        # Make prediction
        prediction = predictor.predict(data)
        result = predictor.predict_with_confidence(data)
        
        return jsonify({
            'success': True,
            'input': data,
            'prediction': {
                'price': result['prediction'],
                'currency': 'USD',
                'confidence': result['confidence'],
                'model_rmse': result['model_rmse']
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """
    Make predictions for multiple houses.
    
    Expected JSON (list of house objects):
    [
        {
            "square_feet": 2500,
            "num_bedrooms": 4,
            "num_bathrooms": 2.5,
            "year_built": 2010,
            "distance_to_city": 5.0
        },
        ...
    ]
    """
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Expected list of house objects'}), 400
        
        # Convert to format expected by predict_batch
        data_dict = {key: [house[key] for house in data] for key in data[0].keys()}
        
        predictions = predictor.predict_batch(data_dict)
        
        # Load metrics
        with open('models/metrics.json', 'r') as f:
            metrics = json.load(f)
        
        return jsonify({
            'success': True,
            'count': len(predictions),
            'predictions': [
                {
                    'input': data[i],
                    'predicted_price': float(predictions[i]),
                    'currency': 'USD'
                } for i in range(len(predictions))
            ],
            'model_confidence': metrics['test']['r2']
        }), 200
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get model information and metadata."""
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Load metrics and features
        with open('models/metrics.json', 'r') as f:
            metrics = json.load(f)
        
        with open('models/features.json', 'r') as f:
            features = json.load(f)
        
        # Get coefficients
        coefficients = {}
        for feature, coef in zip(features, predictor.model.coef_):
            coefficients[feature] = float(coef)
        
        return jsonify({
            'success': True,
            'model_type': 'Linear Regression',
            'features': features,
            'coefficients': coefficients,
            'intercept': float(predictor.model.intercept_),
            'performance': metrics
        }), 200
    
    except Exception as e:
        logger.error(f"Model info error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/docs', methods=['GET'])
def api_docs():
    """Return API documentation."""
    docs = {
        'title': 'ML Housing Prediction API',
        'version': '1.0.0',
        'description': 'REST API for predicting house prices using linear regression',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint',
                'response': {'status': 'healthy'}
            },
            '/predict': {
                'method': 'POST',
                'description': 'Predict price for a single house',
                'request_body': {
                    'square_feet': 'float',
                    'num_bedrooms': 'int',
                    'num_bathrooms': 'float',
                    'year_built': 'int',
                    'distance_to_city': 'float'
                }
            },
            '/predict_batch': {
                'method': 'POST',
                'description': 'Predict prices for multiple houses',
                'request_body': 'List of house objects'
            },
            '/model_info': {
                'method': 'GET',
                'description': 'Get model information and coefficients'
            }
        }
    }
    return jsonify(docs), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
