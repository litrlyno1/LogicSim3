from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """Abstract base class for observers in the Observer pattern.

    Classes inheriting from ``Observer`` must implement the :meth:`update`
    method, which will be invoked whenever the observable they are attached to
    emits a notification.
    """

    @abstractmethod
    def update(self, **kwargs) -> None:
        """Handle an update notification from an observable.

        Args:
            **kwargs: Arbitrary keyword arguments provided by the observable
                during notification.
        """
        ...


class Observable:
    """Class representing the observable in the Observer pattern.

    ``Observable`` maintains a list of observers and provides methods to attach,
    detach, and notify them of changes.
    """

    def __init__(self):
        """Initialize the observable with an empty observer list."""
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer if it is not already registered.

        Args:
            observer (Observer): The observer to attach.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach a previously registered observer.

        Args:
            observer (Observer): The observer to remove.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, **kwargs) -> None:
        """Notify all attached observers of an update.

        Args:
            **kwargs: Arbitrary data to forward to each observer's ``update`` method.
        """
        for observer in self._observers:
            observer.update(**kwargs)