from LogicGate import LogicGate

class BulbGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return (self._getInputValues()[0])