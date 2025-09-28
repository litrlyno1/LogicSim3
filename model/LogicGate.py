from Pin import InputPin, OutputPin
from Propagator import Propagator
from __future__ import annotations

class LogicGate(Propagator):
    
    def __init__(self, numInputs : int, numOutputs : int = 1):
        super().__init__()
        self._numInputs = numInputs
        self._numOutputs = numOutputs
        self._init_pins_()
    
    def _init_pins_(self):
        self._init_input_pins_()
        self._init_output_pins_()
    
    def _init_output_pins_(self):
        self.outputPins = []
        for _ in range(self._numOutputs):
            self.outputPins.append(OutputPin(gate = self))
    
    def _init_input_pins_(self):
        self.inputPins = []
        for _ in range(self._numInputs):
            self.inputPins.append(InputPin(gate = self, index = _))