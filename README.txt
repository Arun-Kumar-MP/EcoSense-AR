# EcoSense-AR: Environmental Monitoring System

EcoSense-AR is a Flask-based web application for real-time environmental monitoring using Arduino sensors. The system collects temperature, humidity, and gas sensor data through serial communication and displays it in a responsive web interface.

## Features

- **Real-time Data Collection**: Continuous reading from Arduino sensors via serial communication
- **Data Storage**: SQLite database with SQLAlchemy ORM for persistent storage
- **Web Dashboard**: Clean, responsive web interface displaying sensor readings
- **Live Updates**: Real-time data visualization with automatic page refresh
- **Modular Architecture**: Well-structured Flask application with blueprints