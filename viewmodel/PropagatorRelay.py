from model.Propagator import Propagator

from viewmodel.PropagatorObserver import PropagatorObserver
from viewmodel.ObjectProperty import ObjectProperty

from PySide6.QtCore import QObject, Signal

class PropagatorRelay(ObjectProperty):
    """Qt relay object that emits signals when a propagator value changes.

    ``PropagatorRelay`` uses a :class:`PropagatorObserver` to watch a
    model-side :class:`Propagator`. When the propagator updates, the relay
    emits a Qt signal with the new value.
    """

    #: Signal emitted when the propagator's value changes.
    #: Arguments:
    #:     str: The ID of the parent object.
    #:     bool: The updated value.
    valueChanged = Signal(str, bool)

    def __init__(self, parentId: str, propagator: Propagator):
        """Initialize the relay.

        Args:
            parentId (str): The ID of the parent object.
            propagator (Propagator): The propagator whose value is observed.
        """
        super().__init__(parentId)
        self._propagatorObserver = PropagatorObserver(self, propagator)

    def onValueChange(self, value: bool) -> None:
        """Emit the valueChanged signal.

        Args:
            value (bool): The new value from the propagator.
        """
        self.valueChanged.emit(self._parentId, value)