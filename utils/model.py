"""
Deep Learning Model for Flood Risk Prediction
This module defines the neural network architecture using TensorFlow/Keras.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np

def build_flood_model(input_shape=4, num_classes=3):
    """
    Build a deep learning model for flood risk classification.
    
    Architecture:
    - Input layer (4 features)
    - Dense layer (64 neurons, ReLU activation)
    - Dropout layer (0.3)
    - Dense layer (32 neurons, ReLU activation)
    - Dropout layer (0.2)
    - Dense layer (16 neurons, ReLU activation)
    - Output layer (3 classes, Softmax activation)
    
    Parameters:
    -----------
    input_shape : int
        Number of input features
    num_classes : int
        Number of output classes (Low, Medium, High)
    
    Returns:
    --------
    model : keras.Model
        Compiled Keras model
    """
    print("🏗️  Building flood risk prediction model...\n")
    
    model = models.Sequential([
        # Input layer
        layers.Input(shape=(input_shape,)),
        
        # First hidden layer with dropout
        layers.Dense(64, activation='relu', name='dense_1'),
        layers.Dropout(0.3, name='dropout_1'),
        
        # Second hidden layer with dropout
        layers.Dense(32, activation='relu', name='dense_2'),
        layers.Dropout(0.2, name='dropout_2'),
        
        # Third hidden layer
        layers.Dense(16, activation='relu', name='dense_3'),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax', name='output')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("✅ Model built successfully!\n")
    print("📋 Model Summary:")
    print("="*60)
    model.summary()
    print("="*60)
    
    return model

def get_callbacks(model_save_path='models/flood_model.h5'):
    """
    Define callbacks for model training.
    
    Parameters:
    -----------
    model_save_path : str
        Path to save the best model
    
    Returns:
    --------
    list
        List of Keras callbacks
    """
    callbacks = [
        # Early stopping to prevent overfitting
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Save best model
        ModelCheckpoint(
            model_save_path,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    return callbacks

def load_model(model_path='models/flood_model.h5'):
    """
    Load a saved Keras model.
    
    Parameters:
    -----------
    model_path : str
        Path to the saved model
    
    Returns:
    --------
    model : keras.Model
        Loaded Keras model
    """
    print(f"📂 Loading model from {model_path}...")
    model = keras.models.load_model(model_path)
    print("✅ Model loaded successfully!")
    return model

if __name__ == '__main__':
    # Test model building
    model = build_flood_model()
    print("\n✨ Model architecture created successfully!")
