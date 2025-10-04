from PySide6.QtCore import QObject, Signal, Slot, QPointF
from model.Observer import Observer
from model.LogicGate import LogicGate

def LogicGateVM(QObject, Observer):
    modelUpdated = Signal()
    posChanged = Signal()
    selectedChanged = Signal(bool)
    deleted = Signal()
    
    def __init__(self, gate : LogicGate, pos: QPointF = QPointF(0,0), selected = True):
        self._gate = gate
        self._pos = pos
        self._selected = selected
        
        self._gate.attach(self)
    
    def getGate(self) -> LogicGate:
        return self._gate
    
    def getPos(self) -> QPointF:
        return self._pos
    
    def setPos(self, pos : QPointF) -> None:
        self._pos = pos
        self.posChanged.emit()
    
    def isSelected(self) -> bool:
        return self._selected
    
    def select(self) -> None:
        if self._selected == False:
            self._selected = True
            self.selectedChanged.emit()
    
    def unselect(self) -> None:
        if self._selected == True:
            self._selected = False
            self.selectedChanged.emit()
    
    def delete(self) -> None:
        self.deleted.emit()
    
    def update(self):
        self.modelUpdated.emit()