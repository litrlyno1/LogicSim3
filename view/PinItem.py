from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, Signal, QObject, Slot
from PySide6.QtGui import QPen
from view.settings.PinItem import PinItemSettings

from abc import ABC, abstractmethod

class PinItem(QGraphicsEllipseItem, ABC):
    
    @property
    @abstractmethod
    def type() -> str:
        pass
    
    @abstractmethod
    def relX(width: float) -> QPointF:
        pass
    
    @abstractmethod
    def relY(height: float) -> QPointF:
        pass

    def __init__(self, parentItem : "CircuitComponentItem", id: str, relativePos : QPointF, settings : PinItemSettings = PinItemSettings.default()):
        self._importSettings(settings)
        super().__init__(-self._radius, -self._radius, self._radius*2, self._radius*2)
        self._id = id
        self.setParentItem(parentItem)
        self._setupGraphics(relativePos)
        self.setFlags(
            QGraphicsEllipseItem.ItemIsSelectable |
            QGraphicsEllipseItem.ItemSendsGeometryChanges
        )
        self._isParentSelected = self._parentComponent.isSelected()
    
    def _importSettings(self, settings : PinItemSettings):
        self._radius = settings.RADIUS
        self._color = settings.COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._draggingColor = settings.DRAGGING_COLOR
        self._borderColor = settings.BORDER_COLOR
        self._borderWidth = settings.BORDER_WIDTH
    
    def _setupGraphics(self, relativePos : QPointF):
        self.setPos(relativePos)
        #print(self.pos().y())
        self.setBrush(self._color)
        self.setPen(QPen(self._borderColor, self._borderWidth))
        self.setZValue(2)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
    
    @property 
    def selected(self):
        return self._selected
    
    @isParentSelected.setter
    def isParentSelected(self, value : bool):
        self._isParentSelected = value
        if value:
            self.setBrush(self._selectedColor)
        else:
            self.setBrush(self._color)
        self.update()
    
    def onParentMoved(self):
        if self._connectionItems:
            for connectionItem in self._connectionItems:
                connectionItem.update_path()
                connectionItem.update()
    
    def addConnectionItem(self, connectionItem):
        self._connectionItems.append(connectionItem)
    
    def removeConnectionItem(self, connectionItem):
        self._connectionItems.remove(connectionItem)
    
    def mousePressEvent(self, event):
        print("Pin: mouse pressed")
        super().mousePressEvent(event)
        event.accept()
        self.signals.mousePressed.emit(self)
    
    def mouseReleaseEvent(self, event):
        print("Pin: mouse released")
        super().mouseReleaseEvent(event)
        event.accept()
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            print("PinItem : Position change")
        return super().itemChange(change, value)

    @staticmethod
    def relY(index: int, pinsNum : int, height: float):
            verticalStep = height / (pinsNum+1)
            y = (index+1)*verticalStep
            return y-height/2

    @staticmethod
    def _inputPinRelX(width):
        return -width/2

    @staticmethod
    def _outputPinRelX(width):
        return width/2

class InputPinItem(PinItem):
    def __init__(self, parentItem : "CircuitComponentItem", id: str, settings : PinItemSettings = PinItemSettings.default()):
        super().__init__(parentItem, id)

    def relX(width: float) -> float:
        return -width/2
    
    def relY(height: float) -> float:
        

class OutputPinItem(PinItem):
    def __init__(self, parentItem : "CircuitComponentItem", id: str, index: int, settings : PinItemSettings = PinItemSettings.default()):
        super().__init__(parentItem, id)
    
    def relX(width: float) -> float:
        return width/2
    
    def relY(height: float, pinNum: int) -> float:
        step = height / (pinNum+1)
        y = (self._index+1)*step
        return y - self.height/2