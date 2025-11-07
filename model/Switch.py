from typing import Literal
from model.CircuitComponent import CircuitComponent

class Switch(CircuitComponent):
    type = "Switch"
    numInputs = 0
    numOutputs = 1
    
    def __init__(self):
        super().__init__()
    
    def toggle(self):
        self._value = not self._value
        self.update()
    
    def _evaluate(self):
        pass