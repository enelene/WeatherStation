import random
from typing import Optional
from weather_monitoring.interfaces import Observer

class WeatherDisplay(Observer):
    """Simply displays the current weather data."""
    
    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        print(f"WeatherDisplay: Showing Temperature = {temperature}°C, "
              f"Humidity = {humidity}%, Wind Speed = {wind_speed} km/h")


class TemperatureAlert(Observer):
    """Alerts if temperature exceeds a random threshold."""
    
    def __init__(self) -> None:
        self._threshold: float = float(random.randint(25, 40))
    
    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if temperature > self._threshold:
            print(f"TemperatureAlert: **Alert! Temperature exceeded {self._threshold}°C: {temperature}°C**")


class HumidityAlert(Observer):
    """Alerts if humidity exceeds a random threshold."""
    
    def __init__(self) -> None:
        self._threshold: float = float(random.randint(60, 90))

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if humidity > self._threshold:
            print(f"HumidityAlert: **Alert! Humidity exceeded {self._threshold}%: {humidity}%**")


class WindSpeedAlert(Observer):
    """Alerts if there is an upward trend in wind speed."""
    
    def __init__(self) -> None:
        self._last_wind_speed: Optional[float] = None

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if self._last_wind_speed is not None:
            if wind_speed > self._last_wind_speed:
                print(f"WindSpeedAlert: **Alert! Wind speed is increasing: "
                      f"{self._last_wind_speed} km/h → {wind_speed} km/h**")
            else:
                print("WindSpeedAlert: No alert (No upward trend detected)")
        
        self._last_wind_speed = wind_speed