# ML Housing Prediction - Architecture Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                              │
│  (Web Browser, Mobile App, Other Services)                   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (Flask)                          │
│  ┌──────────────┬──────────────┬──────────────┐              │
│  │ /health      │ /predict     │ /model_info  │              │
│  │ /predict_batch │ /api/docs  │              │              │
│  └──────────────┴──────────────┴──────────────┘              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              ML Inference Layer                               │
│  ┌─────────────────────────────────────┐                    │
│  │   ModelPredictor (predict.py)        │                    │
│  │  - Load trained model from disk      │                    │
│  │  - Apply feature scaling             │                    │
│  │  - Generate predictions              │                    │
│  │  - Return results with confidence    │                    │
│  └─────────────────────────────────────┘                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Model Storage Layer                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ models/                                                  │  │
│  │  ├── linear_regression_model.pkl   (Trained model)      │  │
│  │  ├── scaler.pkl                    (Feature scaler)     │  │
│  │  ├── features.json                 (Feature names)      │  │
│  │  └── metrics.json                  (Performance stats)   │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Training Pipeline
```
Raw CSV Data
    ↓
Data Loading (pandas)
    ↓
Exploratory Data Analysis (statistics, correlations)
    ↓
Data Cleaning (missing values, outliers)
    ↓
Train/Test Split (80/20)
    ↓
Feature Scaling (StandardScaler)
    ↓
Model Training (LinearRegression)
    ↓
Model Evaluation (R², RMSE, MAE)
    ↓
Save Model & Artifacts
```

### Prediction Pipeline
```
New House Features (JSON)
    ↓
Input Validation
    ↓
Load Scaler
    ↓
Scale Features
    ↓
Load Model
    ↓
Generate Prediction
    ↓
Load Metrics
    ↓
Return Result with Confidence
```

## Component Details

### 1. Data Preprocessing (`src/data_preprocessing.py`)

**Purpose**: Transform raw data into model-ready features

**Key Classes**:
- `DataProcessor`: Main preprocessing orchestrator
  - `load_data()`: Read CSV file
  - `explore_data()`: Display statistics
  - `handle_missing_values()`: Fill NaN values
  - `remove_outliers()`: Filter extreme values
  - `prepare_train_test_split()`: Create train/test sets
  - `scale_features()`: Normalize features

**Why Scaling Matters**:
- Features have different ranges (square_feet: 1000-5000, bathrooms: 1-4)
- Linear regression works better with normalized features
- StandardScaler: Mean=0, Std Dev=1

### 2. Model Training (`src/train_model.py`)

**Purpose**: Train and save the ML model

**Key Classes**:
- `ModelTrainer`: Handles training and evaluation
  - `train()`: Fit LinearRegression
  - `evaluate()`: Calculate metrics
  - `save_model()`: Persist artifacts

**Algorithm**: Linear Regression
```
Price = w₀ + w₁×square_feet + w₂×bedrooms + w₃×bathrooms + w₄×year_built + w₅×distance
```

Where:
- `w₀` = Intercept (base price)
- `w₁...w₅` = Coefficients (weights for each feature)

**Evaluation Metrics**:
- **R² Score**: Percentage of variance explained (0-1)
- **RMSE**: Average prediction error in dollars
- **MAE**: Mean absolute error

### 3. Inference (`src/predict.py`)

**Purpose**: Generate predictions for new data

**Key Classes**:
- `ModelPredictor`: Loads and uses trained model
  - `load_model()`: Load from disk
  - `predict()`: Single prediction
  - `predict_batch()`: Multiple predictions
  - `predict_with_confidence()`: Prediction + metrics

### 4. API Layer (`app.py`)

**Purpose**: Expose ML model as REST service

**Endpoints**:

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Check API status |
| POST | `/predict` | Single prediction |
| POST | `/predict_batch` | Multiple predictions |
| GET | `/model_info` | Model coefficients |
| GET | `/api/docs` | API documentation |

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11 | Core implementation |
| **ML Framework** | scikit-learn | Linear regression |
| **Data Handling** | pandas, numpy | Data manipulation |
| **API Framework** | Flask | REST API server |
| **WSGI Server** | Gunicorn | Production server |
| **Containerization** | Docker | Deployment |
| **Container Orchestration** | Docker Compose | Local multi-container |

## Feature Engineering

### Raw Features
```json
{
    "square_feet": 2500,      // House size
    "num_bedrooms": 4,        // Bedrooms
    "num_bathrooms": 2.5,     // Bathrooms
    "year_built": 2010,       // Age indicator
    "distance_to_city": 5.0   // Location proximity
}
```

### Feature Correlations with Price
```
square_feet        → 0.92  (Strong positive)
num_bedrooms       → 0.89  (Strong positive)
num_bathrooms      → 0.87  (Strong positive)
year_built         → 0.81  (Strong positive)
distance_to_city   → -0.73 (Strong negative)
```

## Deployment Architecture

### Local Development
```
Your Machine
  └─ Python Environment
      └─ Flask Development Server (localhost:5000)
```

### Docker Deployment
```
Docker Container
  ├─ Python Runtime
  ├─ Flask Application
  ├─ Gunicorn WSGI Server
  └─ Model & Scaler Files
  
Port Mapping: Host:5000 → Container:5000
```

### Cloud Deployment Options

**AWS**:
```
AWS EC2 Instance
  └─ Docker Container
      └─ Flask + Gunicorn (Port 5000)
```

**Google Cloud**:
```
Cloud Run
  └─ Docker Image
      └─ Stateless Flask Service
```

**Kubernetes** (Advanced):
```
Kubernetes Cluster
  ├─ Deployment
  │   ├─ Pod 1 (Flask Container)
  │   ├─ Pod 2 (Flask Container)
  │   └─ Pod 3 (Flask Container)
  ├─ Service (LoadBalancer)
  └─ ConfigMaps (Model artifacts)
```

## Performance Characteristics

### Training
- **Time**: ~1-2 seconds (on typical hardware)
- **Data Size**: 200 samples, 5 features
- **Memory**: ~100 MB

### Inference
- **Latency**: ~10-50 ms per prediction
- **Throughput**: ~100+ predictions/second
- **Model Size**: ~2 KB (pickle file)

### Scalability
- Single instance can handle ~1000 requests/sec
- Horizontal scaling via load balancer
- Auto-scaling with cloud platforms

## Data Pipeline

### Input Validation
```python
required_fields = ['square_feet', 'num_bedrooms', 'num_bathrooms', 'year_built', 'distance_to_city']
missing_fields = [f for f in required_fields if f not in request_data]
if missing_fields:
    return error
```

### Feature Scaling
```python
X_scaled = scaler.transform([[square_feet, bedrooms, bathrooms, year_built, distance]])
```

### Prediction
```python
price = model.predict(X_scaled)[0]
```

## Error Handling

```
Request
  ↓
Validate Input
  ├─ Missing fields? → Return 400
  └─ Invalid types? → Return 400
  ↓
Load Model
  ├─ Model missing? → Return 500
  └─ Scaler missing? → Return 500
  ↓
Generate Prediction
  ├─ Scaling error? → Return 500
  └─ Prediction error? → Return 500
  ↓
Return Result (200)
```

## Monitoring & Logging

### Application Logs
- Model loading status
- Prediction requests
- Errors and exceptions

### Metrics to Track
- Request count
- Average latency
- Error rate
- Model accuracy (R², RMSE)

### Example Dashboard
```
┌─────────────────────────────────────┐
│  ML Housing API Metrics              │
├─────────────────────────────────────┤
│ Requests/Hour:      450              │
│ Avg Latency:        25 ms            │
│ Error Rate:         0.5%             │
│ Model R² Score:     0.9187           │
│ Model RMSE:         $43,215          │
└─────────────────────────────────────┘
```

## Security Considerations

1. **Input Validation**: Check all incoming data
2. **Rate Limiting**: Prevent DoS attacks
3. **HTTPS**: Use TLS in production
4. **Authentication**: Add API keys if needed
5. **Model Updates**: Version control models
6. **Data Privacy**: Don't log sensitive data

## Versioning

### Model Versioning Strategy
```
models/
├── v1/
│   ├── model.pkl
│   ├── scaler.pkl
│   └── metrics.json
├── v2/
│   └── ...
└── current -> v2/
```

### API Versioning
```
/api/v1/predict
/api/v2/predict (with new features)
```

## Maintenance Plan

1. **Daily**: Monitor error rates
2. **Weekly**: Review prediction accuracy
3. **Monthly**: Retrain with new data
4. **Quarterly**: Update dependencies
5. **Annually**: Major feature updates

---

This architecture is designed for:
- ✅ **Scalability**: Easy to scale horizontally
- ✅ **Maintainability**: Clear separation of concerns
- ✅ **Reliability**: Error handling and logging
- ✅ **Testability**: Modular design
- ✅ **Reproducibility**: Fixed random seeds, saved artifacts
