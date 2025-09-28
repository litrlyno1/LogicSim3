from __future__ import annotations
from LogicGate import LogicGate
from Propagator import Propagator
from abc import abstractmethod
from Interfaces import ISignalSource, IConnectable

class Pin(Propagator, IConnectable):
    def __init__(self, gate: LogicGate):
        super().__init__()
        self.gate = gate
    
    def getOutput(self):
        ...

class InputPin(Pin):
    def __init__(self, gate, index):
        super().__init__(gate)
        if  not (0 < index < gate._numInputs):
            raise IndexError("Wrong index when initializing ")
        self.index = index
        self.connection = None
    
    def getOutput(self):
        if self.connection is not None and self.connection.getOutput() is None:
            raise ValueError("Input pin expected output from connection, got None instead")
        return self.connection.getOutput() or False

class OutputPin(Pin):
    def __init__(self, gate):
        super().__init__(gate)
        self.connections = []

    def getOutput(self):
        if self.gate.getOutput() is None:
            raise ValueError("Output pin expected output from gate, got None instead")
        return self.gate.getOutput()

#connection is an additional layer for pins interacting with each other

class Connection(Propagator, ISignalSource):
    def __init__(self, source = None, target = None):
        self._source = source
        self._target = target
    
    def getOutput(self):
        return self._source.getOutput()

    def dispose(self):
        self._source.disconnect(self)
        self._target.disconnect()

class ConnectionFactory:
    
    @classmethod 
    def connect(cls, pin1: Pin, pin2: Pin):
        if cls.isValidPair(pin1, pin2):
            if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
                sourcePin = pin2
                targetPin = pin1
            elif isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
                sourcePin = pin1
                targetPin = pin2
            
            conn = Connection(source = sourcePin, target = targetPin)
            sourcePin.connections.append(conn)
            targetPin.connection = conn
            
            return conn
    
    @staticmethod
    def isValidPair(pin1: Pin, pin2: Pin) -> bool:
        if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin) or isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
            return True
        else:
            return False