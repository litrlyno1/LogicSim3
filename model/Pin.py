from LogicGate import LogicGate
from Observer import Observer, Observable
from abc import abstractmethod
from Interfaces import ISignalSource, IConnectable
from __future__ import annotations

class Pin(ISignalSource, IConnectable, Observer, Observable):
    def __init__(self, gate: LogicGate):
        super().__init__()
        self.gate = gate
    
    def update(self):
        self.notify()

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

class Connection(ISignalSource, Observer, Observable):
    def __init__(self, source = None, target = None):
        self._source = source
        self._target = target
    
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
                sourcePin = pin2
                targetPin = pin1
            elif isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
                sourcePin = pin2
                targetPin = pin1
            
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