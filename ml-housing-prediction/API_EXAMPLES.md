# API Usage Examples

This document provides practical examples of using the ML Housing Prediction API.

## Table of Contents
1. [Single Predictions](#single-predictions)
2. [Batch Predictions](#batch-predictions)
3. [Model Information](#model-information)
4. [Advanced Usage](#advanced-usage)
5. [Error Handling](#error-handling)

---

## Single Predictions

### Using cURL

#### Basic Prediction
```bash
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

**Response:**
```json
{
    "success": true,
    "input": {
        "square_feet": 2500,
        "num_bedrooms": 4,
        "num_bathrooms": 2.5,
        "year_built": 2010,
        "distance_to_city": 5.0
    },
    "prediction": {
        "price": 456789.50,
        "currency": "USD",
        "confidence": 0.9187,
        "model_rmse": 43215.50
    }
}
```

### Using Python

#### requests Library
```python
import requests
import json

# API endpoint
url = "http://localhost:5000/predict"

# House features
house_data = {
    "square_feet": 2500,
    "num_bedrooms": 4,
    "num_bathrooms": 2.5,
    "year_built": 2010,
    "distance_to_city": 5.0
}

# Make prediction
response = requests.post(url, json=house_data)
result = response.json()

if result['success']:
    price = result['prediction']['price']
    confidence = result['prediction']['confidence']
    print(f"Predicted Price: ${price:,.2f}")
    print(f"Model Confidence (R²): {confidence:.4f}")
else:
    print(f"Error: {result.get('error')}")
```

#### Using Python Requests with Session
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Setup retry strategy
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

def predict_house(house_data, timeout=5):
    """Make prediction with retry logic."""
    url = "http://localhost:5000/predict"
    try:
        response = session.post(url, json=house_data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
house = {
    "square_feet": 3000,
    "num_bedrooms": 5,
    "num_bathrooms": 3,
    "year_built": 2015,
    "distance_to_city": 3.0
}

result = predict_house(house)
if result:
    print(result['prediction'])
```

### Using JavaScript/Node.js

```javascript
// Fetch API
const houseData = {
    square_feet: 2500,
    num_bedrooms: 4,
    num_bathrooms: 2.5,
    year_built: 2010,
    distance_to_city: 5.0
};

fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(houseData)
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        const price = data.prediction.price;
        const confidence = data.prediction.confidence;
        console.log(`Predicted Price: $${price.toFixed(2)}`);
        console.log(`Confidence: ${(confidence * 100).toFixed(2)}%`);
    } else {
        console.error('Error:', data.error);
    }
})
.catch(error => console.error('Network error:', error));
```

### Using Axios (Node.js)
```javascript
const axios = require('axios');

async function predictHousePrice() {
    const houseData = {
        square_feet: 2500,
        num_bedrooms: 4,
        num_bathrooms: 2.5,
        year_built: 2010,
        distance_to_city: 5.0
    };

    try {
        const response = await axios.post(
            'http://localhost:5000/predict',
            houseData
        );
        console.log('Prediction:', response.data.prediction);
    } catch (error) {
        console.error('Error:', error.message);
    }
}

predictHousePrice();
```

---

## Batch Predictions

### Using cURL

```bash
curl -X POST http://localhost:5000/predict_batch \
  -H "Content-Type: application/json" \
  -d '[
    {
        "square_feet": 2000,
        "num_bedrooms": 3,
        "num_bathrooms": 2,
        "year_built": 2000,
        "distance_to_city": 10.0
    },
    {
        "square_feet": 3000,
        "num_bedrooms": 4,
        "num_bathrooms": 3,
        "year_built": 2015,
        "distance_to_city": 5.0
    },
    {
        "square_feet": 2500,
        "num_bedrooms": 4,
        "num_bathrooms": 2.5,
        "year_built": 2010,
        "distance_to_city": 5.0
    }
  ]'
```

### Using Python with Pandas

```python
import requests
import pandas as pd
import json

# Load data from CSV
df = pd.read_csv('batch_houses.csv')
houses = df.to_dict(orient='records')

# Make batch prediction
url = "http://localhost:5000/predict_batch"
response = requests.post(url, json=houses)
results = response.json()

# Parse results
if results['success']:
    predictions_df = pd.DataFrame(results['predictions'])
    predictions_df['predicted_price'] = predictions_df['predicted_price'].apply(lambda x: f"${x:,.2f}")
    print(predictions_df)
else:
    print(f"Error: {results['error']}")
```

### Processing Large Datasets

```python
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

def predict_batch_chunk(batch):
    """Predict for a chunk of data."""
    url = "http://localhost:5000/predict_batch"
    response = requests.post(url, json=batch)
    return response.json()

def predict_large_dataset(csv_file, chunk_size=100):
    """Process large CSV in chunks."""
    df = pd.read_csv(csv_file)
    
    # Split into chunks
    chunks = [df[i:i+chunk_size].to_dict(orient='records') 
              for i in range(0, len(df), chunk_size)]
    
    all_predictions = []
    
    # Process chunks concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(predict_batch_chunk, chunks)
        
    for result in results:
        if result['success']:
            all_predictions.extend(result['predictions'])
        else:
            print(f"Error: {result['error']}")
    
    return pd.DataFrame(all_predictions)

# Example usage
start = time.time()
predictions = predict_large_dataset('large_dataset.csv', chunk_size=100)
elapsed = time.time() - start
print(f"Processed {len(predictions)} records in {elapsed:.2f}s")
```

---

## Model Information

### Get Model Info
```bash
curl http://localhost:5000/model_info | jq .
```

**Response:**
```json
{
    "success": true,
    "model_type": "Linear Regression",
    "features": [
        "square_feet",
        "num_bedrooms",
        "num_bathrooms",
        "year_built",
        "distance_to_city"
    ],
    "coefficients": {
        "square_feet": 100.25,
        "num_bedrooms": 50000.10,
        "num_bathrooms": 30000.50,
        "year_built": 1000.75,
        "distance_to_city": -500.20
    },
    "intercept": 150000.00,
    "performance": {
        "train": {
            "mse": 2122662500.0,
            "rmse": 46070.32,
            "mae": 35987.21,
            "r2": 0.9234
        },
        "test": {
            "mse": 1866975156.25,
            "rmse": 43215.50,
            "mae": 32847.30,
            "r2": 0.9187
        }
    }
}
```

### Understanding Coefficients

```python
# The model formula
price = intercept + (square_feet * 100.25) + (bedrooms * 50000) + ...

# Example
intercept = 150000
square_feet_coef = 100.25
bedrooms_coef = 50000.10

# For a 2500 sqft, 4-bedroom house
price = 150000 + (2500 * 100.25) + (4 * 50000.10)
price = 150000 + 250625 + 200000.40
price = $600,625.40
```

---

## Advanced Usage

### Create Prediction Client Class

```python
class MLHousingClient:
    """Client for ML Housing Prediction API."""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        
    def health_check(self):
        """Check API health."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def predict(self, house_data):
        """Make single prediction."""
        response = requests.post(
            f"{self.base_url}/predict",
            json=house_data
        )
        return response.json()
    
    def predict_batch(self, houses):
        """Make batch predictions."""
        response = requests.post(
            f"{self.base_url}/predict_batch",
            json=houses
        )
        return response.json()
    
    def get_model_info(self):
        """Get model information."""
        response = requests.get(f"{self.base_url}/model_info")
        return response.json()
    
    def predict_with_interpretation(self, house_data):
        """Predict and interpret results."""
        # Get prediction
        prediction = self.predict(house_data)
        
        # Get model info
        model_info = self.get_model_info()
        
        if prediction['success']:
            price = prediction['prediction']['price']
            confidence = prediction['prediction']['confidence']
            rmse = prediction['prediction']['model_rmse']
            
            # Calculate confidence interval
            lower_bound = price - (1.96 * rmse)
            upper_bound = price + (1.96 * rmse)
            
            return {
                'predicted_price': price,
                'confidence_level': confidence,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'explanation': self._explain_prediction(
                    house_data, model_info['coefficients']
                )
            }
    
    def _explain_prediction(self, house_data, coefficients):
        """Provide explanation for prediction."""
        explanation = "Price breakdown:\n"
        total = 0
        
        for feature, value in house_data.items():
            if feature in coefficients:
                contribution = value * coefficients[feature]
                total += contribution
                explanation += f"  {feature}: {value} × {coefficients[feature]:.2f} = ${contribution:,.2f}\n"
        
        return explanation

# Usage
client = MLHousingClient()

# Check API
print(client.health_check())

# Make prediction
house = {
    "square_feet": 2500,
    "num_bedrooms": 4,
    "num_bathrooms": 2.5,
    "year_built": 2010,
    "distance_to_city": 5.0
}

result = client.predict_with_interpretation(house)
print(f"Predicted Price: ${result['predicted_price']:,.2f}")
print(f"95% Confidence Interval: ${result['lower_bound']:,.2f} - ${result['upper_bound']:,.2f}")
print(result['explanation'])
```

### Error Handling & Retry Logic

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from typing import Optional, Dict, Any

class RobustMLClient:
    """ML client with retry logic and error handling."""
    
    def __init__(self, base_url="http://localhost:5000", max_retries=3):
        self.base_url = base_url
        self.max_retries = max_retries
        self.session = self._create_session()
    
    def _create_session(self):
        """Create requests session with retry strategy."""
        session = requests.Session()
        retry = Retry(
            total=self.max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def predict(self, house_data: Dict[str, Any], 
                timeout: int = 10) -> Optional[Dict]:
        """Make prediction with error handling."""
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json=house_data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            print("Request timed out")
            return None
        except requests.exceptions.ConnectionError:
            print("Connection error - API might be down")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

# Usage with error handling
client = RobustMLClient()

for attempt in range(3):
    result = client.predict({
        "square_feet": 2500,
        "num_bedrooms": 4,
        "num_bathrooms": 2.5,
        "year_built": 2010,
        "distance_to_city": 5.0
    })
    
    if result:
        print("Prediction successful!")
        break
    else:
        print(f"Attempt {attempt + 1} failed, retrying...")
        time.sleep(2)
```

---

## Error Handling

### Common Errors & Solutions

#### Missing Fields Error
```json
{
    "error": "Missing fields: ['num_bedrooms', 'distance_to_city']"
}
```

**Solution:**
```python
required_fields = ['square_feet', 'num_bedrooms', 'num_bathrooms', 'year_built', 'distance_to_city']

house_data = {...}

missing = [f for f in required_fields if f not in house_data]
if missing:
    print(f"Missing: {missing}")
else:
    prediction = client.predict(house_data)
```

#### Model Not Found Error
```json
{
    "error": "Model not loaded"
}
```

**Solution:**
```bash
# Ensure model is trained
python -m src.train_model

# Check model files
ls -la models/
```

#### Invalid JSON Error
```json
{
    "error": "..."
}
```

**Solution:**
```python
import json

# Validate JSON
try:
    json.dumps(house_data)
    # Send to API
except json.JSONDecodeError:
    print("Invalid JSON format")
```

#### Rate Limiting (if implemented)
```json
{
    "error": "Rate limit exceeded"
}
```

**Solution:**
```python
import time
from collections import deque

class RateLimitedClient:
    def __init__(self, requests_per_second=10):
        self.requests_per_second = requests_per_second
        self.request_times = deque()
    
    def _wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()
        # Remove old requests outside the window
        while self.request_times and self.request_times[0] < now - 1:
            self.request_times.popleft()
        
        if len(self.request_times) >= self.requests_per_second:
            sleep_time = 1 - (now - self.request_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def predict(self, house_data):
        self._wait_if_needed()
        self.request_times.append(time.time())
        return client.predict(house_data)
```

---

## Performance Tips

1. **Batch Requests**: Use `/predict_batch` instead of multiple single predictions
2. **Connection Pooling**: Reuse HTTP connections
3. **Caching**: Cache model info since it doesn't change
4. **Async Requests**: Use libraries like `aiohttp` for concurrent requests

---

For more examples and support, refer to the main README.md
