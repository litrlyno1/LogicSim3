from model.Interfaces import IToggleable
from model.Observer import Observable
from model.Component import Component

class Switch(Component, Observable, IToggleable):
    type = "Switch"
    
    def __init__(self):
        self._value = False
    
    def toggle(self):
        self._value = not self._value
        self.update()
    
    def getOutput(self):
        return self._value