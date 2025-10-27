from typing import List
from Pin import Pin, OutputPin, InputPin

class HasPins:
    
    def __init__(self, numInputs : int, numOutputs: int):
        self._numInputs = numInputs
        self._numOutputs = numOutputs
        self._createInputPins(numInputs)
        self._createOutputPins(numOutputs)
    
    @property
    def numInputs(self):
        return self._numInputs
    
    @property
    def numOutputs(self):
        return self._numOutputs

    @property
    def inputPins(self):
        return self._inputPins
    
    @property
    def outputPins(self):
        return self._outputPins

    def getPin(self, type : str, index : int) -> Pin:
        pins = self._inputPins if type == "input" else self._outputPins
        return pins[index]

    @property
    def inputPins(self) -> List[InputPin]:
        return self._inputPins

    @property
    def outputPins(self) -> List[OutputPin]:
        return self._outputPins
    
    def _createInputPins(self, num: int):
        self._inputPins : List[InputPin] = []
        for _ in range(num):
            self._inputPins.append(InputPin(self))
    
    def _createOutputPins(self, num : int):
        self._outputPins : List[OutputPin] = []
        for _ in range(num):
            self._outputPins.append(OutputPin(self))