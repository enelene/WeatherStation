import random
from abc import ABC
from typing import Optional
from weather_monitoring.interfaces import Observer


class WeatherDisplay(Observer):
    """Simply displays the current weather data."""

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        print(
            f"WeatherDisplay: Showing Temperature = {int(temperature)}°C, "
            f"Humidity = {int(humidity)}%, Wind Speed = {int(wind_speed)} km/h"
        )


class BaseThresholdAlert(Observer, ABC):
    """
    Base class for threshold-based alerts.
    
    This class provides common functionality for alerts that trigger
    when a measurement exceeds a threshold value.
    """

    def __init__(
        self, threshold: Optional[float], min_threshold: int, max_threshold: int
    ) -> None:
        """
        Initialize alert with threshold.

        Args:
            threshold: Specific threshold value, or None for random
            min_threshold: Minimum value for random threshold
            max_threshold: Maximum value for random threshold
        """
        self._threshold: float = (
            threshold
            if threshold is not None
            else float(random.randint(min_threshold, max_threshold))
        )

    def _format_alert(
        self, alert_type: str, value: float, unit: str, use_gte: bool = False
    ) -> str:
        """
        Format an alert message.

        Args:
            alert_type: Type of alert (e.g., "Temperature", "Humidity")
            value: Current value that triggered the alert
            unit: Unit of measurement (e.g., "°C", "%")
            use_gte: Whether threshold check uses >= instead of >

        Returns:
            Formatted alert message string
        """
        comparison = "exceeded" if not use_gte else "exceeded"
        return (
            f"{alert_type}Alert: **Alert! {alert_type} {comparison} "
            f"{int(self._threshold)}{unit}: {int(value)}{unit}**"
        )


class TemperatureAlert(BaseThresholdAlert):
    """Alerts if temperature exceeds a threshold."""

    def __init__(self, threshold: Optional[float] = None) -> None:
        super().__init__(threshold, min_threshold=25, max_threshold=40)

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if temperature > self._threshold:
            print(self._format_alert("Temperature", temperature, "°C"))


class HumidityAlert(BaseThresholdAlert):
    """Alerts if humidity exceeds or equals a threshold."""

    def __init__(self, threshold: Optional[float] = None) -> None:
        super().__init__(threshold, min_threshold=60, max_threshold=90)

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if humidity >= self._threshold:
            print(self._format_alert("Humidity", humidity, "%", use_gte=True))


class WindSpeedAlert(Observer):
    """Alerts if there is an upward trend in wind speed."""

    def __init__(self) -> None:
        self._last_wind_speed: Optional[float] = None

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if self._last_wind_speed is not None:
            if wind_speed > self._last_wind_speed:
                print(
                    f"WindSpeedAlert: **Alert! Wind speed is increasing: "
                    f"{int(self._last_wind_speed)} km/h → {int(wind_speed)} km/h**"
                )
            else:
                print("WindSpeedAlert: No alert (No upward trend detected)")

        self._last_wind_speed = wind_speed