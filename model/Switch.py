from Interfaces import IToggleable
from LogicGate import LogicGate

class Switch(LogicGate, IToggleable):
    
    def __init__(self):
        super().__init__(numInputs=0, numOutputs=1)
        self._value = False
        self.type = "Switch"
    
    def toggle(self):
        self._value = not self._value
        self.update()
    
    def getOutput(self):
        return self._value