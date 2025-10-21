from PySide6.QtCore import Signal, Slot, QObject, QPointF
from typing import List

from viewmodel.LogicGateVM import LogicGateVM
from viewmodel.ConnectionVM import ConnectionVM

class CanvasVM(QObject):
    gateAdded = Signal(LogicGateVM)
    gateRemoved = Signal(LogicGateVM)
    gatePosUpdated = Signal(str, QPointF)
    connectionAdded = Signal(object)
    connectionRemoved = Signal(ConnectionVM)
    
    def __init__(self):
        super().__init__()
        self._gates: List[LogicGateVM] = []
        self._connections: List[ConnectionVM] = []
    
    def getGates(self) -> List[LogicGateVM]:
        return self._gates

    def removeGate(self, gate : LogicGateVM) -> None:
        self._gates.remove(gate)
        self.gateRemoved.emit(gate)
    
    def addGate(self, gate : LogicGateVM) -> None:
        self._gates.append(gate)
        gate.posChanged.connect(self.gatePosChanged)
        self.gateAdded.emit(gate)
        #print("CanvasVM: Gate added:")
        #print(gate.__dict__)
    
    def addConnection(self, connection : ConnectionVM):
        self._connections.append(connection)
        self.connectionAdded.emit(connection)
        
    def removeConnection(self, connection : ConnectionVM):
        self._connections.append(connection)
        self.connectionRemoved.emit(connection)
    
    @Slot(str, QPointF)
    def gatePosChanged(self, id : str, pos : QPointF) -> None:
        self.gatePosUpdated.emit(id, pos)