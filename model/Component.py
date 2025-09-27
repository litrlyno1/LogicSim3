from abc import ABC, abstractmethod

class Component(ABC):
    
    def __init__(self):
        super().__init__()
        self._observers = []
    
    @abstractmethod
    def getOutput(self) -> bool:
        pass
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
        self.notify()
    
    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
        self.notify()
    
    def notify(self):
        for observer in self._observers:
            observer.onChange()