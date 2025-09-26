from abc import ABC, abstractmethod

class Component(ABC):
    
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def getOutput(self):
        pass