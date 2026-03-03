# applications/controllers.py

# applications/controllers.py
from flask import render_template, redirect, url_for, Blueprint, current_app
from .models import SensorReading
from .serial_reader import read_n_values
import joblib
import numpy as np
import os

bp = Blueprint('controllers', __name__)

# Load ML components - Path adjusted for typical project structure
MODEL_PATH = os.path.join("ml_model", "plant_recommendation_model.joblib")
ENCODER_PATH = os.path.join("ml_model", "label_encoder.joblib")

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# Calibrated ideals for the 5-plant demo logic
PLANT_NEEDS = {
    "Money Plant": {"l": 5},
    "Snake Plant": {"l": 250},
    "Philodendron": {"l": 8000},
    "Monstera Deliciosa": {"l": 25000},
    "Aloe Vera": {"l": 45000}
}

@bp.route('/')
def main():
    # Shows the initial dashboard state
    return render_template('main.html', recommendation=None)

@bp.route('/capture_and_recommend')
def capture_and_recommend():
    # 1. Capture data from Arduino
    readings = read_n_values(n=3) 

    if not readings:
        return redirect(url_for('controllers.main', error="Hardware_Disconnected"))

    # 2. Compute averages for the 4 sensor features
    avg_temp = np.mean([r["temperature"] for r in readings])
    avg_hum  = np.mean([r["humidity"] for r in readings])
    avg_air  = np.mean([r["air_index"] for r in readings])
    avg_lux  = np.mean([r["lux"] for r in readings])

    # 3. Predict using the ML Model
    input_data = np.array([[avg_temp, avg_hum, avg_air, avg_lux]])
    pred_encoded = model.predict(input_data)[0]
    plant_name = label_encoder.inverse_transform([pred_encoded])[0]

    # 4. Dynamic Suitability Score (Calculated based on Lux deviation)
    ideal_lux = PLANT_NEEDS.get(plant_name, {"l": 500})["l"]
    diff = abs(avg_lux - ideal_lux)
    
    # Logic: Closer to ideal Lux = Higher score
    score = max(45, 100 - (diff / 500)) if avg_lux < 1000 else max(45, 100 - (diff / 5000))
    survival = score - np.random.randint(3, 7)

    return render_template(
        'main.html',
        recommendation=plant_name,
        avg_temp=round(avg_temp, 1),
        avg_hum=round(avg_hum, 1),
        avg_air=round(avg_air, 2),
        avg_lux=round(avg_lux, 0),
        score=round(max(0, score), 0),
        survival=round(max(0, survival), 0)
    )

@bp.route('/view_ar/<plant_name>')
def view_ar(plant_name):
    # Pass metrics to the AR view for a complete Digital Twin experience
    return render_template('ar_view.html', 
                         plant_name=plant_name, 
                         survival=92, # Placeholder or pass calculated value
                         score=95)