"""
Safe Zone Recommendation System
This module finds the nearest safe zones using the Haversine formula.
"""

import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth using the Haversine formula.
    
    Parameters:
    -----------
    lat1, lon1 : float
        Latitude and longitude of first point in decimal degrees
    lat2, lon2 : float
        Latitude and longitude of second point in decimal degrees
    
    Returns:
    --------
    float
        Distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert coordinates to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    
    return distance

def find_nearest_safe_zones(user_lat, user_lon, safe_zones_path='data/safe_zones.csv', n_zones=3):
    """
    Find the nearest safe zones to the user's location.
    
    Parameters:
    -----------
    user_lat : float
        User's latitude
    user_lon : float
        User's longitude
    safe_zones_path : str
        Path to safe zones CSV file
    n_zones : int
        Number of nearest safe zones to return
    
    Returns:
    --------
    list
        List of dictionaries containing safe zone information with distances
    """
    # Load safe zones data
    safe_zones_df = pd.read_csv(safe_zones_path)
    
    # Calculate distances to all safe zones
    distances = []
    for idx, zone in safe_zones_df.iterrows():
        distance = haversine_distance(
            user_lat, user_lon,
            zone['latitude'], zone['longitude']
        )
        distances.append(distance)
    
    # Add distances to dataframe
    safe_zones_df['distance_km'] = distances
    
    # Sort by distance and get top n zones
    nearest_zones = safe_zones_df.nsmallest(n_zones, 'distance_km')
    
    # Convert to list of dictionaries
    result = []
    for idx, zone in nearest_zones.iterrows():
        result.append({
            'name': zone['name'],
            'latitude': zone['latitude'],
            'longitude': zone['longitude'],
            'distance_km': round(zone['distance_km'], 2)
        })
    
    return result

def display_safe_zones(user_lat, user_lon, safe_zones, risk_level='Unknown'):
    """
    Display safe zone recommendations in a formatted way.
    
    Parameters:
    -----------
    user_lat : float
        User's latitude
    user_lon : float
        User's longitude
    safe_zones : list
        List of nearest safe zones
    risk_level : str
        Predicted flood risk level
    """
    print("\n" + "="*60)
    print("🏥 NEAREST SAFE ZONES RECOMMENDATION")
    print("="*60)
    
    print(f"\n📍 Your Location:")
    print(f"   Latitude: {user_lat}")
    print(f"   Longitude: {user_lon}")
    
    if risk_level != 'Unknown':
        print(f"\n⚠️  Flood Risk Level: {risk_level}")
    
    print(f"\n🚨 {len(safe_zones)} Nearest Safe Zones:\n")
    
    for i, zone in enumerate(safe_zones, 1):
        print(f"{i}. {zone['name']}")
        print(f"   📍 Location: ({zone['latitude']}, {zone['longitude']})")
        print(f"   📏 Distance: {zone['distance_km']} km")
        print()
    
    print("="*60)

def get_safe_zone_recommendations(user_lat, user_lon, risk_level='Unknown', 
                                  safe_zones_path='data/safe_zones.csv'):
    """
    Get safe zone recommendations with distance information.
    
    Parameters:
    -----------
    user_lat : float
        User's latitude
    user_lon : float
        User's longitude
    risk_level : str
        Predicted flood risk level
    safe_zones_path : str
        Path to safe zones CSV file
    
    Returns:
    --------
    dict
        Dictionary containing user location, risk level, and safe zones
    """
    # Determine number of zones based on risk level
    if risk_level == 'High':
        n_zones = 5
    elif risk_level == 'Medium':
        n_zones = 3
    else:
        n_zones = 2
    
    # Find nearest safe zones
    safe_zones = find_nearest_safe_zones(user_lat, user_lon, safe_zones_path, n_zones)
    
    result = {
        'user_location': {
            'latitude': user_lat,
            'longitude': user_lon
        },
        'risk_level': risk_level,
        'safe_zones': safe_zones
    }
    
    return result

if __name__ == '__main__':
    # Test safe zone recommendation
    print("🏥 Testing Safe Zone Recommendation System\n")
    
    # Test case 1: Location near Mumbai
    print("Test Case 1: User near Mumbai")
    user_lat = 19.1
    user_lon = 72.9
    
    safe_zones = find_nearest_safe_zones(user_lat, user_lon, n_zones=3)
    display_safe_zones(user_lat, user_lon, safe_zones, risk_level='High')
    
    # Test case 2: Location near Delhi
    print("\n\nTest Case 2: User near Delhi")
    user_lat = 28.7
    user_lon = 77.1
    
    safe_zones = find_nearest_safe_zones(user_lat, user_lon, n_zones=3)
    display_safe_zones(user_lat, user_lon, safe_zones, risk_level='Medium')
