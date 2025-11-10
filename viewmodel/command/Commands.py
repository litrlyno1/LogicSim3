from typing import List, Set, Tuple
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
    def __init__(self, canvasVM : CanvasVM, componentIds : List[ComponentVM], newPosList : List[QPointF]):
        super().__init__()
        self._canvas = canvasVM
        self._componentIds = componentIds
        self._oldPosList = []
        for id in componentIds:
            self._oldPosList.append(self._canvas.components[id].pos)
        self._newPosList = newPosList
        print(f"Commands: Initialized command MoveComponent with ids {self._componentIds}, oldPosList {self._oldPosList}, newPosList {self._newPosList}")
    
    @property
    def components(self):
        return self._componentIds
    
    @property
    def oldPosList(self):
        return self._oldPosList
    
    @property
    def newPosList(self):
        return self._newPosList
    
    def execute(self):
        for index in range(len(self._componentIds)):
            id = self._componentIds[index]
            component = self._canvas.components[id]
            component.pos = self._newPosList[index]
    
    def undo(self):
        for index in range(len(self._componentIds)):
            id = self._componentIds[index]
            component = self._canvas.components[id]
            component.pos = self._oldPosList[index]

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
                adjacentConnections = set()
                for id in self._canvas.connections:
                    connection = self._canvas.connections[id]
                    if connection.isConnectedToCircuitComponent(component):
                        adjacentConnections.add(connection)
                self._adjacentConnections.append(adjacentConnections)
            print(f"Command RemoveComponents. Adjacent connections {adjacentConnections}")
    
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
    def __init__(self, canvasVM : CanvasVM, parentPinPair1 : Tuple[str, str], parentPinPair2: Tuple[str, str]):
        super().__init__()
        self._canvas = canvasVM
        self._pinVM1 = weakref.ref(self._canvas.components[parentPinPair1[0]].pins[parentPinPair1[1]])
        self._pinVM2 = weakref.ref(self._canvas.components[parentPinPair2[0]].pins[parentPinPair2[1]])
        if ConnectionVM.canConnect(self._pinVM1(), self._pinVM2()):
            self._connection = ConnectionVM(self._pinVM1(), self._pinVM2())
        else:
            self._connection = None
            self._createdSuccessfully = False
    
    def execute(self):
        self._canvas.addConnection(self._connection)
    
    def undo(self):
        self._canvas.removeConnection(self._connection)

class RemoveConnections(Command):
    def __init__(self, canvasVM : CanvasVM, connectionIds : List[str]):
        super().__init__()
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

class ToggleComponent(Command):
    def __init__(self, canvasVM : CanvasVM, componentId: str):
        super().__init__()
        self._canvas = canvasVM
        self._component = self._canvas.components[componentId]
    
    def execute(self):
        self._component.toggle()
    
    def undo(self):
        self._component.toggle()