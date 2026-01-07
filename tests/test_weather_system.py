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

        # Should trigger at exactly 85%
        self.assertIn("Alert! Humidity exceeded 85%: 85%", output)

    def test_default_random_threshold(self) -> None:
        """Test that default threshold is within expected range."""
        alert = HumidityAlert()
        self.assertGreaterEqual(alert._threshold, 60.0)
        self.assertLessEqual(alert._threshold, 90.0)


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
        self.assertEqual(obs.count, 2)  # Should not increase


if __name__ == "__main__":
    unittest.main()
