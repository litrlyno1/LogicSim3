from Observer import Observer, Observable
from Interfaces import ISignalSource

#propagator class is used to mark components, which can both receive and transmit a signal
class Propagator(Observer, Observable, ISignalSource):
    def update(self):
        self.notify()
        print("Propagation!")
    
    def getOutput(self):
        ...