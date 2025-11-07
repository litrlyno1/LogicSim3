from typing import Literal
from model.CircuitComponent import CircuitComponent

class Bulb(CircuitComponent):
    type = "Bulb"
    numInputs = 1
    numOutputs = 0
    
    def __init__(self):
        super().__init__()
    
    def _evaluate(self):
        self._value = self._inputPins[0].value