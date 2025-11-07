from view.MovableRelay import MovableRelay

from PySide6.QtCore import QPointF

class Movable:
    
    def __init__(self, id : str, pos : QPointF, **kwargs):
        self._movableRelay = MovableRelay(id, pos)
        super().__init__(id = id, **kwargs)
    
    @property
    def pos(self):
        return self._movableRelay.pos
    
    @pos.setter
    def pos(self, pos : QPointF):
        self._movableRelay.pos = pos
    
    @property
    def move(self, pos: QPointF):
        self._movableRelay.move(pos)