from Interfaces import IToggleable, ISignalSource
from Observer import Observer, IObservable

class Switch(IObservable, IToggleable, ISignalSource):
    
    def __init__(self):
        super().__init__()
    
    def toggle(self):
        self._value = not self._value
        self.notify()
    
    def getOutput(self):
        return self._value
    
    def onChange(self):
        self.notify()