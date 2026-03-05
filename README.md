# MachineLearningModel

A complete, production-ready Machine Learning project demonstrating MLOps best practices — from data preprocessing and model training to REST API serving and Docker deployment.

## Project

### [ML Housing Prediction](ml-housing-prediction/)

A linear regression model that predicts housing prices based on property features. This project showcases an end-to-end MLOps workflow including:

- **Data Processing** — Load, explore, and preprocess housing data with pandas
- **Model Training** — Train and evaluate a linear regression model with scikit-learn
- **REST API** — Serve predictions via a Flask REST API
- **Containerization** — Docker and Docker Compose configurations for deployment
- **Documentation** — Comprehensive guides covering architecture, deployment, and API usage

#### Quick Links

| Resource | Description |
|----------|-------------|
| [README](ml-housing-prediction/README.md) | Full project documentation |
| [Quick Start](ml-housing-prediction/QUICK_START.md) | Get up and running in 5 minutes |
| [Architecture](ml-housing-prediction/ARCHITECTURE.md) | System design and component overview |
| [Deployment](ml-housing-prediction/DEPLOYMENT.md) | Deployment guides (local, Docker, AWS, GCP, Azure) |
| [API Examples](ml-housing-prediction/API_EXAMPLES.md) | Code examples for interacting with the API |

## Getting Started

```bash
# Clone the repository
git clone https://github.com/SumitCodesAI/MachineLearningModel.git
cd MachineLearningModel/ml-housing-prediction

# Install dependencies
pip install -r requirements.txt

# Generate data and train the model
python -m src.train_model

# Start the prediction API
python app.py
```

For a detailed walkthrough, see the [Quick Start Guide](ml-housing-prediction/QUICK_START.md).

## Tech Stack

- **Language**: Python 3.11+
- **ML**: scikit-learn, pandas, NumPy
- **API**: Flask
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest

## License

MIT
