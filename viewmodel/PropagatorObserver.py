from PySide6.QtCore import Signal, QObject

from model.Observer import Observer
from model.Propagator import Propagator

class PropagatorObserver(Observer):
    """Observer that forwards propagator updates to a Qt parent object.

    ``PropagatorObserver`` listens to updates from a :class:`Propagator`
    instance and calls the parent's ``onValueChange`` method whenever the
    propagator's value changes. This allows model-side propagation logic
    to be bridged into Qt signals at the view/view-model layer.
    """

    def __init__(self, parent: QObject, propagator: Propagator):
        """Initialize the observer.

        Args:
            parent (QObject): The Qt object that receives value updates.
                Must implement ``onValueChange(value: bool)``.
            propagator (Propagator): The propagator being observed.
        """
        self._parent = parent
        self._propagator = propagator
        self._propagator.attach(self)

    def update(self) -> None:
        """Forward the propagator's updated value to the parent."""
        self._parent.onValueChange(self._propagator.value)

    @property
    def propagator(self) -> Propagator:
        """Propagator: The observed propagator instance."""
        return self._propagator