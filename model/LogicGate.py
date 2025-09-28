from __future__ import annotations
from Pin import InputPin, OutputPin
from Propagator import Propagator

class LogicGate(Propagator):
    
    def __init__(self, numInputs : int, numOutputs : int = 1):
        super().__init__()
        self._numInputs = numInputs
        self._numOutputs = numOutputs
        self._init_pins_()
        self.type = "Gate"
    
    def _init_pins_(self):
        self._init_input_pins_()
        self._init_output_pins_()
    
    def _init_output_pins_(self):
        self.outputPins = []
        for ind in range(self._numOutputs):
            pin = OutputPin(gate = self, index = ind)
            self.outputPins.append(pin)
            self.attach(pin)
    
    def _init_input_pins_(self):
        self.inputPins = []
        for ind in range(self._numInputs):
            pin = InputPin(gate = self, index = ind)
            self.inputPins.append(pin)
            pin.attach(self)

    def getInputPins(self) -> list[InputPin]:
        return self.inputPins
    
    def getOutputPins(self) -> list[OutputPin]:
        return self.outputPins
    
    def getInputPin(self, index : int) -> InputPin:
        return self.getInputPins()[index]
    
    def getOutputPin(self, index : int) -> OutputPin:
        return self.getOutputPins()[index]