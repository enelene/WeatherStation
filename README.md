Weather Monitoring System
A Python-based weather monitoring system implementing the Observer design pattern with comprehensive testing and validation.

Overview
This system tracks weather conditions (temperature, humidity, wind speed) and automatically notifies different components when conditions change. The implementation demonstrates software design principles including the Observer pattern, dependency injection, and factory pattern.

Features
Observer Pattern Implementation: Loose coupling between weather station and observers
Dynamic Observer Management: Add/remove observers at runtime
Multiple Alert Types:
Temperature alerts (threshold-based, triggers when temperature > threshold)
Humidity alerts (threshold-based, triggers when humidity ≥ threshold)
Wind speed alerts (trend-based, detects increasing wind speed)
Input Validation: Validates all measurements are within realistic ranges
Factory Pattern: Centralized observer creation and configuration
Type Safety: Full type hints with mypy support
Comprehensive Testing: 30+ test cases covering all functionality
Project Structure

weather_monitoring_system/
'''
├── weather_monitoring/
│   ├── __init__.py
│   ├── interfaces.py      # Observer and Subject protocols
│   ├── station.py         # WeatherStation implementation
│   ├── observers.py       # Observer implementations
│   └── factory.py         # ObserverFactory for creating observers
├── tests/
│   └── test_weather_system.py  # Comprehensive test suite
├── main.py                # Simulation runner
├── README.md
├── .gitignore
└── pyproject.toml         # Project configuration
'''
Requirements
Python 3.13+
No external dependencies required for core functionality
Installation
bash
# Clone the repository
git clone <repository-url>
cd weather_monitoring_system

# No additional installation needed - uses Python standard library only
Usage
Running the Simulation
bash
python main.py
This runs a 20-week simulation with:

Weeks 1-3: Fixed weather values
Weeks 4-20: Random weather values
Dynamic observer addition (weeks 4, 5, 6)
Dynamic observer removal (week 8)
Running Tests
bash
# Run all tests with verbose output
python -m unittest discover tests -v

# Run specific test class
python -m unittest tests.test_weather_system.TestWeatherStation

# Run specific test
python -m unittest tests.test_weather_system.TestWeatherStation.test_observer_registration_and_notification
Code Quality Checks
bash
# Type checking with mypy
mypy .

# Format code with ruff
ruff format .

# Lint code with ruff
ruff check .
