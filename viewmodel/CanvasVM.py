from PySide6.QtCore import Signal, Slot, QObject, QPointF
from typing import Dict

from viewmodel.ConnectionVM import ConnectionVM
from viewmodel.CircuitComponentVM import CircuitComponentVM
from viewmodel.ComponentVM import ComponentVM
from viewmodel.PinVM import PinVM

class CanvasVM(QObject):
    componentAdded = Signal(str, str, QPointF)
    #id, type, pos
    circuitComponentAdded = Signal(str, str, QPointF, list, list)
    #id, type, pos, list[inputPins], list[outputPins]
    componentRemoved = Signal(str)
    #id
    componentPosUpdated = Signal(str, QPointF)
    #id, pos
    connectionAdded = Signal(str, tuple, tuple)
    #id, parentPin
    connectionRemoved = Signal(str)
    #id
    componentValueUpdated = Signal(str, bool)
    #id, value
    connectionValueUpdated = Signal(str, bool)
    #id, value
    
    def __init__(self):
        super().__init__()
        self._components : Dict[str, ComponentVM] = dict()
        self._connections : Dict[str, ConnectionVM] = dict()
    
    def addComponent(self, component : ComponentVM):
        self._components[component.id] = component
        component.posChanged.connect(lambda id, pos: self.componentPosUpdated.emit(id, pos))
        if isinstance(component, CircuitComponentVM):
            component.valueChanged.connect(lambda id, value: self.componentValueUpdated.emit(id, value))
            self.circuitComponentAdded.emit(component.id, component.type, component.pos, component.inputPinIds, component.outputPinIds)
            print(f"CanvasVM : emitting circuit component added signal with {component.id, component.type, component.pos, component.inputPinIds, component.outputPinIds}")
        else:
            self.componentAdded.emit(component.id, component.type, component.pos)
            print(f"CanvasVM : emitting component added signal with {component.id, component.type, component.pos}")
        print(f"Current component registry: {self._components}")
    
    def removeComponent(self, component : ComponentVM):
        self._components.pop(component.id)
        component.posChanged.disconnect()
        if isinstance(component, CircuitComponentVM):
            component.valueChanged.disconnect()
        self.componentRemoved.emit(component.id)
        print(f"CanvasVM : emitting component removed signal with {component.id}")
        print(f"Current length of componentList: {len(self._components)}")
    
    def addConnection(self, connection : ConnectionVM):
        self._connections[connection.id] = connection
        connection.connect()
        connection.valueChanged.connect(lambda id, value : self.connectionValueUpdated.emit(id, value))
        self.connectionAdded.emit(connection.id, connection.parentPinIdPair1, connection.parentPinIdPair2)
        print(f"CanvasVM : emitting connection added signal with {connection.id, connection.parentPinIdPair1, connection.parentPinIdPair2}")
        print(f"Current length of connectionList: {len(self._connections)}")
    
    def removeConnection(self, connection : ConnectionVM):
        connection.disconnect()
        connection.valueChanged.disconnect()
        self._connections.pop(connection.id)
        self.connectionRemoved.emit(connection.id)
        print(f"CanvasVM : emitting connection removed signal with {connection.id}")
        print(f"Current length of connectionList: {len(self._connections)}")
    
    @property
    def components(self):
        return self._components
    
    @property
    def connections(self):
        return self._connections