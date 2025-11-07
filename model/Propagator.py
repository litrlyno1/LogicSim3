from abc import ABC, abstractmethod
from model.Observer import Observer, Observable

class Propagator(Observer, Observable, ABC):
    
    def __init__(self):
        super().__init__()
        self._value = False
    
    @property
    def value(self):
        return self._value
    
    def update(self):
        #print(f"Propagation, object: {self}")
        self._evaluate()
        self.notify()
    
    @abstractmethod
    def _evaluate(self):
        pass