from typing import Optional
from weather_monitoring.interfaces import Observer
from weather_monitoring.observers import (
    WeatherDisplay,
    TemperatureAlert,
    WindSpeedAlert,
    HumidityAlert,
)


class ObserverFactory:
    """
    Factory class for creating weather observers.
    
    This factory provides a centralized way to create observers with
    proper configuration, making it easier to manage observer creation
    and maintain consistency across the application.
    """

    @staticmethod
    def create_display() -> Observer:
        """
        Create a weather display observer.

        Returns:
            A new WeatherDisplay instance
        """
        return WeatherDisplay()

    @staticmethod
    def create_temperature_alert(threshold: Optional[float] = None) -> Observer:
        """
        Create a temperature alert observer.

        Args:
            threshold: Temperature threshold in Celsius, or None for random

        Returns:
            A new TemperatureAlert instance
        """
        return TemperatureAlert(threshold=threshold)

    @staticmethod
    def create_humidity_alert(threshold: Optional[float] = None) -> Observer:
        """
        Create a humidity alert observer.

        Args:
            threshold: Humidity threshold percentage, or None for random

        Returns:
            A new HumidityAlert instance
        """
        return HumidityAlert(threshold=threshold)

    @staticmethod
    def create_wind_speed_alert() -> Observer:
        """
        Create a wind speed alert observer.

        Returns:
            A new WindSpeedAlert instance
        """
        return WindSpeedAlert()

    @staticmethod
    def create_all_alerts(
        temp_threshold: float = 32.0, humidity_threshold: float = 85.0
    ) -> list[Observer]:
        """
        Create all alert observers with specified thresholds.

        Args:
            temp_threshold: Temperature threshold in Celsius
            humidity_threshold: Humidity threshold percentage

        Returns:
            List containing all alert observer instances
        """
        return [
            ObserverFactory.create_temperature_alert(threshold=temp_threshold),
            ObserverFactory.create_wind_speed_alert(),
            ObserverFactory.create_humidity_alert(threshold=humidity_threshold),
        ]

    @staticmethod
    def create_default_observers() -> list[Observer]:
        """
        Create default set of observers for typical monitoring setup.

        Returns:
            List containing display and all alert observers
        """
        observers = [ObserverFactory.create_display()]
        observers.extend(ObserverFactory.create_all_alerts())
        return observers