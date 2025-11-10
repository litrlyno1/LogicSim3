from model.LogicGate import LogicGate

class AndGate(LogicGate):
    type = "AndGate"
    numInputs = 2
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        print(f"And Gate evaluated with value {self._value}")
        self._value = self._inputPins[0].value and self._inputPins[1].value

class OrGate(LogicGate):
    type = "OrGate"
    numInputs = 2
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        print(f"Or Gate evaluated with value {self._value}")
        self._value = self._inputPins[0].value or self._inputPins[1].value

class XorGate(LogicGate):
    type = "XorGate"
    numInputs = 2
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        print(f"Xor Gate evaluated with value {self._value}")
        self._value = (not self._inputPins[0].value and self._inputPins[1].value) or (self._inputPins[0].value and not self._inputPins[1].value)

class NotGate(LogicGate):
    type = "NotGate"
    numInputs = 1
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        print(f"Not Gate evaluated with value {self._value}")
        self._value = not self._inputPins[0].value