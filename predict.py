"""
Prediction Script for Flood Risk Assessment
This module handles flood risk prediction for new input data.
"""

import numpy as np
import pickle
from tensorflow import keras

def load_preprocessors(scaler_path='models/scaler.pkl', encoder_path='models/label_encoder.pkl'):
    """
    Load saved scaler and label encoder.
    
    Parameters:
    -----------
    scaler_path : str
        Path to the saved scaler
    encoder_path : str
        Path to the saved label encoder
    
    Returns:
    --------
    scaler, label_encoder
    """
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    with open(encoder_path, 'rb') as f:
        label_encoder = pickle.load(f)
    
    return scaler, label_encoder

def predict_flood_risk(rainfall, temperature, humidity, river_level, 
                       model_path='models/flood_model.h5',
                       scaler_path='models/scaler.pkl',
                       encoder_path='models/label_encoder.pkl'):
    """
    Predict flood risk level for given environmental parameters.
    
    Parameters:
    -----------
    rainfall : float
        Rainfall amount in mm
    temperature : float
        Temperature in Celsius
    humidity : float
        Humidity percentage
    river_level : float
        River water level in meters
    model_path : str
        Path to the trained model
    scaler_path : str
        Path to the saved scaler
    encoder_path : str
        Path to the saved label encoder
    
    Returns:
    --------
    dict
        Dictionary containing prediction results with risk level and probabilities
    """
    # Load model and preprocessors
    model = keras.models.load_model(model_path)
    scaler, label_encoder = load_preprocessors(scaler_path, encoder_path)
    
    # Prepare input data
    input_data = np.array([[rainfall, temperature, humidity, river_level]])
    
    # Scale the input
    input_scaled = scaler.transform(input_data)
    
    # Make prediction
    prediction_proba = model.predict(input_scaled, verbose=0)
    prediction_class = np.argmax(prediction_proba, axis=1)[0]
    
    # Decode prediction
    risk_level = label_encoder.inverse_transform([prediction_class])[0]
    
    # Get probabilities for each class
    probabilities = {
        label: float(prob) 
        for label, prob in zip(label_encoder.classes_, prediction_proba[0])
    }
    
    # Create result dictionary
    result = {
        'risk_level': risk_level,
        'confidence': float(prediction_proba[0][prediction_class]),
        'probabilities': probabilities,
        'input_parameters': {
            'rainfall': rainfall,
            'temperature': temperature,
            'humidity': humidity,
            'river_level': river_level
        }
    }
    
    return result

def display_prediction(result):
    """
    Display prediction results in a formatted way.
    
    Parameters:
    -----------
    result : dict
        Prediction result dictionary
    """
    print("\n" + "="*60)
    print("🌊 FLOOD RISK PREDICTION RESULT")
    print("="*60)
    
    print("\n📊 Input Parameters:")
    for param, value in result['input_parameters'].items():
        print(f"   • {param.replace('_', ' ').title()}: {value}")
    
    print(f"\n🎯 Predicted Risk Level: {result['risk_level']}")
    print(f"💯 Confidence: {result['confidence']*100:.2f}%")
    
    print("\n📈 Probabilities for Each Risk Level:")
    for level, prob in sorted(result['probabilities'].items()):
        bar_length = int(prob * 30)
        bar = "█" * bar_length
        print(f"   {level:8s}: {bar} {prob*100:.2f}%")
    
    print("="*60)

if __name__ == '__main__':
    # Example prediction
    print("🌊 Testing Flood Risk Prediction\n")
    
    # Test case 1: High risk scenario
    print("Test Case 1: High Risk Scenario")
    result1 = predict_flood_risk(
        rainfall=250,
        temperature=32,
        humidity=90,
        river_level=12
    )
    display_prediction(result1)
    
    # Test case 2: Low risk scenario
    print("\n\nTest Case 2: Low Risk Scenario")
    result2 = predict_flood_risk(
        rainfall=20,
        temperature=25,
        humidity=60,
        river_level=3
    )
    display_prediction(result2)
    
    # Test case 3: Medium risk scenario
    print("\n\nTest Case 3: Medium Risk Scenario")
    result3 = predict_flood_risk(
        rainfall=120,
        temperature=28,
        humidity=75,
        river_level=6
    )
    display_prediction(result3)
