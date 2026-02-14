# Weather Monitoring System

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Type Checking: mypy](https://img.shields.io/badge/type_checking-mypy-informational)](https://mypy-lang.org/)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-614097)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust Python-based weather monitoring system implementing the **Observer Design Pattern**. This project demonstrates scalable software architecture, loose coupling, and rigorous automated testing.



---

## Overview

This system acts as a centralized `WeatherStation` that tracks meteorological data (temperature, humidity, and wind speed). It automatically broadcasts updates to a variety of specialized `AlertSystems` (Observers) that trigger based on specific logic, such as threshold breaches or trend detection.

### Core Design Principles
* **Observer Pattern:** Decouples the subject (station) from the notification logic.
* **Factory Pattern:** Centralized creation of observers to manage complexity.
* **Dependency Injection:** Interfaces (Protocols) are used to ensure the system is easy to extend and mock during testing.
* **Single Responsibility:** Each observer handles exactly one type of alert logic.

---

## Features

* **Dynamic Observer Management:** Add or remove monitoring components at runtime without restarting the simulation.
* **Advanced Alert Logic:**
    * 🌡️ **Temperature:** Triggers when values exceed a defined threshold.
    * 💧 **Humidity:** Triggers when values meet or exceed a limit.
    * 🌬️ **Wind Speed:** Detects **increasing trends** over consecutive readings.
* **Data Integrity:** Built-in validation ensures measurements remain within realistic physical ranges.
* **Type Safety:** 100% type-hinted for better IDE support and static analysis.

---

## Project Structure

```text
weather_monitoring_system/
├── weather_monitoring/
│   ├── interfaces.py      # Observer and Subject protocols (ABC/Protocols)
│   ├── station.py         # WeatherStation core implementation
│   ├── observers.py       # Alert implementations (Temp, Humidity, Wind)
│   └── factory.py         # Factory for observer instantiation
├── tests/
│   └── test_weather_system.py  # Comprehensive test suite (30+ cases)
├── main.py                # 20-week simulation runner
├── pyproject.toml         # Tooling configuration (Ruff, Mypy)
└── README.md
