from PySide6.QtCore import Signal, QObject, Slot
import weakref

from core.idGenerator import generateId
from model.Pin import Connection
from viewmodel.PropagatorObject import PropagatorObject
from viewmodel.PinVM import PinVM
from viewmodel.CircuitComponentVM import CircuitComponentVM

class ConnectionVM(PropagatorObject):
    """View-model representation of a connection between two pins.

    ``ConnectionVM`` wraps a model-side :class:`Connection` and exposes
    its functionality to the view layer. It provides IDs, parent references,
    and convenience methods for connecting, disconnecting, and querying
    relationships with circuit components.
    """

    type = "ConnectionVM"

    def __init__(self, pinVM1: PinVM, pinVM2: PinVM):
        """Initialize a connection view-model.

        Args:
            pinVM1 (PinVM): First pin view-model of the connection.
            pinVM2 (PinVM): Second pin view-model of the connection.

        The underlying model connection is created automatically. The
        view-model also registers as a propagator for updates.
        """
        self._pinVM1 = pinVM1
        self._pinVM2 = pinVM2
        self._id = generateId(prefix="Connection")
        self._connection = Connection.create(pinVM1.pin, pinVM2.pin)
        super().__init__(id=self._id, propagator=self._connection)

    @staticmethod
    def canConnect(pinVM1: PinVM, pinVM2: PinVM) -> bool:
        """Check if two pin view-models can be connected.

        Args:
            pinVM1 (PinVM): First pin view-model.
            pinVM2 (PinVM): Second pin view-model.

        Returns:
            bool: True if the pins can be connected according to the model rules.
        """
        return Connection.canConnect(pinVM1.pin, pinVM2.pin)

    def connect(self):
        """Connect the underlying model connection."""
        self._connection.connect()

    def disconnect(self):
        """Disconnect the underlying model connection."""
        self._connection.disconnect()

    @property
    def id(self) -> str:
        """str: Unique identifier of this connection view-model."""
        return self._id

    @property
    def pinId1(self) -> str:
        """str: ID of the first pin view-model."""
        return self._pinVM1.id

    @property
    def pinId2(self) -> str:
        """str: ID of the second pin view-model."""
        return self._pinVM2.id

    @property
    def parentPinIdPair1(self) -> tuple:
        """tuple: Pair (parent component ID, pin ID) for the first pin."""
        return self._pinVM1.parentId, self._pinVM1.id

    @property
    def parentPinIdPair2(self) -> tuple:
        """tuple: Pair (parent component ID, pin ID) for the second pin."""
        return self._pinVM2.parentId, self._pinVM2.id

    def isConnectedToCircuitComponent(self, circuitComponent: CircuitComponentVM) -> bool:
        """Check if either pin is part of a given circuit component.

        Args:
            circuitComponent (CircuitComponentVM): The circuit component to check.

        Returns:
            bool: True if either end of the connection belongs to the component.
        """
        return self._pinVM1.id in circuitComponent.pins.keys() or self._pinVM2.id in circuitComponent.pins.keys()