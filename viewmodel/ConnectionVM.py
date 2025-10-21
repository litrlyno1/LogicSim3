from PySide6.QtCore import Signal, QObject

from model.Pin import Connection
from viewmodel import LogicGateVM
from core.idGenerator import generateId
from viewmodel.ModelObserver import ModelObserver

class ConnectionVM(QObject):
    modelUpdated = Signal(object)
    
    def __init__(self, gate1 : LogicGateVM, type1 : str, index1 : int, gate2 : LogicGateVM, type2 : str, index2 : int):
        self._connection = Connection.create(gate1.getGate().getPin(type = type1, index = index1), gate2.getGate().getPin(type = type2, index = index2))
        self._gate1 = gate1
        self._gate2 = gate2
        self._type1 = type1
        self._type2 = type2
        self._index1 = index1
        self._index2 = index2
        self._id = generateId(prefix = "Connection")
        self._modelObserver = ModelObserver(self, self._connection)
    
    
    def getConnection(self):
        return self._connection
    
    def getGate1(self):
        return self._gate1
    
    def getGate2(self):
        return self._gate2
    
    def getIndex1(self):
        return self._index1
    
    def getIndex2(self):
        return self._index2
    
    def onModelUpdate(self):
        self.modelUpdated.emit(self)