from abc import ABC, abstractmethod

class IToggleable(ABC):
    
    def __init__(self):
        super().__init__()
        self._value = False
    
    @abstractmethod
    def toggle(self):
        pass