from PySide6.QtCore import QObject, QPointF

from viewmodel.ComponentVM import ComponentVM
from model.Switch import Switch

class SwitchVM(ComponentVM):
    type = "switch"
    
    def __init__(self, pos: QPointF = QPointF(0,0)):
        super().__init__(component = Switch(), pos = pos)
        self._pos = pos