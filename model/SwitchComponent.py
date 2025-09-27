from Interfaces import IToggleable, ISignalSource
from Observer import Observer, IObservable

class Switch(IObservable, IToggleable, ISignalSource):
    
    def __init__(self):
        super().__init__()
    
    def toggle(self):
        return not self._value
    
    def getOutput(self):
        return self._value