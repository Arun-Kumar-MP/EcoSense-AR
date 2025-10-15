# app.py
from flask import Flask
from applications.database import db
from applications.models import SensorReading

def create_app():
    app = Flask(__name__)
    app.debug = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Sensor_Readings.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Add shell context here
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'SensorReading': SensorReading}

    # Import and register the blueprint here
    from applications.controllers import bp
    app.register_blueprint(bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)