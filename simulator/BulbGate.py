from LogicGate import LogicGate

class BulbGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
        self._value = False
    
    def getOutput(self):
        self._value = self._getInputValues()[0]
        return (self._getInputValues()[0])
    
    def onChange(self):
        self._value = self.getOutput()