from PySide6.QtCore import QObject, QPointF, Signal

from core.idGenerator import generateId
from model.Component import Component

from viewmodel.Movable import Movable

class ComponentVM(Movable):
    
    def __init__(self, component : Component, pos : QPointF, **kwargs):
        self._component = component
        self._id = generateId(prefix = self.type)
        super().__init__(id = self._id, pos = pos, **kwargs)
    
    @property
    def type(self):
        return self._component.type

    @property
    def id(self):
        return self._id