from PySide6.QtCore import QPointF

from viewmodel.ComponentVM import ComponentVM
from model.Bulb import Bulb

class BulbVM(ComponentVM):
    type = "bulb"
    
    def __init__(self, pos: QPointF = QPointF(0,0)):
        super().__init__(component=Bulb(), pos = pos)
        self._pos = pos