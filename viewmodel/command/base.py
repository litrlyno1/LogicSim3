from abc import ABC, abstractmethod


class Command(ABC):
    
    def __init__(self):
        self._createdSuccessfully = True
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass
    
    @property
    def createdSuccessfully(self) -> bool:
        return self._createdSuccessfully
    
    @createdSuccessfully.setter
    def createdSuccessfully(self, value: bool):
        self._createdSuccessfully = value