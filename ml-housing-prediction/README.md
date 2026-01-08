# ML Housing Prediction - MLOps Project

## Overview
This is a complete end-to-end MLOps project showcasing:
- **Data Processing**: Load, explore, and preprocess housing data
- **Model Training**: Linear regression model with evaluation metrics
- **Model Serving**: Flask REST API for predictions
- **Deployment**: Docker containerization and deployment ready
- **Documentation**: Complete project documentation and examples

## Project Structure
```
ml-housing-prediction/
├── data/
│   ├── generate_data.py          # Generate synthetic housing dataset
│   └── house_data.csv            # Housing dataset (CSV)
├── src/
│   ├── __init__.py               # Package initialization
│   ├── data_preprocessing.py      # Data loading and preprocessing
│   ├── train_model.py            # Model training and evaluation
│   └── predict.py                # Prediction inference
├── models/                        # Trained models (generated after training)
│   ├── linear_regression_model.pkl
│   ├── scaler.pkl
│   ├── metrics.json
│   └── features.json
├── notebooks/                     # Jupyter notebooks for exploration
├── tests/                         # Unit tests
├── app.py                         # Flask API application
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker container configuration
├── docker-compose.yml             # Docker Compose configuration
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)
- pip or conda for package management

### Installation

1. **Clone the repository**
```bash
cd ml-housing-prediction
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Quick Start

#### Step 1: Generate Data
```bash
cd data
python generate_data.py
cd ..
```
This creates `data/house_data.csv` with 200 housing records including:
- `square_feet`: House area
- `num_bedrooms`: Number of bedrooms
- `num_bathrooms`: Number of bathrooms
- `year_built`: Construction year
- `distance_to_city`: Distance to city center (miles)
- `price`: House price (target variable)

#### Step 2: Train the Model
```bash
python -m src.train_model
```

This will:
- Load and explore the data
- Split into 80% train, 20% test
- Train a linear regression model
- Evaluate on both sets
- Save model, scaler, and metrics to `models/` directory

**Expected Output:**
```
=== Model Performance ===
Training R² Score: 0.9234
Test R² Score: 0.9187
Test RMSE: $43,215.50
Test MAE: $32,847.30
```

#### Step 3: Test Predictions
```bash
python -m src.predict
```

This demonstrates how to:
- Load the trained model
- Make single predictions
- Get confidence scores
- View model coefficients

#### Step 4: Start the API Server
```bash
python app.py
```

The Flask server will start at `http://localhost:5000`

## API Documentation

### Health Check
```bash
GET /health
```
Response: `{"status": "healthy", "message": "..."}`

### Single Prediction
```bash
POST /predict
Content-Type: application/json

{
    "square_feet": 2500,
    "num_bedrooms": 4,
    "num_bathrooms": 2.5,
    "year_built": 2010,
    "distance_to_city": 5.0
}
```

**Response:**
```json
{
    "success": true,
    "prediction": {
        "price": 456789.50,
        "confidence": 0.9187,
        "model_rmse": 43215.50
    }
}
```

### Batch Predictions
```bash
POST /predict_batch
Content-Type: application/json

[
    {"square_feet": 2500, "num_bedrooms": 4, ...},
    {"square_feet": 3000, "num_bedrooms": 5, ...}
]
```

### Model Information
```bash
GET /model_info
```

Returns model coefficients and performance metrics.

### API Documentation
```bash
GET /api/docs
```

Returns full API documentation.

## Understanding the ML Pipeline

### 1. Data Preprocessing (`src/data_preprocessing.py`)
```python
from src.data_preprocessing import preprocess_pipeline

X_train, X_test, y_train, y_test, processor = preprocess_pipeline('data/house_data.csv')
```

**What happens:**
- **Load**: Read CSV into pandas DataFrame
- **Explore**: Display statistics and correlations
- **Clean**: Handle missing values
- **Outliers**: Remove data points > 3 standard deviations
- **Split**: 80/20 train/test split
- **Scale**: StandardScaler normalization (mean=0, std=1)

### 2. Model Training (`src/train_model.py`)
```python
from src.train_model import train_pipeline

trainer = train_pipeline()
```

**What happens:**
- **Train**: Fit LinearRegression on training data
- **Evaluate**: Calculate R², RMSE, MAE on both sets
- **Save**: Persist model, scaler, metrics, and features

**Key Metrics:**
- **R² Score**: Proportion of variance explained (0-1, higher is better)
- **RMSE**: Root Mean Squared Error (in dollars)
- **MAE**: Mean Absolute Error (average prediction error)

### 3. Inference/Prediction (`src/predict.py`)
```python
from src.predict import ModelPredictor

predictor = ModelPredictor()
price = predictor.predict({
    'square_feet': 2500,
    'num_bedrooms': 4,
    'num_bathrooms': 2.5,
    'year_built': 2010,
    'distance_to_city': 5.0
})
```

**How it works:**
- Load saved model and scaler
- Accept new data point
- Apply same scaling transformation
- Generate prediction

## Deployment

### Option 1: Docker (Recommended)
```bash
# Build the image
docker build -t ml-housing-api .

# Run the container
docker run -p 5000:5000 ml-housing-api

# Or use Docker Compose
docker-compose up
```

### Option 2: Cloud Deployment
- **AWS**: Use AWS SageMaker or EC2 + Flask
- **Google Cloud**: Deploy to Cloud Run or App Engine
- **Azure**: Use Azure Machine Learning Service
- **Heroku**: Simple deployment with Procfile

Example for Heroku:
```bash
git push heroku main
```

### Option 3: Local Development
```bash
python app.py
# Visit http://localhost:5000/health
```

## Key Concepts for MLOps Portfolio

This project demonstrates:

1. **Data Handling**: 
   - CSV loading with pandas
   - EDA (Exploratory Data Analysis)
   - Data validation and cleaning

2. **ML Development**:
   - Train/test splitting
   - Feature scaling
   - Model training and evaluation
   - Metrics tracking

3. **Reproducibility**:
   - Fixed random seeds
   - Saved scaler and model
   - Version control with features.json

4. **API Design**:
   - RESTful endpoints
   - Error handling
   - Input validation
   - Response formatting

5. **Deployment**:
   - Containerization (Docker)
   - Service health checks
   - Production-ready configurations

6. **Documentation**:
   - Code comments
   - API documentation
   - README and guides

## Testing

Create test cases in `tests/` directory:

```python
# tests/test_predict.py
import pytest
from src.predict import ModelPredictor

def test_prediction():
    predictor = ModelPredictor()
    result = predictor.predict({
        'square_feet': 2500,
        'num_bedrooms': 4,
        'num_bathrooms': 2.5,
        'year_built': 2010,
        'distance_to_city': 5.0
    })
    assert isinstance(result, float)
    assert result > 0
```

Run tests:
```bash
pytest tests/
```

## Model Interpretability

The model is a **linear regression**, which is highly interpretable:

```
Predicted Price = Intercept + 
                  (square_feet * coef) +
                  (bedrooms * coef) +
                  (bathrooms * coef) +
                  (year_built * coef) +
                  (distance_to_city * coef)
```

View coefficients:
```bash
curl http://localhost:5000/model_info
```

## Performance Tuning

To improve model performance:

1. **Feature Engineering**: Add polynomial features, interactions
2. **Data Quality**: Collect more data, fix outliers
3. **Hyperparameters**: Adjust regularization (use Ridge/Lasso)
4. **Ensemble Methods**: Use Random Forest, Gradient Boosting

## CI/CD Integration

Create `.github/workflows/deploy.yml` for GitHub Actions:

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker
        run: docker build -t myrepo/ml-housing:latest .
```

## Next Steps for Portfolio

1. ✅ Train and save the model
2. ✅ Create Flask API
3. ✅ Dockerize the application
4. Add monitoring (Prometheus, Grafana)
5. Add model versioning
6. Set up CI/CD pipeline
7. Deploy to cloud platform
8. Create performance dashboard
9. Add model retraining schedule
10. Implement A/B testing framework

## Troubleshooting

**Model not found error:**
```bash
# Ensure you've run training first
python -m src.train_model
```

**Port 5000 already in use:**
```bash
# Use a different port
python app.py --port 8000
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## License
MIT

## Author
Your Name - ML Engineer

---

**Ready for portfolio!** Share the GitHub repository link in your resume. 🚀
