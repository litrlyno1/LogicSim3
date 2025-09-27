from PySide6.QtCore import Signal, QObject
from model.Component import Component

class ComponentController(QObject):
    inputChanged = Signal(bool)
    
    def __init__(self, component: Component):
        super().__init__()
    
    