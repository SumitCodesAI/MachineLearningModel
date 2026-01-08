"""
Generate synthetic housing dataset for training the linear regression model.
This script creates a realistic housing dataset with features like square feet, rooms, etc.
"""

import pandas as pd
import numpy as np

def generate_housing_data(n_samples=200, random_state=42):
    """
    Generate synthetic housing data.
    
    Features:
    - square_feet: House area in square feet
    - num_bedrooms: Number of bedrooms
    - num_bathrooms: Number of bathrooms
    - year_built: Year the house was built
    - distance_to_city: Distance to city center in miles
    - price: House price in dollars (target variable)
    """
    np.random.seed(random_state)
    
    # Generate features
    square_feet = np.random.uniform(1000, 5000, n_samples)
    num_bedrooms = np.random.randint(1, 6, n_samples)
    num_bathrooms = np.random.uniform(1, 4, n_samples)
    year_built = np.random.randint(1980, 2024, n_samples)
    distance_to_city = np.random.uniform(0.5, 50, n_samples)
    
    # Generate price based on features (with some realistic relationships)
    # Price = base + (100 * sqft) + (50k * bedrooms) + (30k * bathrooms) - (500 * distance) + (1000 * (year-1980))
    base_price = 150000
    price = (
        base_price +
        100 * square_feet +
        50000 * num_bedrooms +
        30000 * num_bathrooms -
        500 * distance_to_city +
        1000 * (year_built - 1980) +
        np.random.normal(0, 50000, n_samples)  # Add some noise
    )
    
    # Create DataFrame
    df = pd.DataFrame({
        'square_feet': square_feet,
        'num_bedrooms': num_bedrooms,
        'num_bathrooms': num_bathrooms,
        'year_built': year_built,
        'distance_to_city': distance_to_city,
        'price': price
    })
    
    return df

if __name__ == "__main__":
    import os
    # Generate and save data
    data = generate_housing_data()
    # Save to current directory
    output_path = os.path.join(os.path.dirname(__file__), 'house_data.csv')
    data.to_csv(output_path, index=False)
    print("✓ Dataset generated successfully!")
    print(f"Saved to: {output_path}")
    print(f"Shape: {data.shape}")
    print("\nFirst few rows:")
    print(data.head())
    print("\nDataset statistics:")
    print(data.describe())
