from model.Observer import Observer, Observable
from model.Interfaces import ISignalSource

#propagator class is used to mark components, which can both receive and transmit a signal
class Propagator(Observer, Observable, ISignalSource):
    def update(self):
        #print(self.type)
        self.notify()
    
    def getOutput(self):
        ...