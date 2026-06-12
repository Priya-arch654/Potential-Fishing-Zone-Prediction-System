# Captain Abyss - Maritime Intelligence & Fishing Zone Prediction

A comprehensive maritime intelligence platform delivering predictive fishing zone analytics, harbor-anchored navigation, and AI-powered guidance for the Indian coastal sector.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Compliance & Safety](#compliance--safety)
- [Contributing](#contributing)

---

## Overview

**Captain Abyss** is an enterprise-grade maritime decision-support system designed for fishermen, maritime operators, and coastal authorities in India. The platform leverages oceanographic telemetry, deterministic zone algorithms, and AI-assisted reasoning to optimize fishing operations while maintaining navigational safety.

### Core Objectives
- Predict high-yield fishing zones with 97+ harbor anchor points
- Provide persistent navigation routing (land and sea)
- Deliver real-time oceanographic conditions
- Enable AI-powered maritime guidance

---

## Features

### 1. Potential Fishing Zone (PFZ) Prediction
- **Harbor-Anchored Algorithm**: Seeded random generation ensures consistent zone placement across sessions
- **Seaward Intelligence**: Geographic-aware directional logic (Arabian Sea westward, Bay of Bengal eastward)
- **Oceanographic Integration**: Live SST, Chlorophyll, Wind Speed, and Safety Rating overlays
- **Zone Persistence**: Zones regenerate deterministically at each harbor location

### 2. Navigation Engine
| Mode | Purpose | Technology |
|------|---------|-----------|
| **Sea Voyage** | Open-ocean maritime routing | Leaflet, Nautical lines, Bearing-based navigation |
| **Land Road** | Harbor access from terrestrial points | OSRM (Open Source Routing Machine) |
| **Bridge Control** | Turn-by-turn maritime maneuvers | Cardinal bearing instructions, real-time heading |

### 3. AI Bridge Command
- **Llama 3.3 70B Integration**: Groq Cloud-powered maritime advisor
- **Contextual Reasoning**: Harbor-specific and zone-specific intelligence
- **Persona-Driven Interface**: Nautical-themed guidance and historical ocean insights
- **Real-Time Alerts**: Security warnings and yield projections on demand

### 4. Data Persistence
- **MongoDB Backend**: Voyage logs, catch records, and route history
- **Yield Analytics Dashboard**: Historical performance and trend analysis
- **Automatic Synchronization**: Trip data captures both land and sea segments

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Leaflet)                   │
│  (Map Rendering, Navigation UI, Bridge Command Panel)        │
└────────────┬─────────────────────────────────────────────────┘
             │
┌────────────▼──────────────────────────────────────────────────┐
│                   Backend API (Flask/Python)                  │
│  (PFZ Algorithm, Routing, Zone Management, Data Sync)        │
└────────────┬─────────────────────────────────────────────────┘
             │
     ┌───────┴──────────────────┬──────────────────┐
     │                          │                  │
┌────▼────────┐    ┌───────────▼──────┐  ┌────────▼──────┐
│   MongoDB   │    │  Groq AI (LLM)   │  │ OpenWeather   │
│   Database  │    │  Llama 3.3 70B   │  │   API         │
└─────────────┘    └──────────────────┘  └───────────────┘
```

---

## Installation

### Requirements
- **Python**: 3.10 or higher
- **MongoDB**: 5.0+ (local or MongoDB Atlas)
- **Internet Connection**: For API integrations (Groq, OpenWeather)

### Step 1: Clone Repository
```bash
git clone https://github.com/Priya-arch654/Potential-Fishing-Zone-Prediction-System.git
cd Potential-Fishing-Zone-Prediction-System
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
```bash
# Ensure MongoDB is running
# For local MongoDB (default):
mongod --dbpath /path/to/data/directory

# For Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

---

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Application
SECRET_KEY=your-secret-key-here
DEBUG=False
FLASK_ENV=production

# Database
MONGO_URI=mongodb://localhost:27017/pfz_database
# OR for MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/pfz_database

# External APIs
GROQ_API_KEY=your-groq-api-key
OPENWEATHER_API_KEY=your-openweather-api-key

# Optional: Harbor Dataset Path
HARBOR_DATA_CSV=data/indian_harbors.csv
```

### Application Settings
Edit `config.py` for advanced tuning:
```python
ZONE_GENERATION_SEED = 42  # Deterministic seeding
ZONE_COUNT_PER_HARBOR = 3  # Fishing zones per location
SEAWARD_BUFFER_KM = 50     # Distance offshore
OSRM_SERVER = "https://router.project-osrm.org/route/v1"
```

---

## Usage

### 1. Start the Application
```bash
python app.py
```
Access at: `http://127.0.0.1:5000`

### 2. Dashboard Features

#### Fishing Zone Prediction
- Select a harbor from the dropdown
- View all predicted fishing zones (marked on map)
- Click any zone to see oceanographic details:
  - Sea Surface Temperature (°C)
  - Chlorophyll Concentration (mg/m³)
  - Wind Speed (knots)
  - Safety Rating (1-10)

#### Navigation
- **Sea Voyage**: Enter destination coordinates, receive maritime bearing
- **Land Road**: Select destination harbor, receive road directions
- **Bridge Commands**: Real-time cardinal headings for vessel piloting

#### AI Assistance
- Click "Ask Captain Abyss" on any harbor or zone
- Receive contextual maritime intelligence
- View historical yield data for the location

### 3. Voyage History
- Access dashboard at `/voyages`
- Filter by date range, harbor, or vessel
- Export logs as CSV/JSON

---

## API Reference

### Fishing Zones Endpoint
```http
GET /api/zones/<harbor_id>
```
**Response**:
```json
{
  "harbor_name": "Mumbai Port",
  "zones": [
    {
      "id": "zone_001",
      "latitude": 18.95,
      "longitude": 72.82,
      "sst": 28.5,
      "chlorophyll": 0.8,
      "wind_speed": 12,
      "safety_rating": 8
    }
  ]
}
```

### Navigation Endpoint
```http
POST /api/route
```
**Payload**:
```json
{
  "mode": "sea",
  "start": [18.95, 72.82],
  "end": [19.05, 73.05]
}
```

### AI Bridge Endpoint
```http
POST /api/bridge/advice
```
**Payload**:
```json
{
  "harbor_id": "mumbai",
  "context": "What are the best fishing conditions today?"
}
```

---

## Data Models

### Harbor Schema
```python
{
  "_id": ObjectId,
  "name": String,
  "state": String,
  "latitude": Float,
  "longitude": Float,
  "capacity": Integer,
  "features": [String]  # Fuel, Water, Repair, etc.
}
```

### Voyage Log Schema
```python
{
  "_id": ObjectId,
  "vessel_id": String,
  "start_time": DateTime,
  "end_time": DateTime,
  "route_type": String,  # "sea" or "land"
  "waypoints": [GeoJSON Point],
  "catch_data": {
    "total_weight_kg": Float,
    "fish_species": [String],
    "timestamp": DateTime
  }
}
```

---

## Compliance & Safety

### Disclaimer
Captain Abyss is a **decision-support tool only**. All predictions are heuristic models for demonstration purposes.

### Regulatory References
- Consult **Indian Coast Guard (ICG)** for navigational alerts
- Verify forecasts with **India Meteorological Department (IMD)**
- Check **INCOIS** (Indian National Centre for Ocean Information Services) for oceanographic data
- Adhere to **MAUSAM** warnings before deep-sea operations

### Best Practices
- Always file voyage plans with local harbor authorities
- Maintain communication on designated maritime VHF channels
- Cross-reference all predictions with official weather services
- Report anomalies to ICG immediately

---

## Contributing

We welcome contributions from maritime professionals, developers, and researchers.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a Pull Request

---

## License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## Support & Contact

- **Issues**: [GitHub Issues](https://github.com/Priya-arch654/Potential-Fishing-Zone-Prediction-System/issues)
- **Documentation**: See `/docs` folder
- **Email**: support@captainabyss.io

---

**Captain Abyss** — *Navigating the deep waters of Indian maritime commerce.* ⚓🌊
