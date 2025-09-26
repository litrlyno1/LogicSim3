from LogicGate import LogicGate

class OrGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self._getInputValues()[0] or self._getInputValues()[1])