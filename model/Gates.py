from model.LogicGate import LogicGate

class AndGate(LogicGate):
    type = "AndGate"
    numInputs = 2
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        self._value = self._inputPins[0].value and self._inputPins[1].value

class OrGate(LogicGate):
    type = "OrGate"
    numInputs = 2
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        self._value = self._inputPins[0] or self._inputPins[1]

class XorGate(LogicGate):
    type = "XorGate"
    numInputs = 2
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        self._value = (not self._inputPins[0] and self._inputPins[1]) or (self._inputPins[0] and not self._inputPins[1])

class NotGate(LogicGate):
    type = "NotGate"
    numInputs = 1
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        self._value = not self._inputPins[0]