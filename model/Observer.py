from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self) -> None:
        ...

class Observable(ABC):
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer : Observer):
        if observer not in self._observers:
            self._observers.append(observer)
        
    def detach(self, observer : Observer): 
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update()

#propagator class is used to mark components, which can both receive and transmit a signal
class Propagator(Observer, Observable):
    def update(self):
        self.notify()