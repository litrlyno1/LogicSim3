from abc import ABC, abstractmethod
from Pin import Connection

class IToggleable(ABC):
    
    def __init__(self):
        super().__init__()
        self._value = False
    
    @abstractmethod
    def toggle(self):
        ...

class ISignalSource(ABC):
    
    @abstractmethod
    def getOutput(self):
        ...

class IConnectable(ABC):
    
    @abstractmethod
    def connect(self, connection : Connection):
        ...
    
    @abstractmethod
    def disconnect(self):
        ...