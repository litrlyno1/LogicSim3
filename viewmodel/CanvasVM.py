from PySide6.QtCore import Signal, Slot, QObject, QPointF
from typing import Dict

from viewmodel.ConnectionVM import ConnectionVM
from viewmodel.CircuitComponentVM import CircuitComponentVM
from viewmodel.ComponentVM import ComponentVM
from viewmodel.PinVM import PinVM

class CanvasVM(QObject):
    """View-model representing the canvas containing components and connections.

    ``CanvasVM`` manages all component and connection view-models on a canvas,
    exposing signals for creation, removal, position updates, and value changes.
    It acts as the central hub for coordinating the UI layer with component
    and connection state changes.
    """

    #: Signal emitted when a generic component is added.
    #: Args: id (str), type (str), pos (QPointF)
    componentAdded = Signal(str, str, QPointF)

    #: Signal emitted when a circuit component (with pins) is added.
    #: Args: id (str), type (str), pos (QPointF), input pin IDs (list),
    #:       output pin IDs (list), initial value (bool)
    circuitComponentAdded = Signal(str, str, QPointF, list, list, bool)

    #: Signal emitted when a component is removed.
    #: Args: id (str)
    componentRemoved = Signal(str)

    #: Signal emitted when a component’s position changes.
    #: Args: id (str), new position (QPointF)
    componentPosUpdated = Signal(str, QPointF)

    #: Signal emitted when a connection is added.
    #: Args: id (str), parent pin ID pair 1 (tuple), parent pin ID pair 2 (tuple)
    connectionAdded = Signal(str, tuple, tuple)

    #: Signal emitted when a connection is removed.
    #: Args: id (str)
    connectionRemoved = Signal(str)

    #: Signal emitted when a component’s value changes.
    #: Args: id (str), new value (bool)
    componentValueUpdated = Signal(str, bool)

    #: Signal emitted when a connection’s value changes.
    #: Args: id (str), new value (bool)
    connectionValueUpdated = Signal(str, bool)

    def __init__(self):
        """Initialize the canvas view-model."""
        super().__init__()
        self._components: Dict[str, ComponentVM] = dict()
        self._connections: Dict[str, ConnectionVM] = dict()

    def addComponent(self, component: ComponentVM):
        """Add a component to the canvas.

        Args:
            component (ComponentVM): The component view-model to add.

        Behavior:
            - Registers listeners for position and value changes.
            - Emits the appropriate signal depending on component type.
        """
        self._components[component.id] = component
        component.posChanged.connect(lambda id, pos: self.componentPosUpdated.emit(id, pos))
        if isinstance(component, CircuitComponentVM):
            component.valueChanged.connect(lambda id, value: self.componentValueUpdated.emit(id, value))
            self.circuitComponentAdded.emit(
                component.id,
                component.type,
                component.pos,
                component.inputPinIds,
                component.outputPinIds,
                component.value
            )
        else:
            self.componentAdded.emit(component.id, component.type, component.pos)

    def removeComponent(self, component: ComponentVM):
        """Remove a component from the canvas.

        Args:
            component (ComponentVM): The component view-model to remove.

        Behavior:
            - Disconnects all signals.
            - Removes the component from the internal registry.
            - Emits ``componentRemoved``.
        """
        self._components.pop(component.id)
        component.posChanged.disconnect()
        if isinstance(component, CircuitComponentVM):
            component.valueChanged.disconnect()
        self.componentRemoved.emit(component.id)

    def addConnection(self, connection: ConnectionVM):
        """Add a connection to the canvas.

        Args:
            connection (ConnectionVM): The connection view-model to add.

        Behavior:
            - Connects the underlying pins.
            - Registers value change listeners.
            - Emits ``connectionAdded``.
        """
        self._connections[connection.id] = connection
        connection.connect()
        connection.valueChanged.connect(lambda id, value: self.connectionValueUpdated.emit(id, value))
        self.connectionAdded.emit(connection.id, connection.parentPinIdPair1, connection.parentPinIdPair2)

    def removeConnection(self, connection: ConnectionVM):
        """Remove a connection from the canvas.

        Args:
            connection (ConnectionVM): The connection view-model to remove.

        Behavior:
            - Disconnects the underlying pins.
            - Disconnects value change signals.
            - Removes the connection from the internal registry.
            - Emits ``connectionRemoved``.
        """
        connection.disconnect()
        connection.valueChanged.disconnect()
        self._connections.pop(connection.id)
        self.connectionRemoved.emit(connection.id)

    @property
    def components(self) -> Dict[str, ComponentVM]:
        """Dict[str, ComponentVM]: Mapping of component IDs to component view-models."""
        return self._components

    @property
    def connections(self) -> Dict[str, ConnectionVM]:
        """Dict[str, ConnectionVM]: Mapping of connection IDs to connection view-models."""
        return self._connections