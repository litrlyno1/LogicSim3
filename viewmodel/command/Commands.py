from PySide6.QtCore import QPointF

from viewmodel.command.base import Command
from viewmodel.CanvasVM import CanvasVM
from viewmodel.LogicGateVM import LogicGateVM
from viewmodel.ConnectionVM import ConnectionVM

class AddGate(Command):
    def __init__(self, canvasVM : CanvasVM, gateType : str, pos : QPointF):
        super().__init__()
        print(f"Gate type: {gateType}")
        print(f"pos: {pos}")
        self._canvas = canvasVM
        self._gate = LogicGateVM(gateType, pos)
        self._pos = pos
    
    def getGate(self):
        return self._gate
    
    def getCanvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.addGate(self._gate)
    
    def undo(self):
        self._canvas.removeGate(self._gate)

class MoveGate(Command):
    def __init__(self, canvasVM : CanvasVM, gate : LogicGateVM, oldPos : QPointF, newPos : QPointF):
        super().__init__()
        self._canvas = canvasVM
        self._gate = gate
        self._oldPos = oldPos
        self._newPos = newPos
    
    def getGate(self):
        return self._gate
    
    def getOldPos(self):
        return self._oldPos
    
    def getNewPos(self):
        return self._newPos
    
    def execute(self):
        self._gate.setPos(self._newPos)
    
    def undo(self):
        self._gate.setPos(self._oldPos)

class RemoveGate(Command):
    def __init__(self, canvasVM : CanvasVM, gate : LogicGateVM):
        super().__init__()
        self._canvas = canvasVM
        self._gate = gate
    
    def getGate(self):
        return self._gate
    
    def getCanvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.removeGate(self._gate)
    
    def undo(self):
        self._canvas.addGate(self._gate)

class CreateConnection(Command):
    def __init__(self, canvasVM : CanvasVM, gate1 : LogicGateVM, type1 : str, index1 : int, gate2 : LogicGateVM, type2 : str, index2 : int):
        self._canvas = canvasVM
        print("Command: creating connection")
        print(f"gate (model): {gate1.getGate()}")
        print(f"gate2 (model): {gate2.getGate()}")
        self._connection = ConnectionVM(gate1, type1, index1, gate2, type2, index2)
    
    def getConnection(self):
        return self._connection
    
    def getCanvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.addConnection(self._connection)
    
    def undo(self):
        self._canvas.removeConnection(self._connection)