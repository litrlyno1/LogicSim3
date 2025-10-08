from PySide6.QtCore import QPointF

from viewmodel.commands.base import Command
from viewmodel.CanvasVM import CanvasVM
from viewmodel.LogicGateVM import LogicGateVM

class AddGate(Command):
    def __init__(self, canvas : CanvasVM, gateType : str, pos : QPointF):
        super().__init__()
        self._canvas = canvas
        self._gate = LogicGateVM.create(self._canvas, gateType, pos)
    
    def getGate(self):
        return self._gate
    
    def getCanvas(self):
        return self._canvas
    
    def execute(self):
        self._canvas.addGate(self._gate)
    
    def undo(self):
        self._canvas.removeGate(self._gate)