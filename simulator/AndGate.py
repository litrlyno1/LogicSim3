from LogicGate import LogicGate

class AndGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def _calculateOutput(self):
        return (self._getInputValues()[0] and self._getInputValues()[1])
    
    def getOutput(self):
        return self._calculateOutput()