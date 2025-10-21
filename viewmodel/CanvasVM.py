from PySide6.QtCore import Signal, Slot, QObject, QPointF
from typing import List

from viewmodel.LogicGateVM import LogicGateVM
from viewmodel.ConnectionVM import ConnectionVM
from viewmodel.ComponentVM import ComponentVM

class CanvasVM(QObject):
    componentAdded = Signal(ComponentVM)
    componentRemoved = Signal(ComponentVM)
    componentPosUpdated = Signal(str, QPointF)
    connectionAdded = Signal(object)
    connectionRemoved = Signal(ConnectionVM)
    
    def __init__(self):
        super().__init__()
        self._components: List[ComponentVM] = []
        self._connections: List[ConnectionVM] = []
    
    def getComponents(self) -> List[ComponentVM]:
        return self._components

    def removeComponent(self, component : ComponentVM) -> None:
        self._components.remove(component)
        self.componentRemoved.emit(component)
    
    def addComponent(self, component : ComponentVM) -> None:
        self._components.append(component)
        print(component)
        component.posChanged.connect(self.componentPosChanged)
        self.componentAdded.emit(component)
    
    def addConnection(self, connection : ConnectionVM):
        self._connections.append(connection)
        self.connectionAdded.emit(connection)
        
    def removeConnection(self, connection : ConnectionVM):
        self._connections.append(connection)
        self.connectionRemoved.emit(connection)
    
    @Slot(str, QPointF)
    def componentPosChanged(self, id : str, pos : QPointF) -> None:
        self.componentPosUpdated.emit(id, pos)