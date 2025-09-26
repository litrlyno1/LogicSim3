from LogicGate import LogicGate

class NotGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return (not self._getInputValues()[0])