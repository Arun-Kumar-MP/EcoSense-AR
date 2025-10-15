from flask import render_template, redirect, url_for, Blueprint
from .models import SensorReading

bp = Blueprint('controllers', __name__)

@bp.route('/')
def index():
    return redirect(url_for('controllers.home'))

@bp.route('/home')
def home():
    readings = (
        SensorReading
        .query
        .order_by(SensorReading.timestamp.asc())
        .limit(50)
        .all()
    )
    return render_template('home.html', readings=readings)
