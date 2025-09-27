from LogicGate import LogicGate

class AndGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self._getInputValues()[0] and self._getInputValues()[1])

class OrGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 2)
    
    def getOutput(self):
        return (self._getInputValues()[0] or self._getInputValues()[1])

class NotGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return (not self._getInputValues()[0])

class BulbGate(LogicGate):
    
    def __init__(self):
        super().__init__(numInputs = 1)
    
    def getOutput(self):
        return (self._getInputValues()[0])
    
    def onChange(self):
        self._value = self.getOutput()