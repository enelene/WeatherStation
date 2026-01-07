from typing import List
from weather_monitoring.interfaces import Observer, Subject


class WeatherStation(Subject):
    """
    Weather monitoring station that maintains weather measurements and notifies observers.

    This class implements the Subject interface from the Observer pattern. It stores
    current weather data (temperature, humidity, wind speed) and notifies all registered
    observers whenever the measurements are updated.

    Attributes:
        _observers: List of registered observers that receive notifications
        _temperature: Current temperature in Celsius
        _humidity: Current humidity percentage
        _wind_speed: Current wind speed in km/h

    Example:
        >>> station = WeatherStation()
        >>> display = WeatherDisplay()
        >>> station.register_observer(display)
        >>> station.set_measurements(25.0, 60.0, 15.0)
        WeatherDisplay: Showing Temperature = 25.0°C, Humidity = 60.0%, Wind Speed = 15.0 km/h
    """

    def __init__(self) -> None:
        """Initialize the weather station with empty observer list and zero measurements."""
        self._observers: List[Observer] = []
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._wind_speed: float = 0.0

    def register_observer(self, observer: Observer) -> None:
        """
        Register an observer to receive weather updates.

        Args:
            observer: The observer to register. Must implement Observer interface.

        Note:
            If the observer is already registered, this method has no effect.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        """
        Remove an observer from receiving weather updates.

        Args:
            observer: The observer to remove.

        Note:
            If the observer is not registered, this method has no effect.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self) -> None:
        """
        Notify all registered observers of the current weather measurements.

        This method calls the update() method on each registered observer,
        passing the current temperature, humidity, and wind speed.
        """
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._wind_speed)

    def set_measurements(
        self, temperature: float, humidity: float, wind_speed: float
    ) -> None:
        """
        Update weather measurements and notify all observers.

        Args:
            temperature: Temperature in Celsius
            humidity: Humidity as a percentage (0-100)
            wind_speed: Wind speed in km/h

        Note:
            This method automatically triggers notification to all observers.
        """
        self._temperature = temperature
        self._humidity = humidity
        self._wind_speed = wind_speed
        self.notify_observers()
