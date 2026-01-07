from typing import Protocol, runtime_checkable


@runtime_checkable
class Observer(Protocol):
    """Interface for any part of the system that needs to receive weather updates."""

    def update(
        self, temperature: float, humidity: float, wind_speed: float
    ) -> None: ...


@runtime_checkable
class Subject(Protocol):
    """Interface for the Weather Station."""

    def register_observer(self, observer: Observer) -> None: ...

    def remove_observer(self, observer: Observer) -> None: ...

    def notify_observers(self) -> None: ...
