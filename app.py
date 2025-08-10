# combined_app.py (V5 - Enhanced Map Visualization)
import os
import time
import logging
import requests
import threading
import pandas as pd
import pydeck as pdk
import streamlit as st
from flask import Flask, jsonify, request
from tinydb import TinyDB, Query
from dotenv import load_dotenv

# --- CONFIGURATION & LOGGING ---
load_dotenv()
log_file = 'data/agent.log'
logging.basicConfig(level="INFO", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# ==============================================================================
# --- 1. AI AGENT LOGIC ---
# ==============================================================================
class WeatherAPI_Sensor:
    def __init__(self, api_key, location):
        self.api_key, self.location = api_key, location
        self.base_url = "http://api.weatherapi.com/v1/current.json"
        if not self.api_key or "YOUR_API_KEY" in self.api_key: raise ValueError("API key is missing or is a placeholder.")
        logger.info(f"Sensor initialized for {self.location}")
        
    def get_reading(self):
        params = {"key": self.api_key, "q": self.location, "aqi": "no"}
        try:
            r = requests.get(self.base_url, params=params, timeout=10)
            r.raise_for_status(); data = r.json()['current']
            return {
                "condition_text": data['condition']['text'], "condition_icon": "https:" + data['condition']['icon'],
                "is_day": data['is_day'], "cloud_cover": data['cloud'], "temp_c": data['temp_c'],
                "wind_kph": data['wind_kph'], "humidity": data['humidity'], "uv": data['uv']}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Exception: {e}"); return None

class DecisionEngine:
    def evaluate(self, fact):
        if not fact: return "UNKNOWN_STATE"
        cond = fact['condition_text'].lower()
        if not fact['is_day']: return "NIGHT_TIME"
        if any(w in cond for w in ["rain", "thunder", "drizzle"]): return "POOR_VISIBILITY_PRECIPITATION"
        if fact['cloud_cover'] > 75: return "OVERCAST"
        return "NORMAL_DAYLIGHT"

class DummyRAG:
    def __init__(self):
        self._kb = {"NIGHT_TIME": {"value": 0.9, "reason": "Night-Time"},"POOR_VISIBILITY_PRECIPITATION": {"value": 0.85, "reason": "Precipitation"},"OVERCAST": {"value": 0.6, "reason": "Overcast"},"NORMAL_DAYLIGHT": {"value": 0.3, "reason": "Normal Daylight"},"UNKNOWN_STATE": {"value": 0.3, "reason": "Unknown State"}}
    def get_recommendation(self, context): return self._kb.get(context, self._kb["UNKNOWN_STATE"])

class WeatherAgent:
    def __init__(self, sensor, engine, rag): self.sensor, self.engine, self.rag = sensor, engine, rag
    def run_cycle(self):
        logger.info("--- Running agent cycle ---")
        fact = self.sensor.get_reading()
        context = self.engine.evaluate(fact)
        rec = self.rag.get_recommendation(context)
        logger.info(f"DB update reason: {rec['reason']}")
        return {"recommendation": rec, "weather_fact": fact}

# ==============================================================================
# --- 2. FLASK BACKEND LOGIC ---
# ==============================================================================
API_KEY = os.environ.get("WEATHER_API_KEY")
LOCATION = os.environ.get("LOCATION", "Mumbai, Maharashtra")
app = Flask(__name__)
if not os.path.exists('data'): os.makedirs('data')
db = TinyDB('data/db.json', indent=4)
Pole = Query()
def initialize_db():
    if not db.all():
        fleet_data = [{"id":f"PN-{i:03d}","locationName":f"Sector {chr(64+i//4)}-{i}","lat":19.05+i*0.005,"lon":72.87+i*0.005,"status":"Online" if i%5!=0 else "Fault","brightness":0.0,"weather":"N/A","manual_override":False} for i in range(1,13)]
        db.insert_multiple(fleet_data)

@app.route('/run-agent-cycle', methods=['POST'])
def run_agent_cycle_endpoint():
    agent = WeatherAgent(WeatherAPI_Sensor(API_KEY, LOCATION), DecisionEngine(), DummyRAG())
    result = agent.run_cycle()
    db.update(result['recommendation'], (Pole.status == 'Online') & (Pole.manual_override == False))
    return jsonify(result)
@app.route('/get-fleet-status', methods=['GET'])
def get_fleet_status(): return jsonify({"fleet": {p['id']: p for p in db.all()}})
@app.route('/set-manual-override/<pole_id>', methods=['POST'])
def set_manual_override(pole_id): db.update(request.json, Pole.id == pole_id); return jsonify({"success": True})
@app.route('/simulate-attack', methods=['POST'])
def simulate_attack(): db.update({'brightness': 0.5, 'weather': "Data Anomaly Detected"}, (Pole.status == 'Online') & (Pole.manual_override == False)); return jsonify({"success": True})
def run_flask_app(): initialize_db(); app.run(port=5000, debug=False, use_reloader=False)

# ==============================================================================
# --- 3. STREAMLIT FRONTEND LOGIC ---
# ==============================================================================
API_URL = "http://127.0.0.1:5000"
def api_call(method, endpoint, json_data=None):
    try:
        url = f"{API_URL}/{endpoint}"
        if method == 'POST': response = requests.post(url, json=json_data, timeout=10)
        else: response = requests.get(url, timeout=5)
        response.raise_for_status(); return response.json()
    except requests.exceptions.RequestException as e: st.error(f"API call failed: {e}"); return None

def get_pole_color(row):
    if row['status'] == 'Online': return [0, 255, 0, 40 + row['brightness'] * 215]
    if row['status'] == 'Fault': return [255, 165, 0, 160]
    return [128, 128, 128, 100] # Offline

st.set_page_config(page_title="VESIT-NG Dashboard", page_icon="🛰️", layout="wide")
st.title("🛰️ VESIT-NG Smart Lighting - Pilot Dashboard")

with st.sidebar:
    st.header("System Controls")
    if st.button("Refresh Live Data", type="primary", use_container_width=True):
        with st.spinner("Running agent..."): result = api_call('POST', 'run-agent-cycle')
        if result and result.get('weather_fact'): st.session_state['weather_fact'] = result['weather_fact']
        st.toast("Data refreshed!", icon="✅"); st.rerun()
    st.header("🌦️ Live Weather")
    if 'weather_fact' in st.session_state and st.session_state['weather_fact']:
        weather = st.session_state['weather_fact']
        st.image(weather['condition_icon'], width=50); st.metric("Condition", weather['condition_text'])
        st.metric("Temperature", f"{weather['temp_c']} °C"); st.metric("Wind Speed", f"{weather['wind_kph']} kph")
    else: st.info("No weather data yet.")
    st.header("🚨 Attack Simulation")
    if st.button("🔥 Simulate Attack", use_container_width=True):
        api_call('POST', 'simulate-attack'); st.toast("Attack command sent!", icon="🔥"); time.sleep(1); st.rerun()

if 'first_load_done' not in st.session_state:
    with st.spinner("Running initial agent cycle..."):
        result = api_call('POST', 'run-agent-cycle')
        if result and result.get('weather_fact'): st.session_state['weather_fact'] = result['weather_fact']
    st.session_state['first_load_done'] = True; st.rerun()

data = api_call('GET', 'get-fleet-status')
if data and "fleet" in data:
    poles_df = pd.DataFrame(data["fleet"].values())
    poles_df['brightness_text'] = poles_df['brightness'].apply(lambda x: f"{x:.0%}")
    poles_df['radius'] = 30 + poles_df['brightness'] * 70
    poles_df['fill_color'] = poles_df.apply(get_pole_color, axis=1)

    st.markdown("## System Health Overview")
    online, faulty, override = poles_df[poles_df['status'] == 'Online'].shape[0], poles_df[poles_df['status'] == 'Fault'].shape[0], poles_df[poles_df['manual_override'] == True].shape[0]
    c1,c2,c3 = st.columns(3); c1.metric("Online", online,"✅"); c2.metric("Faulty", faulty,"⚠️"); c3.metric("Override", override,"🧑‍🔧")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🗺️ Live Map", "📊 Data Table"])
    with tab1:
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v9',
            initial_view_state=pdk.ViewState(latitude=poles_df['lat'].mean(), longitude=poles_df['lon'].mean(), zoom=12, pitch=50),
            layers=[pdk.Layer(
                'ScatterplotLayer', data=poles_df, get_position='[lon, lat]',
                get_fill_color='fill_color', get_radius='radius',
                # MAP ENHANCEMENT: Add a red outline to faulty poles
                get_line_color='status == "Fault" ? [255, 0, 0, 255] : [0, 0, 0, 0]',
                line_width_min_pixels=2,
                pickable=True
            )],
            tooltip={"text": "ID: {id}\nStatus: {status}\nBrightness: {brightness_text}"}
        ))
    with tab2: st.dataframe(poles_df, use_container_width=True)
    st.markdown("---")
    
    st.markdown("## 🧑‍🔧 Pole Management")
    selected_id = st.selectbox("Select Pole:", options=poles_df['id'])
    if selected_id:
        pole = poles_df[poles_df['id'] == selected_id].iloc[0]
        with st.expander("Manual Control Panel", expanded=True):
            override = st.toggle("Enable Manual Override", value=bool(pole.manual_override), key=f"t_{selected_id}")
            brightness = st.slider("Set Brightness", 0, 100, int(pole.brightness*100), 5, "%d%%", key=f"s_{selected_id}", disabled=not override)
            if st.button("Apply Settings", key=f"b_{selected_id}"):
                api_call('POST', f'set-manual-override/{selected_id}', {"manual_override": override, "brightness": brightness/100.0}); time.sleep(0.5); st.rerun()
    
    st.markdown("---")
    with st.expander("📄 View Backend Agent Logs"):
        if os.path.exists(log_file):
            with open(log_file, 'r') as f: st.code(''.join(reversed(f.readlines())), language='log')
        else: st.warning("Log file not found.")
else:
    st.warning("Waiting for backend data...")

# ==============================================================================
# --- 4. MAIN EXECUTION ---
# ==============================================================================
if 'server_started' not in st.session_state:
    logger.info("Starting background Flask server...")
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    st.session_state['server_started'] = True
    time.sleep(2)
    api_call('POST', 'run-agent-cycle')
    st.rerun()