from LogicGate import LogicGate
from Observer import Observer, IObservable
from abc import abstractmethod
from Interfaces import ISignalSource, IConnectable
from __future__ import annotations

class Pin(Observer, IObservable, ISignalSource, IConnectable):
    def __init__(self, gate: LogicGate):
        self.gate = gate

class InputPin(Pin):
    def __init__(self, gate, index):
        super().__init__(gate)
        if gate._numInputs >= index or index < 0:
            raise IndexError("Wrong index when initializing ")
        else:
            self.index = index
        self._connections = []
    
    def getOutput(self):
        if self._connection is not None and self._connection.getOutput() is None:
            raise ValueError("Input pin expected output from connection, got None instead")
        return self._connection.getOutput() or False

    def connect(self, connection : Connection):
        self._connections.append(connection)
        self.attach(connection)
    
    def disconnect(self, connection : Connection):
        self.detach(connection)
        self._connections.remove(connection)

class OutputPin(Pin):
    def __init__(self, gate):
        super().__init__(gate)
        self._connection = None

    def getOutput(self):
        if self.gate.getOutput() is None:
            raise ValueError("Output pin expected output from gate, got None instead")
        return self.gate.getOutput()

    def connect(self, connection : Connection):
        self._connection = connection
        connection.attach(self)
    
    def disconnect(self):
        self._connection.detach(self)
        self._connection = None

class Connection(ISignalSource):
    def __init__(self, inputPin = None, outputPin = None):
        self._inputPin = inputPin
        self._outputPin = outputPin
    
    def getOutput(self):
        return self._inputPin.getOutput()

    def dispose(self):
        self._inputPin.disconnect()
        self._outputPin.disconnect()
    
    @classmethod
    def connect(cls, pin1: Pin, pin2: Pin):
        if cls.isValidPair(pin1, pin2):
            if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
                conn = cls(inputPin = pin1, outputPin = pin2)
            elif isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
                conn = cls(inputPin = pin2, outputPin = pin1)
            
            pin1.connect(conn)
            pin2.connect(conn)
            return conn
    
    @staticmethod
    def isValidPair(pin1: Pin, pin2: Pin) -> bool:
        if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin) or isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
            return True
        else:
            return False