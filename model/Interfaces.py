from abc import ABC, abstractmethod

class IToggleable(ABC):

    @abstractmethod
    def toggle(self) -> None:
        ...

class ISignalSource(ABC):
    
    @abstractmethod
    def getOutput(self) -> bool:
        ...

#defines relationship between Pin and Connection
class IConnectable(ABC):

    @abstractmethod
    def connect(self, conn : "Connection") -> None:
        ...

class ISingleConnectable(IConnectable):
    
    @property
    @abstractmethod
    def connection(self) -> "Connection":
        ...
    
    @abstractmethod
    def disconnect(self) -> None:
        ...

class IMultiConnectable(IConnectable):
    
    @property
    @abstractmethod
    def connections(self) -> list["Connection"]:
        ...
    
    @abstractmethod
    def disconnect(self, conn : "Connection") -> None:
        ...