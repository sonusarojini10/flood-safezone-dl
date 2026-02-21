"""
Flask Backend for Flood Risk Prediction System
This application provides API endpoints for flood prediction and safe zone recommendations.
"""

from flask import Flask, render_template, request, jsonify
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predict import predict_flood_risk
from utils.safezone import get_safe_zone_recommendations

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

@app.route('/')
def home():
    """
    Home page route.
    Renders the main interface for flood risk prediction.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Flood risk prediction endpoint.
    
    Expected JSON input:
    {
        "rainfall": float,
        "temperature": float,
        "humidity": float,
        "river_level": float
    }
    
    Returns:
    {
        "risk_level": string,
        "confidence": float,
        "probabilities": dict,
        "input_parameters": dict
    }
    """
    try:
        # Get input data from request
        data = request.get_json()
        
        # Extract parameters
        rainfall = float(data.get('rainfall', 0))
        temperature = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        river_level = float(data.get('river_level', 0))
        
        # Validate inputs
        if rainfall < 0 or temperature < -50 or temperature > 60:
            return jsonify({'error': 'Invalid input values'}), 400
        
        if humidity < 0 or humidity > 100 or river_level < 0:
            return jsonify({'error': 'Invalid input values'}), 400
        
        # Make prediction
        result = predict_flood_risk(rainfall, temperature, humidity, river_level)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/safezone', methods=['POST'])
def safezone():
    """
    Safe zone recommendation endpoint.
    
    Expected JSON input:
    {
        "latitude": float,
        "longitude": float,
        "risk_level": string (optional)
    }
    
    Returns:
    {
        "user_location": dict,
        "risk_level": string,
        "safe_zones": list
    }
    """
    try:
        # Get input data from request
        data = request.get_json()
        
        # Extract parameters
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        risk_level = data.get('risk_level', 'Unknown')
        
        # Validate inputs
        if latitude < -90 or latitude > 90:
            return jsonify({'error': 'Invalid latitude'}), 400
        
        if longitude < -180 or longitude > 180:
            return jsonify({'error': 'Invalid longitude'}), 400
        
        # Get safe zone recommendations
        result = get_safe_zone_recommendations(latitude, longitude, risk_level)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict-and-recommend', methods=['POST'])
def predict_and_recommend():
    """
    Combined endpoint for flood prediction and safe zone recommendation.
    
    Expected JSON input:
    {
        "rainfall": float,
        "temperature": float,
        "humidity": float,
        "river_level": float,
        "latitude": float,
        "longitude": float
    }
    
    Returns:
    {
        "prediction": dict,
        "safe_zones": dict
    }
    """
    try:
        # Get input data from request
        data = request.get_json()
        
        # Extract parameters for prediction
        rainfall = float(data.get('rainfall', 0))
        temperature = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        river_level = float(data.get('river_level', 0))
        
        # Extract location parameters
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        
        # Make flood risk prediction
        prediction_result = predict_flood_risk(rainfall, temperature, humidity, river_level)
        
        # Get safe zone recommendations based on predicted risk level
        safezone_result = get_safe_zone_recommendations(
            latitude, longitude, 
            risk_level=prediction_result['risk_level']
        )
        
        # Combine results
        combined_result = {
            'prediction': prediction_result,
            'safe_zones': safezone_result
        }
        
        return jsonify(combined_result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Check if model exists
    if not os.path.exists('models/flood_model.h5'):
        print("⚠️  Warning: Model file not found!")
        print("Please run 'python train.py' first to train the model.")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🌊 FLOOD RISK PREDICTION SYSTEM")
    print("="*60)
    print("\n🚀 Starting Flask server...")
    print("📍 Access the application at: http://localhost:5000")
    print("="*60 + "\n")
    
    # Run Flask app
    # Note: Set debug=False in production for security
    app.run(debug=False, host='0.0.0.0', port=5000)
