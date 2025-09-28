from LogicGate import LogicGate
from Observer import Observer, SignalPropagator
from abc import abstractmethod
from Interfaces import ISignalSource, IConnectable
from __future__ import annotations

class Pin(ISignalSource, IConnectable, Observer):
    def __init__(self, gate: LogicGate, propagator : SignalPropagator = None):
        super().__init__()
        self.gate = gate
        self._propagator = propagator
    
    def notifyChange(self):
        self._propagator.propagate()
    
    def onChange(self):
        self.notifyChange()

class InputPin(Pin):
    def __init__(self, gate, index, propagator : SignalPropagator):
        super().__init__(gate, propagator)
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
    def __init__(self, gate, propagator : SignalPropagator = None):
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
    def __init__(self, inputPin = None, outputPin = None, propagator : SignalPropagator = None):
        self._inputPin = inputPin
        self._outputPin = outputPin
        self._propagator = propagator
    
    def getOutput(self):
        return self._inputPin.getOutput()

    def dispose(self):
        self._inputPin.disconnect(self)
        self._outputPin.disconnect()
    
    @classmethod
    def connect(cls, pin1: Pin, pin2: Pin):
        if cls.isValidPair(pin1, pin2):
            if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
                conn = cls(inputPin = pin2, outputPin = pin1)
            elif isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
                conn = cls(inputPin = pin1, outputPin = pin2)
            #roles are reversed for connections: inputPins in LogicGates are outputPins in connections and vice versa
            
            pin1.connect(conn)
            pin2.connect(conn)
            return conn
    
    @staticmethod
    def isValidPair(pin1: Pin, pin2: Pin) -> bool:
        if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin) or isinstance(pin1, InputPin) and isinstance(pin2, OutputPin):
            return True
        else:
            return False
    
    def notifyChange(self):
        self._propagator.propagate()
    
    def onChange(self):
        self.notifyChange()