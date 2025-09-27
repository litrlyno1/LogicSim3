from PySide6.QtCore import Signal, QObject
from model.Component import Component

class ComponentController(QObject):
    
    def __init__(self, component: Component):
        super().__init__()