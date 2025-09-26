from LogicGate import LogicGate

class NotGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def _calculateOutput(self):
        return (not self._getInputValues()[0])
    
    def getOutput(self):
        return self._calculateOutput()