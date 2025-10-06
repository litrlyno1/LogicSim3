from PySide6.QtCore import QObject, Signal, Slot, QPointF

from model.Observer import Observer
from model.LogicGate import LogicGate

from CanvasVM import CanvasVM
from Selectable import Selectable
from Deletable import Deletable
from ModelObserver import ModelObserver

def LogicGateVM(ModelObserver, Selectable, Deletable):
    posChanged = Signal()
    
    def __init__(self, canvas : CanvasVM, gate : LogicGate, pos: QPointF = QPointF(0,0), selected : bool = True):
        super().__init__()
        self._canvas = canvas
        self._gate = gate
        self._pos = pos
        
        self._gate.attach(self)
    
    def getCanvas(self) -> CanvasVM:
        return self._canvas
    
    def getGate(self) -> LogicGate:
        return self._gate
    
    def getPos(self) -> QPointF:
        return self._pos
    
    def setPos(self, pos : QPointF) -> None:
        self._pos = pos
        self.posChanged.connect(self._canvas.onGatePosChanged)
        self.posChanged.emit(self, pos)