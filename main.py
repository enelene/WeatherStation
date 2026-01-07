import random
import time
from weather_monitoring.station import WeatherStation
from weather_monitoring.observers import (
    WeatherDisplay,
    TemperatureAlert,
    WindSpeedAlert,
    HumidityAlert,
)


def run_simulation() -> None:
    station = WeatherStation()

    # Initial Observer
    display = WeatherDisplay()
    station.register_observer(display)

    # Pre-create observers with specific thresholds to match example
    temp_alert = TemperatureAlert(threshold=32.0)
    wind_alert = WindSpeedAlert()
    humidity_alert = HumidityAlert(threshold=85.0)

    # Simulation settings
    weeks = 20

    for week in range(1, weeks + 1):
        print(f"Week {week}:")

        # Dynamic Adding logic based on week number
        if week == 4:
            print("Adding: TemperatureAlert")
            station.register_observer(temp_alert)

        if week == 5:
            print("Adding: WindSpeedAlert")
            station.register_observer(wind_alert)

        if week == 6:
            print("Adding: HumidityAlert")
            station.register_observer(humidity_alert)

        # Set measurements based on week
        if week == 1:
            t, h, w = 28.0, 70.0, 12.0
        elif week == 2:
            t, h, w = 30.0, 72.0, 15.0
        elif week == 3:
            t, h, w = 32.0, 74.0, 18.0
        else:
            t = float(random.randint(20, 45))
            h = float(random.randint(40, 95))
            w = float(random.randint(10, 35))

        # Update Station (this triggers all notifications)
        station.set_measurements(t, h, w)

        # Dynamic Removing logic - AFTER measurements
        if week == 8:
            print("Removing: HumidityAlert")
            station.remove_observer(humidity_alert)

        print("---")
        time.sleep(0.1)


if __name__ == "__main__":
    run_simulation()
