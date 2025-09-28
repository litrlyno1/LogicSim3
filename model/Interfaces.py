from abc import abstractmethod
from Pin import Connection
from typing import Protocol
from Observer import SignalPropagator

class IToggleable(Protocol):
    
    def __init__(self, propagator : SignalPropagator):
        super().__init__()
    
    @abstractmethod
    def toggle(self):
        ...

class ISignalSource(Protocol):
    
    @abstractmethod
    def getOutput(self):
        ...

class IConnectable(Protocol):
    
    @abstractmethod
    def connect(self, connection : Connection):
        ...
    
    @abstractmethod
    def disconnect(self):
        ...