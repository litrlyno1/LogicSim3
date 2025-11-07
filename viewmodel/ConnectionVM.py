from PySide6.QtCore import Signal, QObject, Slot
import weakref

from core.idGenerator import generateId
from model.Pin import Connection
from viewmodel.PropagatorObject import PropagatorObject
from viewmodel.PinVM import PinVM
from viewmodel.CircuitComponentVM import CircuitComponentVM

class ConnectionVM(PropagatorObject):
    type = "ConnectionVM"
    
    def __init__(self, pinVM1 : PinVM, pinVM2 : PinVM):
        self._pinVM1 = pinVM1
        self._pinVM2 = pinVM2
        self._connection = Connection.create(pinVM1.pin, pinVM2.pin)
        self._id = generateId(prefix = "Connection")
        super().__init__(id = self._id, propagator= self._connection)
    
    @staticmethod
    def canConnect(pinVM1 : PinVM, pinVM2 : PinVM):
        return Connection.canConnect(pinVM1.pin, pinVM2.pin)
    
    def connect(self):
        self._connection.connect()
    
    def disconnect(self):
        self._connection.disconnect()
    
    @property
    def id(self):
        return self._id
    
    @property
    def pinId1(self):
        return self._pinVM1.id
    
    @property
    def pinId2(self):
        return self._pinVM2.id
    
    @property
    def pinIds(self):
        return self.pinId1, self.pinId2

    def isConnectedToCircuitComponent(self, circuitComponent : CircuitComponentVM) -> bool:
        return self._pinVM1 in circuitComponent.inputPins + circuitComponent.outputPins or self._pinVM2 in circuitComponent.inputPins + circuitComponent.outputPins