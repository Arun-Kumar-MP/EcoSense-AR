# serial_reader.py

import serial
import time
from app import create_app
from applications.database import db
from applications.models import SensorReading

def read_from_serial(port="COM4", baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        print(f"Connected to {port} at {baudrate} baud.")
    except serial.SerialException:
        print(f"Could not open port {port}")
        return

    time.sleep(2)  # Wait for Arduino to reset

    app = create_app()
    with app.app_context():
        while True:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 4:
                        temp, hum, air_index, lux = map(float, parts)
                        reading = SensorReading(
                            temperature=temp,
                            humidity=hum,
                            air_index=air_index,
                            lux=lux
                        )
                        db.session.add(reading)
                        db.session.commit()
                        print(f"Saved: Temp={temp}°C, Humidity={hum}%, Air_Index={air_index}, LUX={lux}")
            except Exception as e:
                print("Error reading serial data:", e)

if __name__ == "__main__":
    read_from_serial()