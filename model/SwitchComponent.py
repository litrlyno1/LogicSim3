from Component import Component
from Interfaces import IToggleable

class Switch(Component, IToggleable):
    
    def __init__(self):
        super().__init__()
    
    def toggle(self):
        return not self._value
    
    def getOutput(self):
        return self._value