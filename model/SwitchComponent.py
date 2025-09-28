from Interfaces import IToggleable, ISignalSource
from Observer import SignalPropagator

class Switch(IToggleable, ISignalSource):
    
    def __init__(self, propagator : SignalPropagator = None):
        super().__init__(propagator)
        self._value = False
    
    def toggle(self):
        self._value = not self._value
        self.notifyChange()
    
    def getOutput(self):
        return self._value