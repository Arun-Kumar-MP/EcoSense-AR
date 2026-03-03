# applications/controllers.py

from flask import render_template, redirect, url_for, Blueprint, current_app
from .models import SensorReading
from .serial_reader import read_n_values
import joblib
import numpy as np

bp = Blueprint('controllers', __name__)

# Load ML components
model = joblib.load("ml_model/plant_recommendation_model.joblib")
label_encoder = joblib.load("ml_model/label_encoder.joblib")

# Plant Library for Logic-Based Scoring
PLANT_NEEDS = {
    "Snake Plant": {"t": 25, "h": 40, "l": 1500, "a": 2.0},
    "Fern": {"t": 22, "h": 75, "l": 2500, "a": 3.5},
    "Aloe Vera": {"t": 32, "h": 30, "l": 35000, "a": 3.0},
    "Cactus": {"t": 35, "h": 25, "l": 40000, "a": 2.5},
    "Default": {"t": 26, "h": 50, "l": 5000, "a": 2.5}
}

@bp.route('/')
def index():
    return redirect(url_for('controllers.main'))

@bp.route('/main')
def main():
    return render_template(
        'main.html',
        recommendation=None,
        score=None,
        survival=None
    )

@bp.route('/capture_and_recommend')
def capture_and_recommend():
    with current_app.app_context():
        readings = read_n_values(n=5) # Reduced for faster demo response

    if not readings:
        return redirect(url_for('controllers.main', error="Hardware_Disconnected"))

    # Compute averages
    avg_temp = np.mean([r["temperature"] for r in readings])
    avg_hum  = np.mean([r["humidity"] for r in readings])
    avg_air  = np.mean([r["air_index"] for r in readings])
    avg_lux  = np.mean([r["lux"] for r in readings])

    # Predict
    input_data = np.array([[avg_temp, avg_hum, avg_air, avg_lux]])
    pred_encoded = model.predict(input_data)[0]
    plant_name = label_encoder.inverse_transform([pred_encoded])[0]

    # Dynamic Score Logic: 100 - (Difference from Ideal)
    # Different plants have different 'ideal' ranges
    score_temp = 100 - abs(avg_temp - 27) * 4 # Assume 27C is ideal for most
    score_hum  = 100 - abs(avg_hum - 55) * 1.5 
    score_lux  = min(100, (avg_lux / 5000) * 100) # Simplified lux score
    
    score = (score_temp + score_hum + score_lux) / 3
    survival = max(10, score - 5)

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
    # This renders the new page specifically for AR
    return render_template('ar_view.html', plant_name=plant_name)