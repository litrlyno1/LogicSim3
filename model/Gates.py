from LogicGate import LogicGate
from core.registry import registry

class AndGate(LogicGate):
    name = "AndGate"
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self.inputPins[0].getOutput() and self.inputPins[1].getOutput())

class OrGate(LogicGate):
    name = "OrGate"
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self.inputPins[0].getOutput() or self.inputPins[1].getOutput())

class NotGate(LogicGate):
    name = "NotGate"
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return not self.inputPins[0].getOutput()

class BulbGate(LogicGate):
    name = "Bulb"
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return (self.inputPins[0].getOutput())