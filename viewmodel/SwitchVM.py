from viewmodel.CircuitComponentVM import CircuitComponentVM
from viewmodel.Toggleable import Toggleable

from PySide6.QtCore import QPointF

class SwitchVM(CircuitComponentVM, Toggleable):
    type = "Switch"
    
    def __init__(self, circuitComponent : "Switch", pos):
        super().__init__(circuitComponent, pos)
    
    def toggle(self):
        self._component.toggle()