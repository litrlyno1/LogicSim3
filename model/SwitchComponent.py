from Interfaces import IToggleable, ISignalSource
from Observer import SignalPropagator
from LogicGate import LogicGate

class Switch(LogicGate, IToggleable, ISignalSource):
    
    def __init__(self, propagator : SignalPropagator = None):
        super().__init__(numInputs=0, numOutputs=1, propagator = propagator)
        self._value = False
    
    def toggle(self):
        self._value = not self._value
        self.notifyChange()
    
    def getOutput(self):
        return self._value