# 🌊 Flood Risk Prediction and Safe Zone Recommendation System

An AI-powered Deep Learning system that predicts flood risk levels and recommends nearest safe zones based on environmental parameters and user location.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This system uses deep learning to analyze environmental parameters (rainfall, temperature, humidity, river water level) and predict the flood risk level (Low, Medium, High) for a given location. It also recommends the nearest safe zones using the Haversine formula for distance calculation.

## ✨ Features

- **Flood Risk Prediction**: Predicts flood risk levels using a trained deep neural network
- **Environmental Analysis**: Analyzes rainfall, temperature, humidity, and river water levels
- **Safe Zone Recommendations**: Finds and recommends nearest safe zones based on user location
- **Interactive Web Interface**: User-friendly web application with real-time predictions
- **Interactive Map**: Displays user location and safe zones on an interactive map using Leaflet.js
- **Probability Distribution**: Shows confidence levels for each risk category
- **Geolocation Support**: Automatically detects user location using browser geolocation

## 🛠️ Tech Stack

### Machine Learning / Deep Learning
- **Python 3.8+**
- **TensorFlow / Keras** - Deep learning framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Data preprocessing and evaluation
- **Matplotlib** - Visualization

### Backend
- **Flask** - Web framework for API endpoints

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern gradients and animations
- **JavaScript** - Interactive functionality
- **Leaflet.js** - Interactive maps

## 📁 Project Structure

```
flood-safezone-dl/
│
├── data/                          # Dataset storage
│   ├── flood_data.csv            # Training dataset
│   └── safe_zones.csv            # Safe zones locations
│
├── models/                        # Trained models and preprocessors
│   ├── flood_model.h5            # Trained Keras model
│   ├── scaler.pkl                # Feature scaler
│   ├── label_encoder.pkl         # Label encoder
│   └── training_history.png      # Training visualization
│
├── notebooks/                     # Jupyter notebooks (optional)
│
├── backend/                       # Backend utilities (optional)
│
├── frontend/                      # Web application frontend
│   ├── templates/
│   │   └── index.html            # Main web page
│   └── static/
│       ├── css/
│       │   └── style.css         # Styling
│       └── js/
│           └── script.js         # Frontend logic
│
├── utils/                         # Utility modules
│   ├── generate_dataset.py       # Dataset generation
│   ├── preprocessing.py          # Data preprocessing
│   ├── model.py                  # Model architecture
│   └── safezone.py               # Safe zone finder
│
├── train.py                       # Model training script
├── predict.py                     # Prediction script
├── app.py                         # Flask application
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/sonusarojini10/flood-safezone-dl.git
cd flood-safezone-dl
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Dataset
```bash
python utils/generate_dataset.py
```

This will create:
- `data/flood_data.csv` - Synthetic flood dataset (5000 samples)
- `data/safe_zones.csv` - Safe zones across India (15 locations)

### Step 4: Train the Model
```bash
python train.py
```

This will:
- Preprocess the data
- Train the deep learning model
- Save the model to `models/flood_model.h5`
- Save preprocessors (scaler and encoder)
- Generate training history plot

Expected output:
- Training accuracy: ~85-90%
- Validation accuracy: ~85-90%

### Step 5: Run the Web Application
```bash
python app.py
```

Access the application at: **http://localhost:5000**

## 💻 Usage

### Using the Web Interface

1. **Enter Environmental Parameters**:
   - Rainfall (mm): 0-300
   - Temperature (°C): 15-40
   - Humidity (%): 30-100
   - River Water Level (m): 0-15

2. **Enter Your Location**:
   - Latitude: -90 to 90
   - Longitude: -180 to 180
   - Or click "Use My Current Location"

3. **Click "Predict Flood Risk"**

4. **View Results**:
   - Flood risk level (Low/Medium/High)
   - Confidence percentage
   - Probability distribution
   - Nearest safe zones with distances
   - Interactive map showing your location and safe zones

### Using the Command Line

#### Make a Prediction
```bash
python predict.py
```

#### Find Safe Zones
```bash
python -c "from utils.safezone import find_nearest_safe_zones, display_safe_zones; zones = find_nearest_safe_zones(19.0760, 72.8777); display_safe_zones(19.0760, 72.8777, zones)"
```

## 🧠 Model Architecture

The deep learning model uses a Sequential architecture:

```
Input Layer (4 features)
    ↓
Dense Layer (64 neurons, ReLU)
    ↓
Dropout (30%)
    ↓
Dense Layer (32 neurons, ReLU)
    ↓
Dropout (20%)
    ↓
Dense Layer (16 neurons, ReLU)
    ↓
Output Layer (3 classes, Softmax)
```

### Training Configuration
- **Optimizer**: Adam
- **Loss Function**: Sparse Categorical Crossentropy
- **Metrics**: Accuracy
- **Batch Size**: 32
- **Epochs**: 50 (with early stopping)
- **Train/Test Split**: 80/20

## 🔌 API Endpoints

### 1. Home Page
```
GET /
Returns: HTML page
```

### 2. Predict Flood Risk
```
POST /predict
Content-Type: application/json

Request Body:
{
    "rainfall": 150,
    "temperature": 28,
    "humidity": 75,
    "river_level": 6
}

Response:
{
    "risk_level": "Medium",
    "confidence": 0.87,
    "probabilities": {
        "Low": 0.05,
        "Medium": 0.87,
        "High": 0.08
    },
    "input_parameters": {...}
}
```

### 3. Find Safe Zones
```
POST /safezone
Content-Type: application/json

Request Body:
{
    "latitude": 19.0760,
    "longitude": 72.8777,
    "risk_level": "High"
}

Response:
{
    "user_location": {
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "risk_level": "High",
    "safe_zones": [...]
}
```

### 4. Combined Prediction and Recommendation
```
POST /predict-and-recommend
Content-Type: application/json

Request Body:
{
    "rainfall": 250,
    "temperature": 32,
    "humidity": 90,
    "river_level": 12,
    "latitude": 19.0760,
    "longitude": 72.8777
}

Response:
{
    "prediction": {...},
    "safe_zones": {...}
}
```

### 5. Health Check
```
GET /health
Response: {"status": "healthy"}
```

## 📊 Dataset

### Flood Data Features
- **rainfall**: Rainfall amount in mm (0-300)
- **temperature**: Temperature in Celsius (15-40)
- **humidity**: Humidity percentage (30-100)
- **river_level**: River water level in meters (0-15)
- **latitude**: Location latitude
- **longitude**: Location longitude
- **flood_risk**: Target variable (Low, Medium, High)

### Safe Zones
15 safe zones across major Indian cities including:
- Delhi, Mumbai, Kolkata, Chennai
- Bangalore, Hyderabad, Pune, Ahmedabad
- And more...

## 🧪 Testing

Test the prediction functionality:
```bash
python predict.py
```

This will run three test cases:
1. High risk scenario
2. Low risk scenario
3. Medium risk scenario

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Sonu Sarojini**
- GitHub: [@sonusarojini10](https://github.com/sonusarojini10)

## 🙏 Acknowledgments

- TensorFlow/Keras team for the deep learning framework
- Flask team for the web framework
- Leaflet.js for the mapping library
- OpenStreetMap for map tiles

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**⚠️ Disclaimer**: This is a demonstration project for educational purposes. For real-world flood prediction, please consult official meteorological departments and use validated models.

**Made with ❤️ and AI**