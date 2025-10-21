from PySide6.QtCore import QPointF

from viewmodel.command.base import Command
from viewmodel.CanvasVM import CanvasVM
from viewmodel.ComponentVM import ComponentVM
from viewmodel.LogicGateVM import LogicGateVM
from viewmodel.BulbVM import BulbVM
from viewmodel.SwitchVM import SwitchVM
from viewmodel.ConnectionVM import ConnectionVM

# temporary dictionary
text_vm = {
    "Switch" : SwitchVM,
    "Bulb" : BulbVM,
    "AndGate" : LogicGateVM,
    "OrGate" : LogicGateVM,
    "XorGate" : LogicGateVM,
    "NandGate" : LogicGateVM,
    "NotGate" : LogicGateVM
}

class AddComponent(Command):
    def __init__(self, canvasVM : CanvasVM, componentType : str, pos : QPointF):
        super().__init__()
        print(f"Component type: {componentType}")
        print(f"pos: {pos}")
        self._canvas = canvasVM
        componentClass = text_vm[componentType]
        print(f"Add Component command: retrieved class {componentClass}")
        if componentClass == LogicGateVM:
            self._component = LogicGateVM(componentType, pos)
        else:
            self._component = componentClass(pos)
        print(f"Add Component command: created component {self._component}")
        print(self._component)
        self._pos = pos
    
    @property
    def component(self):
        return self._component
    
    def getCanvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.addComponent(self._component)
    
    def undo(self):
        self._canvas.removeComponent(self._component)

class MoveComponent(Command):
    def __init__(self, canvasVM : CanvasVM, component : ComponentVM, oldPos : QPointF, newPos : QPointF):
        super().__init__()
        self._canvas = canvasVM
        self._component = component
        self._oldPos = oldPos
        self._newPos = newPos
    
    @property
    def component(self):
        return self._component
    
    @property
    def oldPos(self):
        return self._oldPos
    
    @property
    def newPos(self):
        return self._newPos
    
    def execute(self):
        self._component.setPos(self._newPos)
    
    def undo(self):
        self._component.setPos(self._oldPos)

class RemoveComponent(Command):
    def __init__(self, canvasVM : CanvasVM, component : ComponentVM):
        super().__init__()
        self._canvas = canvasVM
        self._component = component
    
    @property
    def component(self):
        return self._component
    
    @property
    def canvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.removeComponent(self._component)
    
    def undo(self):
        self._canvas.addComponent(self._component)

class CreateConnection(Command):
    def __init__(self, canvasVM : CanvasVM, gate1 : LogicGateVM, type1 : str, index1 : int, gate2 : LogicGateVM, type2 : str, index2 : int):
        self._canvas = canvasVM
        print("Command: creating connection")
        print(f"gate (model): {gate1.component}")
        print(f"gate2 (model): {gate2.component}")
        self._connection = ConnectionVM(gate1, type1, index1, gate2, type2, index2)
    
    def getConnection(self):
        return self._connection
    
    def getCanvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.addConnection(self._connection)
    
    def undo(self):
        self._canvas.removeConnection(self._connection)