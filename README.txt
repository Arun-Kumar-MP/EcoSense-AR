RUN
pip install -r requirements.txt

python serial_reader.py
python app.py

DB CREATION
python
>>> from app import app, db
>>> from applications.models import SensorReading
>>> with app.app_context():
...     db.create_all()
