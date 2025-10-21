# applications/serial_reader.py

import serial, time
from applications.database import db
from applications.models import SensorReading

def read_n_values(port="COM4", baudrate=9600, n=10):
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        print(f"Connected to {port} at {baudrate} baud.")
    except serial.SerialException:
        print(f"Could not open port {port}")
        return []

    time.sleep(2)  # wait for Arduino reset

    readings = []
    for _ in range(n):
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
                    readings.append({
                        "temperature": temp,
                        "humidity": hum,
                        "air_index": air_index,
                        "lux": lux
                    })
                    print(f"Saved: {temp}°C, {hum}%, {air_index}, {lux} lx")

        except Exception as e:
            print("Error reading serial data:", e)
    return readings