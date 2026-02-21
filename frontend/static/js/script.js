// Global variables
let map;
let userMarker;
let safeZoneMarkers = [];

// Get user's current location
function getLocation() {
    if (navigator.geolocation) {
        document.getElementById('loading').style.display = 'block';
        navigator.geolocation.getCurrentPosition(
            (position) => {
                document.getElementById('latitude').value = position.coords.latitude.toFixed(4);
                document.getElementById('longitude').value = position.coords.longitude.toFixed(4);
                document.getElementById('loading').style.display = 'none';
                showSuccess('Location retrieved successfully!');
            },
            (error) => {
                document.getElementById('loading').style.display = 'none';
                showError('Unable to retrieve location. Please enter manually.');
            }
        );
    } else {
        showError('Geolocation is not supported by your browser.');
    }
}

// Show success message
function showSuccess(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.style.display = 'block';
    errorDiv.style.background = '#dff0d8';
    errorDiv.style.borderColor = '#3c763d';
    document.getElementById('errorText').textContent = '✅ ' + message;
    document.getElementById('errorText').style.color = '#3c763d';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 3000);
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.style.display = 'block';
    errorDiv.style.background = '#fee';
    errorDiv.style.borderColor = '#c33';
    document.getElementById('errorText').textContent = '❌ ' + message;
    document.getElementById('errorText').style.color = '#c33';
}

// Initialize map
function initMap(userLat, userLon, safeZones) {
    // Remove existing map if any
    if (map) {
        map.remove();
    }

    // Create map centered on user location
    map = L.map('map').setView([userLat, userLon], 8);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);

    // Add user location marker
    const userIcon = L.divIcon({
        className: 'user-marker',
        html: '<div style="background: #667eea; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });

    userMarker = L.marker([userLat, userLon], { icon: userIcon })
        .addTo(map)
        .bindPopup('<b>Your Location</b>')
        .openPopup();

    // Add safe zone markers
    safeZoneMarkers = [];
    safeZones.forEach((zone, index) => {
        const zoneIcon = L.divIcon({
            className: 'safezone-marker',
            html: `<div style="background: #38ef7d; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">${index + 1}</div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });

        const marker = L.marker([zone.latitude, zone.longitude], { icon: zoneIcon })
            .addTo(map)
            .bindPopup(`<b>${zone.name}</b><br>Distance: ${zone.distance_km} km`);

        safeZoneMarkers.push(marker);
    });

    // Fit map to show all markers
    const group = L.featureGroup([userMarker, ...safeZoneMarkers]);
    map.fitBounds(group.getBounds().pad(0.1));
}

// Display probability bars
function displayProbabilities(probabilities) {
    const container = document.getElementById('probabilityBars');
    container.innerHTML = '';

    const levels = ['Low', 'Medium', 'High'];
    levels.forEach(level => {
        const prob = probabilities[level] || 0;
        const percentage = (prob * 100).toFixed(1);

        const item = document.createElement('div');
        item.className = 'probability-item';

        item.innerHTML = `
            <div class="probability-label">
                <span>${level} Risk</span>
                <span>${percentage}%</span>
            </div>
            <div class="probability-bar">
                <div class="probability-fill ${level.toLowerCase()}" style="width: ${percentage}%">
                    ${percentage > 10 ? percentage + '%' : ''}
                </div>
            </div>
        `;

        container.appendChild(item);
    });
}

// Display safe zones list
function displaySafeZones(safeZones) {
    const container = document.getElementById('safeZonesList');
    container.innerHTML = '';

    if (safeZones.length === 0) {
        container.innerHTML = '<p>No safe zones found in your area.</p>';
        return;
    }

    safeZones.forEach((zone, index) => {
        const item = document.createElement('div');
        item.className = 'safezone-item';

        item.innerHTML = `
            <div class="safezone-name">${index + 1}. ${zone.name}</div>
            <div class="safezone-details">
                📍 Coordinates: ${zone.latitude}, ${zone.longitude}
            </div>
            <div class="safezone-distance">📏 Distance: ${zone.distance_km} km</div>
        `;

        container.appendChild(item);
    });
}

// Display results
function displayResults(data) {
    const prediction = data.prediction;
    const safeZones = data.safe_zones;

    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });

    // Display risk level
    const riskLevel = prediction.risk_level;
    const confidence = (prediction.confidence * 100).toFixed(1);

    document.getElementById('riskLevel').textContent = riskLevel;
    document.getElementById('confidence').textContent = confidence;

    const riskBadge = document.getElementById('riskBadge');
    riskBadge.className = 'risk-badge ' + riskLevel.toLowerCase();

    // Display probabilities
    displayProbabilities(prediction.probabilities);

    // Display safe zones
    displaySafeZones(safeZones.safe_zones);

    // Initialize map
    initMap(safeZones.user_location.latitude, safeZones.user_location.longitude, safeZones.safe_zones);
}

// Handle form submission
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Hide previous results and errors
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';

    // Show loading
    document.getElementById('loading').style.display = 'block';

    // Get form data
    const formData = {
        rainfall: parseFloat(document.getElementById('rainfall').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        river_level: parseFloat(document.getElementById('river_level').value),
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value)
    };

    try {
        // Make API request
        const response = await fetch('/predict-and-recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        // Hide loading
        document.getElementById('loading').style.display = 'none';

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        showError('Error: ' + error.message);
    }
});

// Add sample data button functionality
function fillSampleData(scenario) {
    const sampleData = {
        'high': {
            rainfall: 250,
            temperature: 32,
            humidity: 90,
            river_level: 12,
            latitude: 19.0760,
            longitude: 72.8777
        },
        'medium': {
            rainfall: 120,
            temperature: 28,
            humidity: 75,
            river_level: 6,
            latitude: 28.6139,
            longitude: 77.2090
        },
        'low': {
            rainfall: 20,
            temperature: 25,
            humidity: 60,
            river_level: 3,
            latitude: 13.0827,
            longitude: 80.2707
        }
    };

    const data = sampleData[scenario];
    if (data) {
        document.getElementById('rainfall').value = data.rainfall;
        document.getElementById('temperature').value = data.temperature;
        document.getElementById('humidity').value = data.humidity;
        document.getElementById('river_level').value = data.river_level;
        document.getElementById('latitude').value = data.latitude;
        document.getElementById('longitude').value = data.longitude;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Flood Risk Prediction System loaded');
});
