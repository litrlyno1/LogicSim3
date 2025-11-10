from typing import List

from PySide6.QtCore import QRectF, Qt, Slot, QPointF, Signal
from view.CircuitComponentItem import CircuitComponentItem
from view.settings.BulbItem import BulbItemSettings

class BulbItem(CircuitComponentItem):
    bulbClicked = Signal(str)
    
    def __init__(self, id: str, type:str, pos: QPointF, inputPinIds: List[str], outputPinIds: List[str], settings: BulbItemSettings = BulbItemSettings.default()):
        super().__init__(id, type, pos, inputPinIds, outputPinIds, settings)
        self._importSettings(settings)
    
    def _importSettings(self, settings: BulbItemSettings):
        self._onColor = settings.ON_COLOR