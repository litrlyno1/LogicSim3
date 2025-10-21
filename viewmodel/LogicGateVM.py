from PySide6.QtCore import Signal, Slot, QPointF

from model.Observer import Observer
from model.LogicGate import LogicGate
from core.registry import ComponentRegistry
from viewmodel.ModelObserver import ModelObserver
from viewmodel.ComponentVM import ComponentVM

class LogicGateVM(ComponentVM):
    type = "gate"
    modelUpdated = Signal(object)
    
    def __init__(self, gateType : str, pos: QPointF = QPointF(0,0)):
        super().__init__(component=ComponentRegistry.getComponent(gateType)(), pos = pos)
        self._gateType = gateType
        self._modelObserver = ModelObserver(self, self._component)
        #print(self.__dict__)
    
    def getId(self):
        return self._id
    
    def getGateType(self) -> str:
        return self._gateType
    
    def getPos(self) -> QPointF:
        return self._pos
    
    def setPos(self, pos : QPointF) -> None:
        self._pos = pos
        self.posChanged.emit(self._id, pos)
    
    def onModelUpdate(self):
        self.modelUpdated.emit(self)