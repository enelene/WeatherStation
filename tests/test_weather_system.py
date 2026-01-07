import unittest
from io import StringIO
import sys
from weather_monitoring.station import WeatherStation
from weather_monitoring.observers import TemperatureAlert, WindSpeedAlert

class TestWeatherStation(unittest.TestCase):
    def setUp(self) -> None:
        self.station = WeatherStation()

    def test_observer_registration_and_notification(self) -> None:
        """Test that registered observers receive updates."""
        
        # Create a mock observer using a simple list to capture data
        class MockObserver:
            def __init__(self) -> None:
                self.data = None
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
        self.assertEqual(observer.call_count, 1) # Should not have increased

class TestWindSpeedAlert(unittest.TestCase):
    def test_wind_speed_increase_alert(self) -> None:
        """Test that the alert triggers only on increase."""
        alert = WindSpeedAlert()
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        # First update - just stores history, no comparison possible yet
        alert.update(20, 50, 10) 
        
        # Second update - Increase (10 -> 15)
        alert.update(20, 50, 15)
        
        # Third update - Decrease (15 -> 12)
        alert.update(20, 50, 12)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("10 km/h → 15 km/h", output)
        self.assertNotIn("15 km/h → 12 km/h", output)
class TestTemperatureAlert(unittest.TestCase):
    def test_threshold_trigger(self) -> None:
        """Test that temperature alert triggers above threshold."""
        alert = TemperatureAlert()
        # Force a known threshold for testing
        alert._threshold = 30.0
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Below threshold
        alert.update(29.0, 50, 10)
        # Above threshold
        alert.update(31.0, 50, 10)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Alert! Temperature exceeded 30.0°C: 31.0°C", output)
        self.assertNotIn("29.0°C", output)

if __name__ == "__main__":
    unittest.main()