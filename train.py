"""
Training Script for Flood Risk Prediction Model
This script trains the deep learning model and visualizes the results.
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from utils.generate_dataset import generate_flood_dataset, generate_safezones_dataset
from utils.preprocessing import FloodDataPreprocessor
from utils.model import build_flood_model, get_callbacks

def plot_training_history(history, save_path='models/training_history.png'):
    """
    Plot training history (accuracy and loss).
    
    Parameters:
    -----------
    history : keras.callbacks.History
        Training history object
    save_path : str
        Path to save the plot
    """
    print("\n📊 Plotting training history...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot accuracy
    axes[0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].legend(loc='lower right')
    axes[0].grid(True, alpha=0.3)
    
    # Plot loss
    axes[1].plot(history.history['loss'], label='Training Loss', linewidth=2)
    axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Training history plot saved to {save_path}")
    
    return fig

def train_model(epochs=50, batch_size=32):
    """
    Complete training pipeline for flood risk prediction model.
    
    Parameters:
    -----------
    epochs : int
        Number of training epochs
    batch_size : int
        Batch size for training
    
    Returns:
    --------
    model : keras.Model
        Trained model
    history : keras.callbacks.History
        Training history
    """
    print("🌊 FLOOD RISK PREDICTION MODEL TRAINING")
    print("="*60)
    
    # Step 1: Check if datasets exist, if not generate them
    if not os.path.exists('data/flood_data.csv'):
        print("\n📊 Dataset not found. Generating synthetic dataset...\n")
        generate_flood_dataset()
        generate_safezones_dataset()
    
    # Step 2: Preprocess data
    print("\n" + "="*60)
    print("STEP 1: DATA PREPROCESSING")
    print("="*60)
    
    preprocessor = FloodDataPreprocessor('data/flood_data.csv')
    X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline()
    
    # Step 3: Build model
    print("\n" + "="*60)
    print("STEP 2: MODEL BUILDING")
    print("="*60)
    
    model = build_flood_model(input_shape=X_train.shape[1], num_classes=3)
    
    # Step 4: Train model
    print("\n" + "="*60)
    print("STEP 3: MODEL TRAINING")
    print("="*60)
    print(f"🏋️  Training for {epochs} epochs with batch size {batch_size}...\n")
    
    callbacks = get_callbacks('models/flood_model.h5')
    
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )
    
    # Step 5: Evaluate model
    print("\n" + "="*60)
    print("STEP 4: MODEL EVALUATION")
    print("="*60)
    
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"\n📊 Final Training Results:")
    print(f"   ✅ Test Loss: {test_loss:.4f}")
    print(f"   ✅ Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Step 6: Plot training history
    print("\n" + "="*60)
    print("STEP 5: VISUALIZATION")
    print("="*60)
    
    plot_training_history(history, 'models/training_history.png')
    
    # Step 7: Summary
    print("\n" + "="*60)
    print("✨ TRAINING COMPLETE!")
    print("="*60)
    print(f"📁 Model saved to: models/flood_model.h5")
    print(f"📁 Scaler saved to: models/scaler.pkl")
    print(f"📁 Label encoder saved to: models/label_encoder.pkl")
    print(f"📁 Training plot saved to: models/training_history.png")
    print("="*60)
    
    return model, history

if __name__ == '__main__':
    # Train the model
    model, history = train_model(epochs=50, batch_size=32)
