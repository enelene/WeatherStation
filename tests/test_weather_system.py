import unittest
from io import StringIO
import sys
from typing import Optional
from weather_monitoring.station import WeatherStation
from weather_monitoring.observers import (
    WeatherDisplay,
    TemperatureAlert,
    WindSpeedAlert,
    HumidityAlert,
)
from weather_monitoring.factory import ObserverFactory


class TestWeatherStation(unittest.TestCase):
    def setUp(self) -> None:
        self.station = WeatherStation()

    def test_observer_registration_and_notification(self) -> None:
        """Test that registered observers receive updates."""

        class MockObserver:
            def __init__(self) -> None:
                self.data: Optional[tuple[float, float, float]] = None

            def update(self, t: float, h: float, w: float) -> None:
                self.data = (t, h, w)

        observer = MockObserver()
        self.station.register_observer(observer)

        self.station.set_measurements(25.0, 60.0, 10.0)
        self.assertEqual(observer.data, (25.0, 60.0, 10.0))

    def test_remove_observer(self) -> None:
        """Test that removed observers do not receive updates."""

        class MockObserver:
            def __init__(self) -> None:
                self.call_count = 0

            def update(self, t: float, h: float, w: float) -> None:
                self.call_count += 1

        observer = MockObserver()
        self.station.register_observer(observer)
        self.station.set_measurements(10, 10, 10)
        self.assertEqual(observer.call_count, 1)

        self.station.remove_observer(observer)
        self.station.set_measurements(20, 20, 20)
        self.assertEqual(observer.call_count, 1)

    def test_duplicate_observer_registration(self) -> None:
        """Test that same observer cannot be registered twice."""

        class MockObserver:
            def __init__(self) -> None:
                self.call_count = 0

            def update(self, t: float, h: float, w: float) -> None:
                self.call_count += 1

        observer = MockObserver()
        self.station.register_observer(observer)
        self.station.register_observer(observer)

        self.station.set_measurements(10, 10, 10)
        self.assertEqual(observer.call_count, 1)

    def test_multiple_observers(self) -> None:
        """Test that multiple observers all receive notifications."""

        class MockObserver:
            def __init__(self) -> None:
                self.data: Optional[tuple[float, float, float]] = None

            def update(self, t: float, h: float, w: float) -> None:
                self.data = (t, h, w)

        obs1 = MockObserver()
        obs2 = MockObserver()
        obs3 = MockObserver()

        self.station.register_observer(obs1)
        self.station.register_observer(obs2)
        self.station.register_observer(obs3)

        self.station.set_measurements(30.0, 70.0, 15.0)

        self.assertEqual(obs1.data, (30.0, 70.0, 15.0))
        self.assertEqual(obs2.data, (30.0, 70.0, 15.0))
        self.assertEqual(obs3.data, (30.0, 70.0, 15.0))

    def test_invalid_temperature_too_low(self) -> None:
        """Test that temperature below -100°C raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.station.set_measurements(-101.0, 50.0, 10.0)
        self.assertIn("Temperature", str(context.exception))

    def test_invalid_temperature_too_high(self) -> None:
        """Test that temperature above 100°C raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.station.set_measurements(101.0, 50.0, 10.0)
        self.assertIn("Temperature", str(context.exception))

    def test_invalid_humidity_too_low(self) -> None:
        """Test that negative humidity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.station.set_measurements(25.0, -1.0, 10.0)
        self.assertIn("Humidity", str(context.exception))

    def test_invalid_humidity_too_high(self) -> None:
        """Test that humidity above 100% raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.station.set_measurements(25.0, 101.0, 10.0)
        self.assertIn("Humidity", str(context.exception))

    def test_invalid_wind_speed_negative(self) -> None:
        """Test that negative wind speed raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.station.set_measurements(25.0, 50.0, -1.0)
        self.assertIn("Wind speed", str(context.exception))

    def test_valid_boundary_values(self) -> None:
        """Test that boundary values are accepted."""
        # Should not raise any exceptions
        self.station.set_measurements(-100.0, 0.0, 0.0)
        self.station.set_measurements(100.0, 100.0, 0.0)
        self.station.set_measurements(0.0, 50.0, 200.0)


class TestWeatherDisplay(unittest.TestCase):
    def test_display_output_format(self) -> None:
        """Test that display shows correct format without decimal points."""
        display = WeatherDisplay()

        captured_output = StringIO()
        sys.stdout = captured_output

        display.update(25.5, 65.3, 12.8)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should format as integers
        self.assertIn("25°C", output)
        self.assertIn("65%", output)
        self.assertIn("12 km/h", output)
        # Should NOT contain decimal points
        self.assertNotIn("25.5", output)
        self.assertNotIn("65.3", output)

    def test_display_zero_values(self) -> None:
        """Test display with zero values."""
        display = WeatherDisplay()

        captured_output = StringIO()
        sys.stdout = captured_output

        display.update(0.0, 0.0, 0.0)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("0°C", output)
        self.assertIn("0%", output)
        self.assertIn("0 km/h", output)


class TestTemperatureAlert(unittest.TestCase):
    def test_threshold_trigger(self) -> None:
        """Test that temperature alert triggers above threshold."""
        alert = TemperatureAlert(threshold=30.0)

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(29.0, 50, 10)
        alert.update(31.0, 50, 10)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Alert! Temperature exceeded 30°C: 31°C", output)
        self.assertNotIn("29°C", output)

    def test_threshold_equality_no_alert(self) -> None:
        """Test that alert doesn't trigger at exactly threshold."""
        alert = TemperatureAlert(threshold=30.0)

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(30.0, 50, 10)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertEqual(output, "")

    def test_default_random_threshold(self) -> None:
        """Test that default threshold is within expected range."""
        alert = TemperatureAlert()
        self.assertGreaterEqual(alert._threshold, 25.0)
        self.assertLessEqual(alert._threshold, 40.0)

    def test_extreme_temperature_values(self) -> None:
        """Test with extreme temperature values."""
        alert = TemperatureAlert(threshold=30.0)

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(100.0, 50, 10)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("100°C", output)


class TestHumidityAlert(unittest.TestCase):
    def test_threshold_trigger(self) -> None:
        """Test that humidity alert triggers above threshold."""
        alert = HumidityAlert(threshold=75.0)

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(25, 74.0, 10)
        alert.update(25, 76.0, 10)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Alert! Humidity exceeded 75%: 76%", output)
        self.assertNotIn("74%", output)

    def test_threshold_equality_triggers_alert(self) -> None:
        """Test that alert DOES trigger at exactly threshold."""
        alert = HumidityAlert(threshold=85.0)

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(25, 85.0, 10)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Alert! Humidity exceeded 85%: 85%", output)

    def test_default_random_threshold(self) -> None:
        """Test that default threshold is within expected range."""
        alert = HumidityAlert()
        self.assertGreaterEqual(alert._threshold, 60.0)
        self.assertLessEqual(alert._threshold, 90.0)

    def test_extreme_humidity_values(self) -> None:
        """Test with maximum humidity value."""
        alert = HumidityAlert(threshold=85.0)

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(25, 100.0, 10)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("100%", output)


class TestWindSpeedAlert(unittest.TestCase):
    def test_wind_speed_increase_alert(self) -> None:
        """Test that the alert triggers only on increase."""
        alert = WindSpeedAlert()

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(20, 50, 10)
        alert.update(20, 50, 15)
        alert.update(20, 50, 12)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("10 km/h → 15 km/h", output)
        self.assertIn("No alert (No upward trend detected)", output)

    def test_wind_speed_equal_no_alert(self) -> None:
        """Test that equal wind speed prints 'no alert'."""
        alert = WindSpeedAlert()

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(20, 50, 15)
        alert.update(20, 50, 15)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("No alert", output)

    def test_first_update_no_output(self) -> None:
        """Test that first update produces no output (no history)."""
        alert = WindSpeedAlert()

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(20, 50, 15)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertEqual(output, "")

    def test_continuous_increase(self) -> None:
        """Test multiple consecutive increases."""
        alert = WindSpeedAlert()

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(20, 50, 10)
        alert.update(20, 50, 15)
        alert.update(20, 50, 20)
        alert.update(20, 50, 25)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("10 km/h → 15 km/h", output)
        self.assertIn("15 km/h → 20 km/h", output)
        self.assertIn("20 km/h → 25 km/h", output)

    def test_zero_wind_speed(self) -> None:
        """Test with zero wind speed values."""
        alert = WindSpeedAlert()

        captured_output = StringIO()
        sys.stdout = captured_output

        alert.update(20, 50, 0)
        alert.update(20, 50, 0)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("No alert", output)


class TestObserverFactory(unittest.TestCase):
    def test_create_display(self) -> None:
        """Test factory creates WeatherDisplay."""
        observer = ObserverFactory.create_display()
        self.assertIsInstance(observer, WeatherDisplay)

    def test_create_temperature_alert_with_threshold(self) -> None:
        """Test factory creates TemperatureAlert with specific threshold."""
        observer = ObserverFactory.create_temperature_alert(threshold=30.0)
        self.assertIsInstance(observer, TemperatureAlert)
        self.assertEqual(observer._threshold, 30.0)

    def test_create_temperature_alert_random_threshold(self) -> None:
        """Test factory creates TemperatureAlert with random threshold."""
        observer = ObserverFactory.create_temperature_alert()
        self.assertIsInstance(observer, TemperatureAlert)
        self.assertGreaterEqual(observer._threshold, 25.0)
        self.assertLessEqual(observer._threshold, 40.0)

    def test_create_humidity_alert(self) -> None:
        """Test factory creates HumidityAlert."""
        observer = ObserverFactory.create_humidity_alert(threshold=75.0)
        self.assertIsInstance(observer, HumidityAlert)
        self.assertEqual(observer._threshold, 75.0)

    def test_create_wind_speed_alert(self) -> None:
        """Test factory creates WindSpeedAlert."""
        observer = ObserverFactory.create_wind_speed_alert()
        self.assertIsInstance(observer, WindSpeedAlert)

    def test_create_all_alerts(self) -> None:
        """Test factory creates all alert types."""
        alerts = ObserverFactory.create_all_alerts()
        self.assertEqual(len(alerts), 3)
        self.assertIsInstance(alerts[0], TemperatureAlert)
        self.assertIsInstance(alerts[1], WindSpeedAlert)
        self.assertIsInstance(alerts[2], HumidityAlert)

    def test_create_default_observers(self) -> None:
        """Test factory creates default observer set."""
        observers = ObserverFactory.create_default_observers()
        self.assertEqual(len(observers), 4)
        self.assertIsInstance(observers[0], WeatherDisplay)


class TestIntegration(unittest.TestCase):
    def test_full_simulation_scenario(self) -> None:
        """Test a complete scenario with multiple observers."""
        station = WeatherStation()
        display = WeatherDisplay()
        temp_alert = TemperatureAlert(threshold=30.0)

        station.register_observer(display)

        captured_output = StringIO()
        sys.stdout = captured_output

        # Week 1
        station.set_measurements(25.0, 60.0, 10.0)

        # Week 2 - add temperature alert
        station.register_observer(temp_alert)
        station.set_measurements(35.0, 65.0, 12.0)

        # Week 3 - remove temperature alert
        station.remove_observer(temp_alert)
        station.set_measurements(40.0, 70.0, 15.0)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify display appeared in all updates
        self.assertEqual(output.count("WeatherDisplay"), 3)

        # Verify temp alert only appeared in week 2
        self.assertEqual(output.count("TemperatureAlert"), 1)
        self.assertIn("35°C", output)

    def test_observer_removal_stops_notifications(self) -> None:
        """Test that removed observers don't receive further updates."""
        station = WeatherStation()

        class CountingObserver:
            def __init__(self) -> None:
                self.count = 0

            def update(self, t: float, h: float, w: float) -> None:
                self.count += 1

        obs = CountingObserver()
        station.register_observer(obs)

        station.set_measurements(20, 50, 10)
        self.assertEqual(obs.count, 1)

        station.set_measurements(25, 55, 12)
        self.assertEqual(obs.count, 2)

        station.remove_observer(obs)

        station.set_measurements(30, 60, 15)
        self.assertEqual(obs.count, 2)

    def test_factory_with_station(self) -> None:
        """Test using factory to create and register observers."""
        station = WeatherStation()

        # Use factory to create observers
        display = ObserverFactory.create_display()
        temp_alert = ObserverFactory.create_temperature_alert(threshold=30.0)

        station.register_observer(display)
        station.register_observer(temp_alert)

        captured_output = StringIO()
        sys.stdout = captured_output

        station.set_measurements(35.0, 60.0, 15.0)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("WeatherDisplay", output)
        self.assertIn("TemperatureAlert", output)


if __name__ == "__main__":
    unittest.main()