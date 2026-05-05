# ⚓ Captain Abyss | Potential Fishing Zone Prediction System

**Captain Abyss** is a professional-grade maritime intelligence platform designed for the Indian coastal sector. It provides high-fidelity Potential Fishing Zone (PFZ) predictions, stable harbor-anchored navigation, and AI-powered bridge guidance for modern fishermen and maritime explorers.

---

## 🌊 Key Features

### 📡 Maritime Intelligence Engine
- **Deterministic Zone Stability**: Fishing zones are anchored to 97+ Indian harbors using a seeded random generation algorithm, ensuring markers remain persistent across sessions and map interactions.
*   **Seaward Directional Logic**: Integrated 'Seaward Intelligence' that understands the geography of India (West for Arabian Sea, East for Bay of Bengal), pushing all predicted points deep into the ocean and away from land part.
- **Oceanographic Telemetry**: Real-time visualization of SST (Sea Surface Temperature), Chlorophyll levels, Wind Speed, and Safety Ratings.

### 🗺️ Hybrid Navigation System
- **Sea Voyage Mode**: Specialized maritime routing using high-visibility nautical dashed lines and direct "as-the-crow-flies" navigation for open ocean travel.
- **Land Road Mode**: Integrated OSRM (Open Source Routing Machine) logic for road-based navigation to reach harbors from any land location.
- **Abyss Bridge Control**: A dedicated bridge panel providing turn-by-turn maritime maneuvers with precise cardinal bearings (e.g., "Head North-West across the abyss").

### 🤖 AI Bridge Command
- **Captain Abyss AI**: Integrated Llama 3.3 70B (via Groq API) acting as a legendary maritime guide, providing real-time advice and historical ocean context in a unique nautical persona.
- **Interactive Intelligence Portal**: Tap any harbor or fishing zone to reveal deep-sea security alerts and yield data.

### 📜 Voyage History & Data Persistence
- **Persistent Logs**: All trips (both land and sea) are automatically synchronized with a MongoDB backend.
- **Yield Analytics**: Detailed history of catch logs and past voyages accessible via a high-performance dashboard.

---

## 🛠️ Technology Stack
- **Backend**: Python (Flask), PyMongo (MongoDB Atlas/Local)
- **Frontend**: Leaflet (Local GIS), Leaflet-Routing-Machine, Tailwind CSS
- **AI Model**: Llama 3.3 70B (Groq Cloud)
- **Data Source**: Custom Indian Coastal Harbor Dataset (CSV)

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- MongoDB (Running locally on port 27017 or a MongoDB Atlas URI)
- API Keys: `GROQ_API_KEY`, `OPENWEATHER_API_KEY`

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/abinayasasikumar10-debug/stitch_aquazone_pfz_predictor.git

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-dev-key
MONGO_URI=mongodb://localhost:27017/pfz_database
GROQ_API_KEY=your-groq-api-key
OPENWEATHER_API_KEY=your-openweather-api-key
```

### 4. Run the Abyss
```bash
python app.py
```
Access the dashboard at `http://127.0.0.1:5000`

---

## 🛡️ Safety & Compliance
This platform uses heuristic data models for demonstration purposes. Users should always consult official Indian Coast Guard (ICG) and INCOIS alerts before undertaking deep-sea voyages.

---

**Built by the Abyss for the Captains of the Sea.** ⚓🌑🌊
