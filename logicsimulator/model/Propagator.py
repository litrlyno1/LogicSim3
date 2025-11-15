from abc import ABC, abstractmethod
from logicsimulator.model.Observer import Observer, Observable

class Propagator(Observer, Observable, ABC):
    """Abstract base class for components that propagate state changes.

    ``Propagator`` acts as both an :class:`Observer` and an :class:`Observable`.
    It receives updates from other objects, evaluates its own state, and then
    notifies its observers. Subclasses must implement the :meth:`_evaluate`
    method, which updates the internal value based on the component's logic.

    Attributes:
        value (bool): The current boolean value after evaluation.
    """

    def __init__(self):
        """Initialize the propagator with a default value of ``False``."""
        super().__init__()
        self._value = False

    @property
    def value(self) -> bool:
        """The current output value of the propagator.

        Returns:
            bool: The evaluated boolean value.
        """
        return self._value

    def update(self) -> None:
        """React to an update from an observed object.

        When invoked, the propagator evaluates its new state and notifies its
        observers of the updated value.
        """
        self._evaluate()
        self.notify()

    @abstractmethod
    def _evaluate(self) -> None:
        """Evaluate the internal state of the propagator.

        Subclasses must implement this method to update ``self._value`` based on
        their specific logic.
        """
        pass