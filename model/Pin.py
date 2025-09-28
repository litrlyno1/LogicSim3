from LogicGate import LogicGate
from Observer import Observer
from abc import abstractmethod
from Interfaces import ISignalSource, IConnectable
from __future__ import annotations

class Pin(ISignalSource, IConnectable, Observer):
    def __init__(self, gate: LogicGate):
        super().__init__()
        self.gate = gate

class InputPin(Pin):
    def __init__(self, gate, index):
        super().__init__(gate)
        if  not (0 < index < gate._numInputs):
            raise IndexError("Wrong index when initializing ")
        self.index = index
        self._connection = None
    
    def getOutput(self):
        if self._connection is not None and self._connection.getOutput() is None:
            raise ValueError("Input pin expected output from connection, got None instead")
        return self._connection.getOutput() or False

    def connect(self, connection : Connection):
        self._connection = connection
        self.attach(connection)
        self.notifyChange()
    
    def disconnect(self):
        self._connection.detach(self)
        self.notifyChange()
        self._connection = None

class OutputPin(Pin):
    def __init__(self, gate):
        super().__init__(gate, propagator)
        self._connections = []

    def getOutput(self):
        if self.gate.getOutput() is None:
            raise ValueError("Output pin expected output from gate, got None instead")
        return self.gate.getOutput()

    def connect(self, connection : Connection):
        self._connections.append(connection)
        connection.attach(self)
        self.notifyChange()
    
    def disconnect(self, connection : Connection):
        self.detach(connection)
        connection.notifyChange()
        self._connections.remove(connection)

#connection is an additional layer for pins interacting with each other

class Connection(ISignalSource, Observer):
    def __init__(self, source = None, target = None):
        self._source = source
        self._target = target
        self._propagator = propagator
    
    def getOutput(self):
        return self._inputPin.getOutput()

    def dispose(self):
        self._inputPin.disconnect(self)
        self._outputPin.disconnect()

def ConnectionFactory():
    
    @classmethod 
    def connect(pin1: Pin, pin2: Pin):
        if isValidPair(pin1, pin2):
            if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
                conn = Connection(source = pin2, target = pin1)
            elif isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
                conn = Connection(source = pin1, target = pin2)
            
            pin1.connect(conn)
            pin2.connect(conn)
            return conn
    
    @staticmethod
    def isValidPair(pin1: Pin, pin2: Pin) -> bool:
        if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin) or isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
            return True
        else:
            return False