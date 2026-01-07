Weather Monitoring System
A Python-based weather monitoring system implementing the Observer design pattern.
Overview
This system tracks weather conditions (temperature, humidity, wind speed) and automatically notifies different components when conditions change. Components can include displays, alert systems, and custom observers.
Design Pattern
The system implements the Observer Pattern:

Subject: WeatherStation maintains weather data and notifies observers
Observers: Various components (WeatherDisplay, TemperatureAlert, etc.) react to changes

Project Structure
weather_monitoring/
├── __init__.py
├── interfaces.py      # Observer and Subject protocols
├── station.py         # WeatherStation implementation
└── observers.py       # Observer implementations

tests/
└── test_weather_system.py

main.py                # Simulation runner
Features

Dynamic Observer Management: Add/remove observers at runtime
Multiple Alert Types:

Temperature alerts (threshold-based)
Humidity alerts (threshold-based)
Wind speed alerts (trend-based)


Flexible Thresholds: Random or injected thresholds for testing
Type Safety: Full type hints with mypy support

Installation
bash# Clone the repository
git clone <repository-url>
cd weather_monitoring_system

# Install dependencies (if any)
pip install -r requirements.txt
Usage
Running the Simulation
bashpython main.py
Running Tests
bashpython -m unittest discover tests

# Or with coverage
python -m pytest --cov=weather_monitoring tests/
Linting and Formatting
bash# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy weather_monitoring tests
Example
pythonfrom weather_monitoring.station import WeatherStation
from weather_monitoring.observers import WeatherDisplay, TemperatureAlert

# Create station and observers
station = WeatherStation()
display = WeatherDisplay()
alert = TemperatureAlert(threshold=30.0)

# Register observers
station.register_observer(display)
station.register_observer(alert)

# Update weather (observers are automatically notified)
station.set_measurements(35.0, 65.0, 15.0)

# Output:
# WeatherDisplay: Showing Temperature = 35.0°C, Humidity = 65.0%, Wind Speed = 15.0 km/h
# TemperatureAlert: **Alert! Temperature exceeded 30.0°C: 35.0°C**
Design Principles

Single Responsibility: Each class has one reason to change
Open/Closed: Open for extension (new observers), closed for modification
Dependency Inversion: Depends on abstractions (Observer protocol), not concrete classes
Interface Segregation: Clean, minimal interfaces

Requirements

Python 3.13+
Type hints throughout
Follows PEP 8 conventions

Testing
The project includes comprehensive tests covering:

Observer registration/removal
Alert triggering logic
Edge cases (equal values, first updates)
Integration scenarios
