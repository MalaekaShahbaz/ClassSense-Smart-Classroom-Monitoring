
"""
ClassSense - Smart Classroom Monitoring System
File: storage.py

Stores classroom temperature and humidity readings
in a CSV file for future analysis and visualisation.
"""

import csv
from pathlib import Path


DATA_DIRECTORY = Path(__file__).resolve().parent / "data"
CSV_FILE = DATA_DIRECTORY / "classroom_readings.csv"

FIELDNAMES = [
    "timestamp",
    "temperature",
    "humidity",
    "source",
]


def initialise_storage(file_path=CSV_FILE):
    """Create the data folder and CSV file if needed."""

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists() or file_path.stat().st_size == 0:
        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

    return file_path


def save_reading(reading, file_path=CSV_FILE):
    """Append one temperature/humidity reading to the CSV file."""

    required_fields = set(FIELDNAMES)

    if not required_fields.issubset(reading):
        missing = required_fields - set(reading)
        raise ValueError(f"Missing reading fields: {sorted(missing)}")

    temperature = float(reading["temperature"])
    humidity = float(reading["humidity"])

    if not -40 <= temperature <= 80:
        raise ValueError("Temperature is outside the supported range.")

    if not 0 <= humidity <= 100:
        raise ValueError("Humidity must be between 0 and 100%.")

    file_path = initialise_storage(file_path)

    clean_reading = {
        "timestamp": reading["timestamp"],
        "temperature": temperature,
        "humidity": humidity,
        "source": reading["source"],
    }

    with file_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(clean_reading)

    return file_path


def load_readings(file_path=CSV_FILE):
    """Read all previously saved classroom measurements."""

    file_path = Path(file_path)

    if not file_path.exists():
        return []

    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def count_readings(file_path=CSV_FILE):
    """Count how many readings are stored."""

    return len(load_readings(file_path))


if __name__ == "__main__":
    from simulator import generate_reading

    print("ClassSense - CSV Storage Test")
    print("----------------------------")

    reading = generate_reading()

    save_reading(reading)
    

    print("Reading saved successfully!")
    print(f"Timestamp: {reading['timestamp']}")
    print(f"Temperature: {reading['temperature']} °C")
    print(f"Humidity: {reading['humidity']} %")
    print(f"Source: {reading['source']}")
    print(f"\nCSV location: {CSV_FILE}")
    print(f"Total saved readings: {count_readings()}")
