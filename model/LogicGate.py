from Pin import InputPin, OutputPin
from Observer import Observer, IObservable
from Interfaces import ISignalSource
from __future__ import annotations

class LogicGate(Observer, IObservable, ISignalSource):
    
    def __init__(self, numInputs : int, numOutputs : int = 1):
        self._numInputs = numInputs
        self._numOutputs = numOutputs
        self._initPins_()
    
    def __initPins__(self):
        self.__initInputPins__()
        self.__initOutputPins__()
    
    def __initOutputPins__(self):
        self.outputPins = []
        for _ in range(self._numOutputs):
            self.outputPins.append(OutputPin(gate = self))
    
    def __initInputPins__(self):
        self.inputPins = []
        for _ in range(self._numInputs):
            self.inputPins.append(InputPin(gate = self, index = _))