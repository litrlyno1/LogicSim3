from model.LogicGate import LogicGate

class AndGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self.getInputPin(0).getOutput() and self.getInputPin(1).getOutput())

class OrGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self.getInputPin(0).getOutput() or self.getInputPin(1).getOutput())

class XorGate(LogicGate):
    
    def __init__(self, numInputs, numOutputs = 1):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self.getInputPin(0).getOutput() ^ self.getInputPin(1).getOutput())

class NotGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return not self.getInputPin(0).getOutput()

class BulbGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return (self.inputPins[0].getOutput())