from PySide6.QtCore import Signal, Slot, QObject, QPointF
from typing import List

from viewmodel.LogicGateVM import LogicGateVM

class CanvasVM(QObject):
    gateAdded = Signal(LogicGateVM, QPointF)
    gateRemoved = Signal(LogicGateVM)
    gateMoved = Signal(LogicGateVM)
    
    def __init__(self):
        self._gates: List[LogicGateVM] = []
    
    def getGates(self) -> List[LogicGateVM]:
        return self._gates

    def removeGate(self, gate : LogicGateVM) -> None:
        self._gates.remove(gate)
        self.gateRemoved.emit(gate)
    
    def addGate(self, gate : LogicGateVM) -> None:
        self._gates.append(gate)
        self.gateAdded.emit(gate)
    
    def onGatePosChanged(self, gate : LogicGateVM, pos : QPointF) -> None:
        self.gateMoved.emit(gate, pos)