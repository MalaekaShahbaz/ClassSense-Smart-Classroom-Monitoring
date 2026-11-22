
"""
ClassSense - Smart Classroom Monitoring System
File: simulator.py

Generate simulated classroom temperature and humidity
readings for development and testing without a DHT11 sensor.

These readings are synthetic, NOT real sensor measurements.
"""

import random
import time
from datetime import datetime


def generate_reading():
    """Generate one simulated DHT11-style reading."""

    temperature = round(random.uniform(18.0, 30.0), 1)
    humidity = round(random.uniform(35.0, 75.0), 1)

    return {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "temperature": temperature,
        "humidity": humidity,
        "source": "simulation",
    }


def check_conditions(temperature, humidity):
    """Return basic classroom environmental alerts."""

    alerts = []

    if temperature > 27:
        alerts.append("High classroom temperature")
    elif temperature < 18:
        alerts.append("Low classroom temperature")

    if humidity > 70:
        alerts.append("High humidity")
    elif humidity < 30:
        alerts.append("Low humidity")

    return alerts


def run_simulation(number_of_readings=5, interval=2):
    """Generate and display simulated classroom readings."""

    print("\n======================================")
    print(" ClassSense - Classroom Monitoring")
    print(" Mode: SIMULATION")
    print("======================================\n")

    for reading_number in range(1, number_of_readings + 1):
        reading = generate_reading()

        print(f"Reading {reading_number}")
        print(f"Time: {reading['timestamp']}")
        print(f"Temperature: {reading['temperature']} °C")
        print(f"Humidity: {reading['humidity']} %")
        print(f"Source: {reading['source']}")

        alerts = check_conditions(
            reading["temperature"],
            reading["humidity"]
        )

        if alerts:
            for alert in alerts:
                print(f"ALERT: {alert}")
        else:
            print("Status: No threshold alerts")

        print("--------------------------------------")

        if reading_number < number_of_readings:
            time.sleep(interval)

    print("\nSimulation completed successfully.")


if __name__ == "__main__":
    run_simulation()
