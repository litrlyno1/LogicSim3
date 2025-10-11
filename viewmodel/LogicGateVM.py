from PySide6.QtCore import QObject, Signal, Slot, QPointF

from model.Observer import Observer
from model.LogicGate import LogicGate
from core.registry import GateRegistry

from viewmodel.Selectable import Selectable
from viewmodel.Deletable import Deletable
from viewmodel.ModelObserver import ModelObserver

class LogicGateVM(QObject, Selectable, Deletable):
    posChanged = Signal()
    modelUpdated = Signal()
    
    def __init__(self, gateType : str, pos: QPointF = QPointF(0,0), selected : bool = False):
        super().__init__()
        self._gateType = gateType
        self._gate = GateRegistry.getGate(self._gateType)()
        self._pos = pos
        self._modelObserver = ModelObserver(self, self._gate)
        print("Gate Initialized: ")
        #print(self.__dict__)
    
    def getGateType(self) -> str:
        return self._gateType
    
    def getGate(self) -> LogicGate:
        return self._gate
    
    def getPos(self) -> QPointF:
        return self._pos
    
    def setPos(self, pos : QPointF) -> None:
        self._pos = pos
        self.posChanged.connect(self._canvas.onGatePosChanged)
        self.posChanged.emit(self, pos)
    
    def onModelUpdate(self):
        self.modelUpdated.emit(self)
    
    @classmethod
    def create(cls, gateType : str, pos : QPointF):
        return(cls(gateType, pos))