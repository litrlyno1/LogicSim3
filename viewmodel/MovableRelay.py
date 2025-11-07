from viewmodel.ObjectProperty import ObjectProperty
from PySide6.QtCore import QPointF, Signal

class MovableRelay(ObjectProperty):
    posChanged = Signal(str, QPointF)
    
    def __init__(self, parentId : str, pos : QPointF):
        super().__init__(parentId)
        self._pos = pos
    
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos : QPointF):
        self._pos = pos
        self.posChanged.emit(self._parentId, pos)