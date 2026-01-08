# Deployment Guide

## Step-by-Step Deployment

This guide covers deploying the ML Housing Prediction API to various platforms.

## Prerequisites

- Git installed
- Docker installed (for Docker deployments)
- Cloud account (for cloud deployments)
- Basic command-line knowledge

---

## Option 1: Local Deployment (Development)

### 1.1 Setup Environment
```bash
# Clone or navigate to project
cd ml-housing-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Generate Data and Train Model
```bash
# Generate synthetic housing data
cd data
python generate_data.py
cd ..

# Train the model
python -m src.train_model
```

Expected output:
```
=== Model Performance ===
Training R² Score: 0.9234
Test R² Score: 0.9187
Test RMSE: $43,215.50
```

### 1.3 Start the API Server
```bash
python app.py
```

Server runs at: `http://localhost:5000`

### 1.4 Test the API
```bash
# Health check
curl http://localhost:5000/health

# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "square_feet": 2500,
    "num_bedrooms": 4,
    "num_bathrooms": 2.5,
    "year_built": 2010,
    "distance_to_city": 5.0
  }'
```

---

## Option 2: Docker Deployment (Recommended)

### 2.1 Build Docker Image
```bash
cd ml-housing-prediction

# Build the image
docker build -t ml-housing-api:latest .
```

### 2.2 Run Container
```bash
# Run the container
docker run -d \
  --name ml-api \
  -p 5000:5000 \
  ml-housing-api:latest
```

### 2.3 Test Container
```bash
# Check status
docker ps

# View logs
docker logs ml-api

# Test API
curl http://localhost:5000/health
```

### 2.4 Using Docker Compose (Multiple Containers)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f ml-api

# Stop services
docker-compose down
```

### 2.5 Push to Docker Registry
```bash
# Login to Docker Hub
docker login

# Tag image
docker tag ml-housing-api:latest yourusername/ml-housing-api:latest

# Push
docker push yourusername/ml-housing-api:latest
```

---

## Option 3: AWS Deployment

### 3.1 Deploy to EC2

#### Create EC2 Instance
1. Go to AWS Console → EC2 → Instances
2. Click "Launch Instance"
3. Select Ubuntu 22.04 LTS
4. Choose instance type: `t3.micro` (free tier eligible)
5. Configure security group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80)
   - Allow HTTPS (port 443)
6. Launch and download key pair

#### Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/yourusername/ml-housing-prediction.git
cd ml-housing-prediction

# Build and run
docker-compose up -d
```

#### Setup Domain (Optional)
1. Point your domain to EC2 IP
2. Install Nginx reverse proxy
3. Configure SSL with Let's Encrypt

### 3.2 Deploy to AWS SageMaker

1. Go to SageMaker → Notebooks
2. Create notebook instance
3. Upload your code
4. Train model in notebook
5. Deploy endpoint
6. Get inference URL

```python
import boto3
import sagemaker

session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Train and deploy
endpoint_name = 'ml-housing-prediction'
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium'
)
```

### 3.3 Deploy to AWS Lambda

#### Package Function
```bash
# Install serverless
npm install -g serverless

# Create serverless project
serverless create --template aws-python3 --path ml-housing

# Copy app.py and models to project
# Update serverless.yml
```

#### Deploy
```bash
serverless deploy
```

---

## Option 4: Google Cloud Deployment

### 4.1 Deploy to Cloud Run

#### Prerequisites
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Initialize
gcloud init
```

#### Deploy
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy ml-housing-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Gets URL like: `https://ml-housing-api-xxxxx.run.app`

#### Test Cloud Run
```bash
curl https://ml-housing-api-xxxxx.run.app/health
```

### 4.2 Deploy to Compute Engine

```bash
# Create VM
gcloud compute instances create ml-api-vm \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=e2-medium

# SSH into VM
gcloud compute ssh ml-api-vm

# Follow similar steps as EC2 deployment
```

---

## Option 5: Azure Deployment

### 5.1 Deploy to Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name ml-housing --location eastus

# Build and push to Azure Container Registry
az acr create --resource-group ml-housing --name mlhousing --sku Basic

# Build image
az acr build --registry mlhousing --image ml-housing-api:latest .

# Deploy to Container Instances
az container create \
  --resource-group ml-housing \
  --name ml-api \
  --image mlhousing.azurecr.io/ml-housing-api:latest \
  --ports 5000 \
  --environment-variables FLASK_ENV=production
```

### 5.2 Deploy to Azure App Service

```bash
# Create App Service Plan
az appservice plan create \
  --name ml-housing-plan \
  --resource-group ml-housing \
  --sku FREE --is-linux

# Create Web App
az webapp create \
  --resource-group ml-housing \
  --plan ml-housing-plan \
  --name ml-housing-api \
  --deployment-container-image-name-user mlhousing.azurecr.io/ml-housing-api:latest
```

---

## Option 6: Heroku Deployment

### 6.1 Setup
```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login
```

### 6.2 Create Procfile
```
web: gunicorn app:app
```

### 6.3 Deploy
```bash
# Create Heroku app
heroku create ml-housing-api

# Deploy code
git push heroku main

# View logs
heroku logs --tail
```

App runs at: `https://ml-housing-api.herokuapp.com`

---

## Option 7: Kubernetes Deployment (Advanced)

### Prerequisites
- Kubernetes cluster (Minikube, EKS, GKE, or AKS)
- kubectl installed

### 7.1 Create Kubernetes Manifests

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-housing-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-housing-api
  template:
    metadata:
      labels:
        app: ml-housing-api
    spec:
      containers:
      - name: api
        image: ml-housing-api:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ml-housing-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
  selector:
    app: ml-housing-api
```

### 7.2 Deploy
```bash
# Create namespace
kubectl create namespace ml-housing

# Apply manifests
kubectl apply -f deployment.yaml -n ml-housing
kubectl apply -f service.yaml -n ml-housing

# Check deployment
kubectl get deployments -n ml-housing
kubectl get pods -n ml-housing
kubectl get svc -n ml-housing

# Port forward (for testing)
kubectl port-forward svc/ml-housing-service 5000:80 -n ml-housing
```

---

## Monitoring & Maintenance

### Health Checks
```bash
# Regular health check
curl -s https://your-api-domain/health | jq .

# Monitor response time
time curl https://your-api-domain/health
```

### Logging
```bash
# Docker
docker logs -f ml-api

# Cloud services usually provide log dashboards
```

### Scaling
- **Horizontal Scaling**: Add more instances behind load balancer
- **Vertical Scaling**: Increase instance memory/CPU
- **Auto-scaling**: Configure based on metrics

### Updating
```bash
# Pull latest code
git pull origin main

# Rebuild Docker image
docker build -t ml-housing-api:v2 .

# Test locally
docker run -p 5000:5000 ml-housing-api:v2

# Deploy
docker push ml-housing-api:v2
# Or redeploy your cloud service
```

---

## Cost Estimation

| Platform | Instance Type | Estimated Monthly Cost |
|----------|--------------|----------------------|
| **AWS EC2** | t3.micro | $10-15 (free first year) |
| **Google Cloud Run** | On-demand | $0.40 + $0.50/M requests |
| **Azure Container Instances** | Standard | $25-50 |
| **Heroku** | Free dyno | $0 (limited) |
| **Heroku** | Basic dyno | $7/month |

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Docker Issues
```bash
# Clear images and containers
docker system prune -a

# Rebuild from scratch
docker build --no-cache -t ml-housing-api:latest .
```

### Model Not Found
```bash
# Ensure models directory is copied in Dockerfile
# Check file permissions
ls -la models/
```

### Memory Issues
```bash
# Increase Docker memory limit
docker run -m 2g -p 5000:5000 ml-housing-api:latest
```

---

## Production Checklist

- ✅ Models are trained and saved
- ✅ Environment variables configured
- ✅ Logging is enabled
- ✅ Error handling in place
- ✅ Rate limiting configured
- ✅ HTTPS/SSL enabled
- ✅ Monitoring set up
- ✅ Auto-scaling configured
- ✅ Backup and recovery plan
- ✅ Documentation updated

---

## Next Steps

1. Choose your deployment platform
2. Follow the specific guide above
3. Test all endpoints
4. Set up monitoring
5. Configure auto-scaling
6. Set up CI/CD pipeline
7. Plan for model updates

For questions or issues, check the main README.md
