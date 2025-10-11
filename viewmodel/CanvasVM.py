from PySide6.QtCore import Signal, Slot, QObject, QPointF
from typing import List

from viewmodel.LogicGateVM import LogicGateVM

class CanvasVM(QObject):
    gateAdded = Signal(LogicGateVM)
    gateRemoved = Signal(LogicGateVM)
    gateMoved = Signal(LogicGateVM, QPointF)
    
    def __init__(self):
        super().__init__()
        self._gates: List[LogicGateVM] = []
    
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
    
    @Slot(LogicGateVM, QPointF)
    def gatePosChanged(self, gate : LogicGateVM, pos : QPointF) -> None:
        self.gateMoved.emit(gate, pos)