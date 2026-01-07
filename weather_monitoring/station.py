from typing import List
from weather_monitoring.interfaces import Observer, Subject

class WeatherStation(Subject):
    """
    The Main System: Stores weather data and notifies observers of changes.
    """
    def __init__(self) -> None:
        self._observers: List[Observer] = []
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._wind_speed: float = 0.0

    def register_observer(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._wind_speed)

    def set_measurements(self, temperature: float, humidity: float, wind_speed: float) -> None:
        """Updates weather data and triggers notifications."""
        self._temperature = temperature
        self._humidity = humidity
        self._wind_speed = wind_speed
        self.notify_observers()
