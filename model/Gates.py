from LogicGate import LogicGate

class AndGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self.inputPins[0].getOutput() and self.inputPins[1].getOutput())

class OrGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self.inputPins[0].getOutput() or self.inputPins[1].getOutput())

class NotGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return not self.inputPins[0].getOutput()

class BulbGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return (self.inputPins[0].getOutput())