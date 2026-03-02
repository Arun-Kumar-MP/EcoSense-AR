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
    return render_template(
        'main.html',
        recommendation=None,
        score=None,
        survival=None
    )

@bp.route('/capture_and_recommend')
def capture_and_recommend():
    with current_app.app_context():
        readings = read_n_values(n=10)

    if not readings:
        return render_template(
            'main.html',
            recommendation=None,
            score=None,
            survival=None
        )

    # Compute averages
    avg_temp = np.mean([r["temperature"] for r in readings])
    avg_hum  = np.mean([r["humidity"] for r in readings])
    avg_air  = np.mean([r["air_index"] for r in readings])
    avg_lux  = np.mean([r["lux"] for r in readings])

    # Predict plant
    input_data = np.array([[avg_temp, avg_hum, avg_air, avg_lux]])
    pred_encoded = model.predict(input_data)[0]
    plant_name = label_encoder.inverse_transform([pred_encoded])[0]

    # -------- Environmental Suitability Score --------

    def clamp(val, min_val=0, max_val=100):
        return max(min_val, min(max_val, val))

    score_temp = 100 - abs(avg_temp - 28) * 2
    score_hum  = 100 - abs(avg_hum - 60) * 1.5
    score_lux  = 100 - abs(avg_lux - 500) / 10
    score_air  = 100 - abs(avg_air - 3) * 10

    score = (score_temp + score_hum + score_lux + score_air) / 4
    score = clamp(score)

    survival = max(10, score - 10)

    return render_template(
        'main.html',
        recommendation=plant_name,
        avg_temp=round(avg_temp,2),
        avg_hum=round(avg_hum,2),
        avg_air=round(avg_air,2),
        avg_lux=round(avg_lux,2),
        score=round(score,0),
        survival=round(survival,0)
    )