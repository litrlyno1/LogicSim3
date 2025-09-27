from Component import Component
from Interfaces import IToggleable

class Switch(Component, IToggleable):
    
    def __init__(self):
        super().__init__()
        self._value = False
    
    '''def toggle(self):
        if self._value == False:
            self._value = True
        else:
            self._value = False'''
    
    def getOutput(self):
        return self._value