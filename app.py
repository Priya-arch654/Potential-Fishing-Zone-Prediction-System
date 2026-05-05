import os
import random
import requests
import csv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from groq import Groq

# Load Indian Coastal Zones and Safety Data
COASTAL_ZONES = []
try:
    with open('fishing_harbors_safety_data.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            COASTAL_ZONES.append({
                "lat": float(row['Latitude']),
                "lon": float(row['Longitude']),
                "state": row['State'],
                "location": row['Location'],
                "safety": row.get('Safety_Rating', 'Unknown'),
                "sst": float(row.get('SST', 26.0)),
                "chlorophyll": float(row.get('Chlorophyll', 0.5)),
                "wind_speed": float(row.get('Wind_Speed', 5.0))
            })
except Exception as e:
    print(f"Error loading CSV: {e}")

def is_in_sea(lat, lon, harbor):
    # Directional Intelligence: Push points AWAY from the Indian landmass
    state = harbor.get('state', '').lower()
    h_lat = harbor['lat']
    h_lon = harbor['lon']
    
    # WEST COAST: Sea is to the WEST (Longitude must be LESS than harbor)
    if any(s in state for s in ['gujarat', 'maharashtra', 'goa', 'karnataka', 'kerala']):
        if lon >= h_lon - 0.05: return False # Must be clearly West
        
    # EAST COAST: Sea is to the EAST (Longitude must be MORE than harbor)
    if any(s in state for s in ['tamil nadu', 'andhra', 'odisha', 'west bengal']):
        if lon <= h_lon + 0.05: return False # Must be clearly East
        
    # SOUTH TIP: Sea is also SOUTH
    if 'tamil nadu' in state and h_lat < 10.0:
        if lat >= h_lat - 0.05: return False # Must be South of harbor
        
    return True

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key-123")

# MongoDB Setup
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/pfz_database")
client = MongoClient(mongo_uri)
db = client.get_default_database()
users_coll = db.users
catch_logs_coll = db.catch_logs
voyages_coll = db.voyages

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.name = user_data.get('name', 'Fisherman')

@login_manager.user_loader
def load_user(user_id):
    user_data = users_coll.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# --- ROUTES ---

@app.route('/chatbot')
@login_required
def chatbot_view():
    return render_template('chatbot.html')

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = users_coll.find_one({"email": email})
        if user_data and check_password_hash(user_data['password'], password):
            user_obj = User(user_data)
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "error")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if users_coll.find_one({"email": email}):
            flash("Email already registered", "error")
        else:
            hashed_pw = generate_password_hash(password)
            users_coll.insert_one({"name": name, "email": email, "password": hashed_pw})
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        "active_zones": 12,
        "recent_catches": catch_logs_coll.count_documents({"user_id": current_user.id}),
        "avg_sst": 26.4
    }
    return render_template('dashboard.html', stats=stats)

@app.route('/map')
@login_required
def map_view():
    return render_template('map.html')

@app.route('/api/get_harbors')
@login_required
def get_harbors():
    return jsonify(COASTAL_ZONES)

@app.route('/api/get_zones')
@login_required
def get_zones():
    lat = float(request.args.get('lat', 15.0))
    lon = float(request.args.get('lon', 75.0))
    
    # Anchor to nearest harbor for directional logic
    harbor = min(COASTAL_ZONES, key=lambda p: (p['lat'] - lat)**2 + (p['lon'] - lon)**2)
    
    zones = []
    seed = int((lat + lon) * 1000)
    rng = random.Random(seed)
    
    attempts = 0
    while len(zones) < 3 and attempts < 100:
        attempts += 1
        state = harbor['state'].lower()
        
        # West Coast: Sea is West
        if any(s in state for s in ['gujarat', 'maharashtra', 'goa', 'karnataka', 'kerala']):
            offset_lon = rng.uniform(-1.5, -0.4) # Push West
            offset_lat = rng.uniform(-0.5, 0.5)
        # East Coast: Sea is East
        elif any(s in state for s in ['tamil nadu', 'andhra', 'odisha', 'west bengal']):
            offset_lon = rng.uniform(0.4, 1.5) # Push East
            offset_lat = rng.uniform(-0.5, 0.5)
        else:
            offset_lon = rng.uniform(-0.8, 0.8)
            offset_lat = rng.uniform(-0.8, 0.8)
            
        z_lat, z_lon = harbor['lat'] + offset_lat, harbor['lon'] + offset_lon
        
        if is_in_sea(z_lat, z_lon, harbor):
            zones.append({
                "lat": round(z_lat, 4), "lon": round(z_lon, 4),
                "status": rng.choice(["HIGH", "MEDIUM"]),
                "sst": f"{round(rng.uniform(24, 28), 2)}°C",
                "chlorophyll": f"{round(rng.uniform(0.3, 0.9), 2)} mg/m³",
                "wind_speed": f"{round(rng.uniform(3, 12), 2)} kn",
                "salinity": rng.choice(["Safe", "Average Safe", "Danger"])
            })
    return jsonify(zones)

@app.route('/api/recommendations')
@login_required
def get_recommendations():
    logs = list(catch_logs_coll.find().sort("quantity", -1).limit(10))
    recommendations = []
    for log in logs:
        if 'lat' in log and 'lon' in log:
            recommendations.append({
                "lat": log['lat'], "lon": log['lon'], "yield": log['quantity'],
                "fish_type": log['fish_type'], "timestamp": log['timestamp']
            })
    return jsonify(recommendations)

@app.route('/catch_logs')
@login_required
def catch_logs():
    logs = list(catch_logs_coll.find({"user_id": current_user.id}).sort("_id", -1))
    return render_template('catch_log.html', logs=logs)

@app.route('/api/add_catch', methods=['POST'])
@login_required
def add_catch():
    data = request.json
    catch_logs_coll.insert_one({
        "user_id": current_user.id, "fish_type": data.get('fish_type'),
        "quantity": float(data.get('quantity', 0)), "lat": float(data.get('lat', 0)),
        "lon": float(data.get('lon', 0)), "timestamp": data.get('timestamp')
    })
    return jsonify({"status": "success"})

@app.route('/api/save_voyage', methods=['POST'])
@login_required
def save_voyage():
    data = request.json
    voyages_coll.insert_one({
        "user_id": current_user.id, "waypoints": data.get('waypoints'),
        "destination_name": data.get('destination_name'), "distance": data.get('distance'),
        "timestamp": data.get('timestamp')
    })
    return jsonify({"status": "success"})

@app.route('/api/get_my_voyages')
@login_required
def get_my_voyages():
    voyages = list(voyages_coll.find({"user_id": current_user.id}).sort("_id", -1))
    for v in voyages:
        v['_id'] = str(v['_id'])
    return jsonify(voyages)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.json.get('message')
    
    # 1. Fetch Context from Database (Voyages and Catches)
    voyages = list(voyages_coll.find({"user_id": current_user.id}).sort("_id", -1).limit(5))
    catches = list(catch_logs_coll.find({"user_id": current_user.id}).sort("_id", -1).limit(5))
    
    # 2. Format Intelligence Brief
    voyage_summary = "\n".join([f"- {v.get('destination_name', 'Trip')}: {v.get('distance', '--')}km" for v in voyages]) if voyages else "No voyages recorded yet."
    catch_summary = "\n".join([f"- {c.get('fish_type', 'Fish')}: {c.get('quantity', 0)}kg" for c in catches]) if catches else "No catches logged yet."
    
    project_context = """
    PLATFORM CAPABILITIES (Your Internal Logic):
    - PFZ Engine: Uses deterministic seeding for stable fishing zones.
    - Seaward Intelligence: Automatically pushes zones into the sea based on harbor state (West Coast -> Arabian Sea, East Coast -> Bay of Bengal).
    - Hybrid Routing: Supports 'Sea mode' (direct dashed lines) and 'Land mode' (road-based).
    - Bridge Control: Provides cardinal bearings (North, East, etc.) for open ocean navigation.
    """

    system_prompt = f"""You are 'Captain Abyss', the high-performance AI bridge commander of this navigator.
    
    CAPTAIN'S LOGS (Real-time DB Access):
    - RECENT VOYAGES:
    {voyage_summary}
    
    - RECENT CATCHES:
    {catch_summary}
    
    {project_context}

    INSTRUCTIONS:
    1. Be logical and data-driven. If the captain has caught more fish in a specific trip, congratulate him and suggest similar coordinates.
    2. Reference the platform's features (Sea/Land mode, Seaward logic) to show you know how the system works.
    3. Use your unique nautical persona: speak like a legend of the Indian Ocean.
    4. Help the captain optimize his routes based on his distance history.
    """

    client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
    try:
        completion = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7, max_tokens=1024,
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

@app.route('/api/weather')
@login_required
def get_weather():
    lat, lon = request.args.get('lat'), request.args.get('lon')
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        resp = requests.get(url).json()
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
