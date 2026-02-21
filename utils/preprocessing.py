"""
Data Preprocessing Utilities for Flood Risk Prediction
This module handles data loading, cleaning, and preprocessing.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

class FloodDataPreprocessor:
    """
    Preprocessor class for flood risk prediction data.
    Handles data loading, cleaning, encoding, and scaling.
    """
    
    def __init__(self, data_path='data/flood_data.csv'):
        """
        Initialize the preprocessor.
        
        Parameters:
        -----------
        data_path : str
            Path to the flood dataset CSV file
        """
        self.data_path = data_path
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self):
        """Load dataset from CSV file."""
        print("📂 Loading dataset...")
        self.df = pd.read_csv(self.data_path)
        print(f"✅ Dataset loaded successfully!")
        print(f"📊 Shape: {self.df.shape}")
        print(f"\n📋 First few rows:")
        print(self.df.head())
        return self.df
    
    def check_missing_values(self):
        """Check and report missing values in the dataset."""
        print("\n🔍 Checking for missing values...")
        missing = self.df.isnull().sum()
        if missing.sum() == 0:
            print("✅ No missing values found!")
        else:
            print("⚠️  Missing values found:")
            print(missing[missing > 0])
        return missing
    
    def handle_missing_values(self):
        """Handle missing values by filling with mean for numerical columns."""
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print("🔧 Handling missing values...")
            # Fill numerical columns with mean
            numerical_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].mean())
            print("✅ Missing values handled!")
        return self.df
    
    def prepare_features(self, feature_columns=None):
        """
        Prepare features and target variable.
        
        Parameters:
        -----------
        feature_columns : list, optional
            List of column names to use as features.
            If None, uses default feature set.
        
        Returns:
        --------
        X : array
            Feature matrix
        y : array
            Encoded target labels
        """
        if feature_columns is None:
            # Default features (excluding latitude, longitude for prediction)
            feature_columns = ['rainfall', 'temperature', 'humidity', 'river_level']
        
        print(f"\n🎯 Preparing features: {feature_columns}")
        
        # Extract features
        X = self.df[feature_columns].values
        
        # Encode target labels (Low=0, Medium=1, High=2)
        y = self.label_encoder.fit_transform(self.df['flood_risk'])
        
        print(f"✅ Features shape: {X.shape}")
        print(f"✅ Target shape: {y.shape}")
        print(f"📊 Label encoding: {dict(zip(self.label_encoder.classes_, self.label_encoder.transform(self.label_encoder.classes_)))}")
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets.
        
        Parameters:
        -----------
        X : array
            Feature matrix
        y : array
            Target labels
        test_size : float
            Proportion of dataset to include in test split
        random_state : int
            Random seed for reproducibility
        
        Returns:
        --------
        X_train, X_test, y_train, y_test
        """
        print(f"\n📊 Splitting data (test_size={test_size})...")
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"✅ Training set: {self.X_train.shape}")
        print(f"✅ Testing set: {self.X_test.shape}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def scale_features(self, X_train, X_test):
        """
        Scale features using StandardScaler.
        
        Parameters:
        -----------
        X_train : array
            Training features
        X_test : array
            Testing features
        
        Returns:
        --------
        X_train_scaled, X_test_scaled
        """
        print("\n⚖️  Scaling features...")
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("✅ Features scaled successfully!")
        
        return X_train_scaled, X_test_scaled
    
    def save_preprocessors(self, scaler_path='models/scaler.pkl', encoder_path='models/label_encoder.pkl'):
        """
        Save scaler and label encoder for later use.
        
        Parameters:
        -----------
        scaler_path : str
            Path to save the scaler
        encoder_path : str
            Path to save the label encoder
        """
        print("\n💾 Saving preprocessors...")
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        print(f"✅ Scaler saved to {scaler_path}")
        print(f"✅ Label encoder saved to {encoder_path}")
    
    def preprocess_pipeline(self):
        """
        Execute complete preprocessing pipeline.
        
        Returns:
        --------
        X_train_scaled, X_test_scaled, y_train, y_test
        """
        print("🚀 Starting preprocessing pipeline...\n")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Check and handle missing values
        self.check_missing_values()
        self.handle_missing_values()
        
        # Prepare features
        X, y = self.prepare_features()
        
        # Split data
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        # Save preprocessors
        self.save_preprocessors()
        
        print("\n" + "="*60)
        print("✨ Preprocessing pipeline complete!")
        
        return X_train_scaled, X_test_scaled, y_train, y_test

if __name__ == '__main__':
    # Test preprocessing pipeline
    preprocessor = FloodDataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline()
