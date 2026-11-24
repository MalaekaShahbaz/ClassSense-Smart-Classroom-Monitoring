
"""
ClassSense - Smart Classroom Monitoring System
File: app.py

Flask web application for displaying classroom
temperature and humidity readings.

Currently uses simulated DHT11 sensor readings.
"""

from flask import Flask, render_template, jsonify
from backend.sensor import ClassroomSensor

# Create Flask application
app = Flask(__name__)

# Initialise sensor in simulation mode
sensor = ClassroomSensor(mode="simulation")


# Main dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# API for temperature and humidity readings
@app.route("/api/readings")
def readings():
    try:
        # Get reading from existing sensor interface
        reading = sensor.read()

        return jsonify({
            "temperature": reading["temperature"],
            "humidity": reading["humidity"],
            "source": reading.get("source", "simulation"),
            "status": "active"
        })

    except Exception as error:
        app.logger.error("Sensor error: %s", error)

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve sensor reading"
        }), 500


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
