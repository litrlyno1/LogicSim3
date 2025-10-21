from PySide6.QtCore import QObject, Signal, QPointF

from model import Component
from core.idGenerator import generateId

class ComponentVM(QObject):
    posChanged = Signal(str, QPointF)
    
    def __init__(self, component : Component, pos : QPointF):
        super().__init__()
        self._component = component
        self._id = generateId(prefix= self.__class__.type)
        self._pos = pos
    
    @property 
    def component(self):
        return self._component

    @property
    def pos(self):
        return self._pos