from abc import ABC, abstractmethod

class Component(ABC):
    
    @property
    @abstractmethod
    def type(self) -> str:
        pass