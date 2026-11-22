
"""
ClassSense - Smart Classroom Monitoring System
File: sensor.py

Provides a common interface for simulated readings
and real DHT11 sensor readings on Raspberry Pi.
"""

from datetime import datetime

from simulator import generate_reading


class SensorError(Exception):
    """Raised when a sensor reading cannot be obtained."""


class ClassroomSensor:
    def __init__(self, mode="simulation", gpio_pin=4):
        self.mode = mode.lower()
        self.gpio_pin = gpio_pin

        if self.mode not in ("simulation", "hardware"):
            raise ValueError(
                "Sensor mode must be 'simulation' or 'hardware'."
            )

        self._device = None

    def _initialise_hardware(self):
        """Initialise the DHT11 only when hardware mode is used."""

        try:
            import board
            import adafruit_dht
        except ImportError as error:
            raise SensorError(
                "DHT11 libraries are not installed. "
                "Use simulation mode on your MacBook."
            ) from error

        if self.gpio_pin != 4:
            raise SensorError(
                "This initial implementation supports GPIO4 only."
            )

        try:
            self._device = adafruit_dht.DHT11(
                board.D4,
                use_pulseio=False
            )
        except Exception as error:
            raise SensorError(
                f"Could not initialise DHT11: {error}"
            ) from error

    def read(self):
        """Read classroom temperature and humidity."""

        if self.mode == "simulation":
            return generate_reading()

        if self._device is None:
            self._initialise_hardware()

        try:
            temperature = self._device.temperature
            humidity = self._device.humidity

            if temperature is None or humidity is None:
                raise SensorError(
                    "DHT11 returned an incomplete measurement."
                )

            return {
                "timestamp": datetime.now().astimezone().isoformat(
                    timespec="seconds"
                ),
                "temperature": float(temperature),
                "humidity": float(humidity),
                "source": "dht11",
            }

        except RuntimeError as error:
            raise SensorError(
                f"Temporary DHT11 reading error: {error}"
            ) from error

    def close(self):
        """Release hardware resources."""

        if self._device is not None:
            self._device.exit()
            self._device = None


if __name__ == "__main__":
    sensor = ClassroomSensor(mode="simulation")

    try:
        reading = sensor.read()

        print("\nClassSense - Sensor Interface Test")
        print("----------------------------------")
        print(f"Mode: {sensor.mode}")
        print(f"Timestamp: {reading['timestamp']}")
        print(f"Temperature: {reading['temperature']} °C")
        print(f"Humidity: {reading['humidity']} %")
        print(f"Source: {reading['source']}")
        print("\nSensor test completed successfully.")

    finally:
        sensor.close()
