from viewmodel.CircuitComponentVM import CircuitComponentVM
from viewmodel.Clickable import Clickable

from PySide6.QtCore import QPointF

class SwitchVM(CircuitComponentVM, Clickable):
    type = "SwitchVM"
    
    def __init__(self, circuitComponent : "Bulb", pos):
        super().__init__(circuitComponent, pos)
    
    def toggle(self):
        self._component.toggle()

    def onClick(self):
        self.toggle()