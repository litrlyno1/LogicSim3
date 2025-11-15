from __future__ import annotations
from typing import Optional, Tuple, List
from abc import ABC, abstractmethod
import weakref

from model.Propagator import Propagator

class Pin(Propagator, ABC):
    """Abstract base class for circuit pins.

    Pins act as connection points for circuit components. Each pin is a
    propagator and can update its value based on connections or its parent
    component. Concrete pin types must define the ``type`` property.
    """

    def __init__(self, parent: "CircuitComponent"):
        """Initialize the pin.

        Args:
            parent (CircuitComponent): The parent component this pin belongs to.
        """
        super().__init__()
        self._parent = weakref.ref(parent)

    @property
    def parent(self) -> "CircuitComponent":
        """CircuitComponent: The parent component of this pin."""
        return self._parent()

    @property
    @abstractmethod
    def type(self) -> str:
        """str: Type of the pin ('InputPin' or 'OutputPin')."""
        pass

# ------------------------------------------------------------------------

class InputPin(Pin):
    """Represents an input pin of a circuit component.

    An input pin receives a value from a connected output pin through a
    :class:`Connection`. It can attach/detach from a connection and
    automatically updates its value when the connection changes.
    """

    type = "InputPin"

    def __init__(self, parent: "CircuitComponent"):
        super().__init__(parent)
        self.attach(parent)
        self._connection: Optional[Connection] = None

    @property
    def connection(self) -> Optional[Connection]:
        """Optional[Connection]: The current connection of this input pin."""
        return self._connection

    def connect(self, conn: Connection) -> None:
        """Connect the input pin to a connection.

        Args:
            conn (Connection): The connection to attach.
        """
        self._connection = conn
        self._connection.attach(self)
        self.update()

    def disconnect(self) -> None:
        """Disconnect the input pin from its connection."""
        if self._connection:
            self._connection.detach(self)
        self._connection = None
        self.update()

    def _evaluate(self) -> None:
        """Evaluate the input pin's value from the connection."""
        self._value = self._connection.value if self._connection else False

# ------------------------------------------------------------------------

class OutputPin(Pin):
    """Represents an output pin of a circuit component.

    An output pin can connect to multiple input pins. Its value is always
    the same as the parent component's value. The output pin notifies all
    attached connections when its value changes.
    """

    type = "OutputPin"

    def __init__(self, parent: "CircuitComponent"):
        super().__init__(parent)
        parent.attach(self)
        self._connections: List[Connection] = []

    @property
    def connections(self) -> List[Connection]:
        """List[Connection]: All connections attached to this output pin."""
        return self._connections

    def connect(self, conn: Connection) -> None:
        """Attach a new connection to this output pin."""
        self._connections.append(conn)
        self.attach(conn)

    def disconnect(self, conn: Connection) -> None:
        """Remove a connection from this output pin."""
        self.detach(conn)
        self._connections.remove(conn)

    def _evaluate(self) -> None:
        """Set the output value based on the parent component's value."""
        self._value = self.parent.value

# ------------------------------------------------------------------------

class Connection(Propagator):
    """Represents a connection between an output pin and an input pin.

    A connection propagates the value from the source (output pin) to
    the target (input pin). It prevents cycles in the circuit and
    provides helper methods for creating and managing connections.
    """

    type = "Connection"

    def __init__(self, source: Pin = None, target: Pin = None):
        """Initialize a connection and attach it to pins.

        Args:
            source (Pin): The source output pin.
            target (Pin): The target input pin.
        """
        super().__init__()
        self._source = weakref.ref(source)
        self._target = weakref.ref(target)
        self.connect()

    @property
    def source(self) -> OutputPin:
        """OutputPin: The source/output pin of the connection."""
        return self._source()

    @property
    def target(self) -> InputPin:
        """InputPin: The target/input pin of the connection."""
        return self._target()

    def _evaluate(self) -> None:
        """Set the connection value to match the source pin."""
        self._value = self.source.value

    def connect(self):
        """Attach the connection to the source and target pins."""
        self.source.connect(self)
        self.update()
        self.target.connect(self)

    def disconnect(self):
        """Detach the connection from both pins."""
        self.source.disconnect(self)
        self.update()
        self.target.disconnect()

    @classmethod
    def create(cls, pin1: Pin, pin2: Pin) -> Optional[Connection]:
        """Create a connection if the pins are compatible.

        Args:
            pin1 (Pin): First pin.
            pin2 (Pin): Second pin.

        Returns:
            Optional[Connection]: A new connection if pins can connect,
                otherwise None.
        """
        if Connection.canConnect(pin1, pin2):
            sourcePin, targetPin = Connection._order(pin1, pin2)
            connection = cls(sourcePin, targetPin)
            return connection
        return None

    @staticmethod
    def _order(pin1: Pin, pin2: Pin) -> Tuple[OutputPin, InputPin]:
        """Determine which pin is source and which is target.

        Args:
            pin1 (Pin): First pin.
            pin2 (Pin): Second pin.

        Returns:
            Tuple[OutputPin, InputPin]: Ordered source and target pins.
        """
        if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
            sourcePin = pin2
            targetPin = pin1
        elif isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
            sourcePin = pin1
            targetPin = pin2
        return sourcePin, targetPin

    @staticmethod
    def _createsCycle(sourcePin: OutputPin, targetPin: InputPin) -> bool:
        """Check if connecting the pins would create a cycle.

        Args:
            sourcePin (OutputPin): The proposed source pin.
            targetPin (InputPin): The proposed target pin.

        Returns:
            bool: True if a cycle would be created, False otherwise.
        """
        return targetPin.parent.precedes(sourcePin.parent)

    @staticmethod
    def canConnect(pin1: Pin, pin2: Pin) -> bool:
        """Check if two pins can be connected.

        Args:
            pin1 (Pin): First pin.
            pin2 (Pin): Second pin.

        Returns:
            bool: True if the pins can connect without creating a cycle,
                and they belong to different components.
        """
        if not pin1.parent == pin2.parent and not pin1.type == pin2.type:
            sourcePin, targetPin = Connection._order(pin1, pin2)
            if targetPin.connection is None and not Connection._createsCycle(sourcePin, targetPin):
                return True
        return False