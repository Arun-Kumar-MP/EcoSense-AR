# applications/controllers.py

from flask import render_template, redirect, url_for, Blueprint, current_app
from .models import SensorReading
from .serial_reader import read_n_values
import joblib
import numpy as np

bp = Blueprint('controllers', __name__)

# Load ML model and encoder once
model = joblib.load("ml_model/plant_recommendation_model.joblib")
label_encoder = joblib.load("ml_model/label_encoder.joblib")

@bp.route('/')
def index():
    return redirect(url_for('controllers.main'))

@bp.route('/main')
def main():
    return render_template('main.html')

@bp.route('/capture_and_recommend')
def capture_and_recommend():
    with current_app.app_context():
        readings = read_n_values(n=10)

    if not readings:
        return render_template('main.html', recommendation="No sensor data captured.")

    # Compute averages
    avg_temp = np.mean([r["temperature"] for r in readings])
    avg_hum  = np.mean([r["humidity"] for r in readings])
    avg_air  = np.mean([r["air_index"] for r in readings])
    avg_lux  = np.mean([r["lux"] for r in readings])

    # Predict plant
    input_data = np.array([[avg_temp, avg_hum, avg_air, avg_lux]])
    pred_encoded = model.predict(input_data)[0]
    plant_name = label_encoder.inverse_transform([pred_encoded])[0]

    return render_template('main.html', 
                           recommendation=plant_name,
                           avg_temp=round(avg_temp,2),
                           avg_hum=round(avg_hum,2),
                           avg_air=round(avg_air,2),
                           avg_lux=round(avg_lux,2))