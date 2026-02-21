"""
Synthetic Dataset Generator for Flood Risk Prediction
This script generates synthetic data for training the flood prediction model.
"""

import pandas as pd
import numpy as np

def generate_flood_dataset(n_samples=5000, save_path='data/flood_data.csv'):
    """
    Generate synthetic flood risk dataset with environmental parameters.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
    save_path : str
        Path to save the CSV file
    
    Returns:
    --------
    pd.DataFrame
        Generated dataset
    """
    np.random.seed(42)
    
    # Generate features
    rainfall = np.random.uniform(0, 300, n_samples)  # mm
    temperature = np.random.uniform(15, 40, n_samples)  # Celsius
    humidity = np.random.uniform(30, 100, n_samples)  # percentage
    river_level = np.random.uniform(0, 15, n_samples)  # meters
    latitude = np.random.uniform(8.0, 37.0, n_samples)  # India latitude range
    longitude = np.random.uniform(68.0, 97.0, n_samples)  # India longitude range
    
    # Generate flood risk based on conditions
    flood_risk = []
    
    for i in range(n_samples):
        # Calculate risk score based on multiple factors
        risk_score = 0
        
        # Rainfall contribution
        if rainfall[i] > 200:
            risk_score += 3
        elif rainfall[i] > 100:
            risk_score += 2
        elif rainfall[i] > 50:
            risk_score += 1
        
        # River level contribution
        if river_level[i] > 10:
            risk_score += 3
        elif river_level[i] > 7:
            risk_score += 2
        elif river_level[i] > 4:
            risk_score += 1
        
        # Humidity contribution (high humidity + high rainfall = higher risk)
        if humidity[i] > 85 and rainfall[i] > 100:
            risk_score += 1
        
        # Temperature contribution (extreme temperature with high rainfall)
        if temperature[i] > 35 and rainfall[i] > 150:
            risk_score += 1
        
        # Classify based on risk score
        if risk_score >= 5:
            flood_risk.append('High')
        elif risk_score >= 3:
            flood_risk.append('Medium')
        else:
            flood_risk.append('Low')
    
    # Create DataFrame
    df = pd.DataFrame({
        'rainfall': rainfall,
        'temperature': temperature,
        'humidity': humidity,
        'river_level': river_level,
        'latitude': latitude,
        'longitude': longitude,
        'flood_risk': flood_risk
    })
    
    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"✅ Dataset saved to {save_path}")
    print(f"📊 Dataset shape: {df.shape}")
    print(f"\n📈 Flood Risk Distribution:")
    print(df['flood_risk'].value_counts())
    print(f"\n📋 Sample data:")
    print(df.head())
    
    return df

def generate_safezones_dataset(save_path='data/safe_zones.csv'):
    """
    Generate synthetic safe zones dataset with locations across India.
    
    Parameters:
    -----------
    save_path : str
        Path to save the CSV file
    
    Returns:
    --------
    pd.DataFrame
        Safe zones dataset
    """
    safe_zones = [
        {'name': 'Emergency Relief Center - Delhi', 'latitude': 28.6139, 'longitude': 77.2090},
        {'name': 'Flood Shelter - Mumbai', 'latitude': 19.0760, 'longitude': 72.8777},
        {'name': 'Safe Zone - Kolkata', 'latitude': 22.5726, 'longitude': 88.3639},
        {'name': 'Relief Camp - Chennai', 'latitude': 13.0827, 'longitude': 80.2707},
        {'name': 'Emergency Shelter - Bangalore', 'latitude': 12.9716, 'longitude': 77.5946},
        {'name': 'Safe Haven - Hyderabad', 'latitude': 17.3850, 'longitude': 78.4867},
        {'name': 'Relief Center - Pune', 'latitude': 18.5204, 'longitude': 73.8567},
        {'name': 'Flood Shelter - Ahmedabad', 'latitude': 23.0225, 'longitude': 72.5714},
        {'name': 'Safe Zone - Jaipur', 'latitude': 26.9124, 'longitude': 75.7873},
        {'name': 'Emergency Camp - Lucknow', 'latitude': 26.8467, 'longitude': 80.9462},
        {'name': 'Relief Center - Patna', 'latitude': 25.5941, 'longitude': 85.1376},
        {'name': 'Safe Haven - Bhopal', 'latitude': 23.2599, 'longitude': 77.4126},
        {'name': 'Flood Shelter - Guwahati', 'latitude': 26.1445, 'longitude': 91.7362},
        {'name': 'Emergency Zone - Kochi', 'latitude': 9.9312, 'longitude': 76.2673},
        {'name': 'Relief Camp - Chandigarh', 'latitude': 30.7333, 'longitude': 76.7794},
    ]
    
    df = pd.DataFrame(safe_zones)
    df.to_csv(save_path, index=False)
    print(f"\n✅ Safe zones dataset saved to {save_path}")
    print(f"📊 Total safe zones: {len(df)}")
    print(f"\n📋 Safe zones:")
    print(df)
    
    return df

if __name__ == '__main__':
    print("🌊 Generating Flood Risk Dataset...\n")
    flood_df = generate_flood_dataset()
    
    print("\n" + "="*60 + "\n")
    
    print("🏥 Generating Safe Zones Dataset...\n")
    safezones_df = generate_safezones_dataset()
    
    print("\n" + "="*60)
    print("✨ Dataset generation complete!")
