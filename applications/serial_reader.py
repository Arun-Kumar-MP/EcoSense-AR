# applications/serial_reader.py

import serial
import serial.tools.list_ports
import time
from applications.database import db
from applications.models import SensorReading

def find_arduino_port():
    """Dynamically identifies the Arduino COM port."""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # Looks for keywords associated with Arduino Nano or USB-Serial chips
        if any(key in p.description for key in ["Arduino", "USB Serial", "CH340", "CP210"]):
            print(f">>> Found hardware on: {p.device}")
            return p.device
    return None

def read_n_values(baudrate=9600, n=10):
    port = find_arduino_port()
    if not port:
        print("!!! ERROR: No hardware detected on any COM port !!!")
        return []

    try:
        with serial.Serial(port, baudrate, timeout=2) as ser:
            print(f">>> Initializing connection to {port}...")
            time.sleep(2) # Give Nano time to reset
            
            readings = []
            count = 0
            print("--- STARTING LIVE DATA STREAM ---")
            
            while count < n:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 4:
                        try:
                            t, h, a, l = map(float, parts)
                            
                            # Keep the terminal printing active
                            print(f"[RECV] Sample {count+1}: T={t}C | H={h}% | Air={a} | L={l}lx")
                            
                            new_data = SensorReading(temperature=t, humidity=h, air_index=a, lux=l)
                            db.session.add(new_data)
                            readings.append({"temperature": t, "humidity": h, "air_index": a, "lux": l})
                            count += 1
                        except ValueError:
                            continue
            
            db.session.commit()
            print("--- STREAM COMPLETE: DATA SAVED ---")
            return readings
            
    except Exception as e:
        print(f"!!! SERIAL ERROR: {e} !!!")
        return []