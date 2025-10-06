from viewmodel.commands.base import Command
from viewmodel.CanvasVM import CanvasVM
from viewmodel.LogicGateVM import LogicGateVM

class RemoveGate(Command):
    def __init__(self, canvas : CanvasVM, gate : LogicGateVM):
        super().__init__()
        self._canvas = canvas
        self._gate = gate
    
    def getGate(self):
        return self._gate
    
    def getCanvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.removeGate(self._gate)
    
    def undo(self):
        self._canvas.addGate(self._gate)