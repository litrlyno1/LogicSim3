from typing import List, Set
import weakref

from PySide6.QtCore import QPointF

from viewmodel.command.base import Command
from viewmodel.CanvasVM import CanvasVM
from viewmodel.CircuitComponentVM import CircuitComponentVM
from viewmodel.ComponentVM import ComponentVM
from viewmodel.ConnectionVM import ConnectionVM
from viewmodel.ComponentVMFactory import ComponentVMFactory
from viewmodel.PinVM import PinVM

class AddComponents(Command):
    def __init__(self, canvasVM : CanvasVM, componentTypeList : List[str], posList: List[QPointF]):
        super().__init__()
        self._canvas = canvasVM
        self._components : List[ComponentVM] = list()
        for index in range(len(componentTypeList)):
            self._components.append(ComponentVMFactory.createComponent(type = componentTypeList[index], pos = posList[index]))
    
    @property
    def component(self):
        return self._component
    
    def execute(self):
        for component in self._components:
            self._canvas.addComponent(component = component)
    
    def undo(self):
        for component in self._components:
            self._canvas.removeComponent(component)

class MoveComponents(Command):
    def __init__(self, canvasVM : CanvasVM, components : List[ComponentVM], oldPosList : List[QPointF], newPosList : List[QPointF]):
        super().__init__()
        self._canvas = canvasVM
        self._components = components
        self._oldPosList = oldPosList
        self._newPosList = newPosList
    
    @property
    def components(self):
        return self._components
    
    @property
    def oldPosList(self):
        return self._oldPosList
    
    @property
    def newPosList(self):
        return self._newPosList
    
    def execute(self):
        for index in range(len(self._components)):
            self._components[index].pos = self._newPosList[index]
    
    def undo(self):
        for index in range(len(self._components)):
            self._components[index].pos = self._oldPosList[index]

class RemoveComponents(Command):
    def __init__(self, canvasVM : CanvasVM, componentIds : List[str]):
        super().__init__()
        self._canvas = canvasVM
        self._componentsIds = componentIds
        self._components : List[ComponentVM] = list()
        self._adjacentConnections : List[Set[ConnectionVM]] = list()
        for id in self._componentsIds:
            component = self._canvas.components[id]
            self._components.append(component)
            if isinstance(component, CircuitComponentVM):
                adjacent = set()
                for id in self._canvas.connections:
                    connection = self._canvas.connections[id]
                    if connection.isConnectedToCircuitComponent(component):
                        adjacent.add(connection)
                self._adjacentConnections.append(adjacent)
            else:
                self._adjacentConnections.append([])
    
    @property
    def components(self):
        return self._components
    
    @property
    def canvas(self):
        return self._canvas
    
    def execute(self):
        for connectionSet in self._adjacentConnections:
            for connection in connectionSet:
                self._canvas.removeConnection(connection)
        for component in self._components:
            self._canvas.removeComponent(component)
    
    def undo(self):
        for component in self._components:
            self._canvas.addComponent(component)
        for connectionSet in self._adjacentConnections:
            for connection in connectionSet:
                self._canvas.addConnection(connection)

class CreateConnection(Command):
    def __init__(self, canvasVM : CanvasVM, pinVM1 : PinVM, pinVM2 : PinVM):
        self._canvas = canvasVM
        self._pinVM1 = weakref.ref(pinVM1)
        self._pinVM2 = weakref.ref(pinVM2)
    
    def execute(self):
        self._connection = ConnectionVM(self._pinVM1(), self._pinVM2())
        self._canvas.addConnection(self._connection)
    
    def undo(self):
        self._canvas.removeConnection(self._connection)

class RemoveConnections(Command):
    def __init__(self, canvasVM : CanvasVM, connectionIds : List[str]):
        self._canvas = canvasVM
        self._connectionIds = connectionIds
        self._connections = list()
        for id in self._connectionIds:
            self._connections.append(self._canvas.connections[id])
    
    def execute(self):
        for connection in self._connections:
            self._canvas.removeConnection(connection)
    
    def undo(self):
        for connection in self._connections:
            self._canvas.addConnection(connection)