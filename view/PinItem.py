from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen
from view.settings.PinItem import PinItemSettings

class PinItem(QGraphicsEllipseItem):

    def __init__(self, parentGate : "GateItem", type : str, index : int, settings : PinItemSettings = PinItemSettings.default()):
        self._parentGate = parentGate
        self._type = type
        self._index = index
        self._importSettings(settings)
        super().__init__(-self._radius, -self._radius, self._radius*2, self._radius*2, parentGate)
        
        self._setupGraphics()
        self.setSelected(False)
    
    def _importSettings(self, settings : PinItemSettings):
        self._radius = settings.RADIUS
        self._color = settings.COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._borderColor = settings.BORDER_COLOR
        self._borderWidth = settings.BORDER_WIDTH
    
    def _setupGraphics(self):
        self.setPos(QPointF(self._getRelX(), self._getRelY()))
        #print(self.pos().y())
        self.setBrush(self._color)
        self.setPen(QPen(self._borderColor, self._borderWidth))
        self.setZValue(2)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
    
    def setSelected(self, selected : bool):
        super().setSelected(selected)
        if selected:
            self.setBrush(self._selectedColor)
        else:
            self.setBrush(self._color)
        self.update()
    
    def _getRelX(self):
        width = self._parentGate.getWidth()
        if self._type == "output":
            return width/2
        else:
            return -width/2
    
    def _getRelY(self):
        height = self._parentGate.getHeight()
        if self._type == "output":
            pinAmount = self._parentGate.getLogicGateVM().getGate().getNumOutputs()
        else:
            pinAmount = self._parentGate.getLogicGateVM().getGate().getNumInputs()
        
        step = height / (pinAmount+1)
        y = (self._index+1)*step
        return y - height/2