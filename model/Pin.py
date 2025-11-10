from __future__ import annotations
from typing import Optional, Tuple, List
from abc import ABC, abstractmethod
import weakref

from model.Propagator import Propagator

class Pin(Propagator, ABC):
    def __init__(self, parent : "CircuitComponent"):
        super().__init__()
        self._parent = weakref.ref(parent)
    
    @property
    def parent(self) -> "CircuitComponent":
        return self._parent

    @property
    @abstractmethod
    def type(self) -> str:
        pass

class InputPin(Pin):
    type = "InputPin"
    
    def __init__(self, parent : "CircuitComponent"):
        super().__init__(parent)
        self.attach(parent)
        self._connection = None
    
    @property
    def connection(self) -> Optional[Connection]:
        return self._connection

    def connect(self, conn : Connection) -> None:
        self._connection = conn
        self._connection.attach(self)
        self.update()
    
    def disconnect(self) -> None:
        if self._connection:
            self._connection.detach(self)
        self._connection = None
        self.update()
    
    def _evaluate(self) -> None:
        self._value = self._connection.value if self._connection else False
        print(f"Input Pin evaluated, value {self._value}")

class OutputPin(Pin):
    type = "OutputPin"
    
    def __init__(self, parent : "CircuitComponent"):
        super().__init__(parent)
        parent.attach(self)
        self._connections: List[Connection] = []

    @property
    def connections(self) -> List[Connection]:
        return self._connections
    
    def connect(self, conn: Connection) -> None:
        self._connections.append(conn)
        self.attach(conn)
    
    def disconnect(self, conn: Connection) -> None:
        self.detach(conn)
        self._connections.remove(conn)
    
    def _evaluate(self) -> None:
        self._value = self._parent().value
        print(f"Output Pin evaluated, value {self._value}")

#connection is an additional layer for pins interacting with each other
class Connection(Propagator):
    type = "Connection"
    
    def __init__(self, source : Pin = None, target : Pin = None):
        super().__init__()
        self._source = weakref.ref(source)
        self._target = weakref.ref(target)
        print(self._source())
        print(self._target())
        self.connect()
    
    def _evaluate(self) -> None:
        self._value = self._source().value
        print(f"Connection evaluated, value {self._value}")
    
    def connect(self):
        self._source().connect(self)
        self.update()
        self._target().connect(self)
    
    def disconnect(self):
        self._source().disconnect(self)
        self.update()
        self._target().disconnect()
    
    @classmethod 
    def create(cls, pin1: Pin, pin2: Pin) -> Optional[Connection]:
        if Connection.canConnect(pin1, pin2):
            sourcePin, targetPin = Connection._order(pin1, pin2)
            connection = cls(sourcePin, targetPin)
            return connection
        else: 
            print("Model: Connection impossible to create")
            return None
    
    @staticmethod
    def _order(pin1 : Pin, pin2 : Pin) -> Tuple[OutputPin, InputPin]:
        if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
            sourcePin = pin2
            targetPin = pin1
        elif isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
            sourcePin = pin1
            targetPin = pin2
        return sourcePin, targetPin

    @staticmethod
    def _createsCycle(sourcePin : OutputPin, targetPin : InputPin) -> bool:
        return targetPin.parent().precedes(sourcePin.parent())
    
    @staticmethod
    def canConnect(pin1 : Pin, pin2 : Pin) -> bool:
        if not pin1.parent == pin2.parent and not pin1.type == pin2.type:
            sourcePin, targetPin = Connection._order(pin1, pin2)
            if not Connection._createsCycle(sourcePin, targetPin):
                return True
        return False