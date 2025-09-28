from abc import ABC, abstractmethod
from Pin import Connection

class IToggleable(ABC):

    @abstractmethod
    def toggle(self) -> None:
        ...

class ISignalSource(ABC):
    
    @abstractmethod
    def getOutput(self) -> bool:
        ...

class IConnectable(ABC):
    
    @abstractmethod
    def connect(self, connection : Connection) -> None:
        ...
    
    @abstractmethod
    def disconnect(self) -> None:
        ...