"""
Data Preprocessing Module
This module handles loading, exploring, and preparing data for model training.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles all data preprocessing tasks."""
    
    def __init__(self, filepath):
        """
        Initialize the DataProcessor.
        
        Args:
            filepath: Path to the CSV file
        """
        self.filepath = filepath
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        
    def load_data(self):
        """Load data from CSV file."""
        logger.info(f"Loading data from {self.filepath}")
        self.df = pd.read_csv(self.filepath)
        logger.info(f"Data loaded. Shape: {self.df.shape}")
        return self.df
    
    def explore_data(self):
        """Explore and display data information."""
        logger.info("=== Data Exploration ===")
        print("\nDataset Shape:", self.df.shape)
        print("\nFirst few rows:")
        print(self.df.head())
        print("\nData Types:")
        print(self.df.dtypes)
        print("\nMissing Values:")
        print(self.df.isnull().sum())
        print("\nStatistical Summary:")
        print(self.df.describe())
        print("\nCorrelation with Price:")
        print(self.df.corr()['price'].sort_values(ascending=False))
        return self.df.describe()
    
    def handle_missing_values(self):
        """Handle missing values in the dataset."""
        logger.info("Handling missing values")
        # For numerical columns, fill with median
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna(self.df[col].median(), inplace=True)
        logger.info("Missing values handled")
        return self.df
    
    def remove_outliers(self, columns=None, threshold=3):
        """
        Remove outliers using z-score method.
        
        Args:
            columns: List of columns to check for outliers
            threshold: Z-score threshold (default: 3)
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns
        
        logger.info(f"Removing outliers (threshold={threshold})")
        initial_rows = len(self.df)
        
        for col in columns:
            z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
            self.df = self.df[z_scores < threshold]
        
        removed_rows = initial_rows - len(self.df)
        logger.info(f"Removed {removed_rows} outlier rows")
        return self.df
    
    def prepare_train_test_split(self, test_size=0.2, random_state=42):
        """
        Split data into train and test sets.
        
        Args:
            test_size: Proportion of test set
            random_state: Random state for reproducibility
        """
        logger.info(f"Splitting data: {(1-test_size)*100:.0f}% train, {test_size*100:.0f}% test")
        
        # Separate features and target
        X = self.df.drop('price', axis=1)
        y = self.df['price']
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        logger.info(f"Train set size: {len(self.X_train)}")
        logger.info(f"Test set size: {len(self.X_test)}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def scale_features(self):
        """Standardize features using StandardScaler."""
        logger.info("Scaling features")
        
        # Fit scaler on training data
        self.X_train = self.scaler.fit_transform(self.X_train)
        # Transform test data
        self.X_test = self.scaler.transform(self.X_test)
        
        logger.info("Features scaled successfully")
        return self.X_train, self.X_test
    
    def get_processed_data(self):
        """Return the processed train/test split."""
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_feature_names(self):
        """Get feature names after preprocessing."""
        return list(self.df.drop('price', axis=1).columns)

def preprocess_pipeline(filepath, test_size=0.2):
    """
    Complete preprocessing pipeline.
    
    Args:
        filepath: Path to the CSV file
        test_size: Proportion of test set
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, processor)
    """
    processor = DataProcessor(filepath)
    processor.load_data()
    processor.explore_data()
    processor.handle_missing_values()
    processor.remove_outliers()
    processor.prepare_train_test_split(test_size=test_size)
    processor.scale_features()
    
    return processor.get_processed_data() + (processor,)
