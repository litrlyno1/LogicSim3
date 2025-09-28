from __future__ import annotations
from Propagator import Propagator
from Interfaces import ISingleConnectable, IMultiConnectable

class Pin(Propagator):
    def __init__(self, gate: "LogicGate"):
        super().__init__()
        self.gate = gate

class InputPin(Pin, ISingleConnectable):
    def __init__(self, gate, index):
        super().__init__(gate)
        if not (0 <= index < gate._numInputs):
            raise IndexError("Wrong index when initializing ")
        self.index = index
        self._connection = None
        self.type = "InputPin"
    
    @property
    def connection(self):
        return self._connection
    
    def getOutput(self):
        if self._connection is not None and self._connection.getOutput() is None:
            raise ValueError("Input pin expected output from connection, got None instead")
        return self._connection.getOutput() or False

    def connect(self, conn : Connection):
        self._connection = conn
        self._connection.attach(self)
        self.update()
    
    def disconnect(self, conn : Connection):
        self._connection = None
        self._connection.detach(self)
        self.update()

class OutputPin(Pin, IMultiConnectable):
    def __init__(self, gate, index : int):
        super().__init__(gate)
        if not (0 <= index < gate._numOutputs):
            raise IndexError("Wrong index when initializing ")
        self.index = index
        self._connections: list[Connection] = []
        self.type = "OutputPin"

    @property
    def connections(self):
        return self._connections

    def getOutput(self):
        if self.gate.getOutput() is None:
            raise ValueError("Output pin expected output from gate, got None instead")
        return self.gate.getOutput()
    
    def connect(self, conn: Connection):
        self._connections.append(conn)
        self.attach(conn)
        self.update()
    
    def disconnect(self, conn: Connection):
        self._connections.remove(conn)
        self.detach(conn)
        conn.update()

#connection is an additional layer for pins interacting with each other
class Connection(Propagator):
    def __init__(self, source = None, target = None):
        super().__init__()
        self._source = source
        self._target = target
        self.type = "Connection"
    
    def getOutput(self):
        return self._source.getOutput()

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
            sourcePin.connect(conn)
            targetPin.connect(conn)
            
            return conn
    
    @staticmethod
    def isValidPair(pin1: Pin, pin2: Pin) -> bool:
        if isinstance(pin1, InputPin) and isinstance(pin2, OutputPin) or isinstance(pin2, InputPin) and isinstance(pin1, OutputPin):
            return True
        else:
            return False