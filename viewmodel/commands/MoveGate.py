from PySide6.QtCore import QPointF

from viewmodel.commands.base import Command
from viewmodel.LogicGateVM import LogicGateVM

class AddGate(Command):
    def __init__(self, gate : LogicGateVM, oldPos : QPointF, newPos : QPointF):
        super().__init__()
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