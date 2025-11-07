from PySide6.QtWidgets import QGraphicsItem

from view.Movable import Movable

class ComponentItem(QGraphicsItem, Movable):
    
    def __init__(self, id : str, type : str, pos : str):
        self._type = type
        QGraphicsItem.__init__(self)
        Movable.__init__(self, id = id, pos = pos)
        self._id = id
    
    @property
    def id(self):
        return self._id
    
    @property
    def type(self):
        return self._type