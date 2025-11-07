from PySide6.QtCore import Signal, QPointF

from view.ItemProperty import ItemProperty

class MovableRelay(ItemProperty):
    moved = Signal(str, QPointF)
    
    def __init__(self, parentId : str, pos : QPointF):
        super().__init__(parentId)
        self._pos = pos
    
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos : QPointF):
        self._pos = pos
    
    def move(self, pos : QPointF):
        self.moved.emit(self._parentId, pos)