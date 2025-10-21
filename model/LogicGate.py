from __future__ import annotations
from typing import List
from model.Pin import InputPin, OutputPin, Pin
from model.Propagator import Propagator
from model.Component import Component

class LogicGate(Component, Propagator):

    def __init__(self, numInputs: int, numOutputs: int = 1):
        super().__init__()
        self._numInputs = numInputs
        self._numOutputs = numOutputs
        self._pins = self._PinManager(self)
        self._pins.createInputPins(numInputs)
        self._pins.createOutputPins(numOutputs)
    
    def getNumInputs(self) -> int:
        return self._numInputs

    def getNumOutputs(self) -> int:
        return self._numOutputs

    def getInputPins(self) -> List[InputPin]:
        return self._pins.inputPins

    def getInputPin(self, index: int) -> InputPin:
        return self._pins.getInputPin(index)

    def getPin(self, type : str, index : int) -> Pin:
        return self.getInputPin(index) if type == "input" else self.getOutputPin(index)

    def getOutputPins(self) -> List[OutputPin]:
        return self._pins.outputPins

    def getOutputPin(self, index: int) -> OutputPin:
        return self._pins.getOutputPin(index)
    
    class _PinManager:
        def __init__(self, gate: "LogicGate"):
            self._gate = gate
            self._inputPins: List[InputPin] = []
            self._outputPins: List[OutputPin] = []

        def createInputPins(self, num: int):
            self._inputPins = []
            for index in range(num):
                pin = InputPin(gate = self._gate, index=index)
                self._inputPins.append(pin)

        @property
        def inputPins(self) -> List[InputPin]:
            return self._inputPins

        def getInputPin(self, index: int) -> InputPin:
            return self._inputPins[index]

        def createOutputPins(self, num: int):
            self._outputPins = []
            for index in range(num):
                pin = OutputPin(gate = self._gate, index=index)
                self._gate.attach(pin)
                self._outputPins.append(pin)

        @property
        def outputPins(self) -> List[OutputPin]:
            return self._outputPins

        def getOutputPin(self, index: int) -> OutputPin:
            return self._outputPins[index]