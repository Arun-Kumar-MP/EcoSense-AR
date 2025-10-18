# applications/controllers.py

from flask import render_template, redirect, url_for, Blueprint, current_app
from .models import SensorReading
from .serial_reader import read_n_values

bp = Blueprint('controllers', __name__)

@bp.route('/')
def index():
    return redirect(url_for('controllers.home'))

@bp.route('/home')
def home():
    readings = SensorReading.query.order_by(SensorReading.timestamp.asc()).limit(50).all()
    return render_template('home.html', readings=readings)

@bp.route('/capture')
def capture():
    # Use the current app context
    with current_app.app_context():
        read_n_values(n=10)
    return redirect(url_for('controllers.home'))