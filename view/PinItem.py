from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, Signal, QObject, Slot
from PySide6.QtGui import QPen
from view.settings.PinItem import PinItemSettings

class PinItemSignals(QObject):
    mousePressed = Signal(object)

class PinItem(QGraphicsEllipseItem):

    def __init__(self, parentComponent : "ComponentItem", type : str, index : int, settings : PinItemSettings = PinItemSettings.default()):
        self._parentComponent = parentComponent
        self._type = type
        self._index = index
        self._importSettings(settings)
        super().__init__(-self._radius, -self._radius, self._radius*2, self._radius*2)
        self.setParentItem(parentComponent)
        self.signals = PinItemSignals()
        
        self._setupGraphics()
        self.setFlags(
            QGraphicsEllipseItem.ItemIsSelectable |
            QGraphicsEllipseItem.ItemSendsGeometryChanges
        )
        self._isParentSelected = self._parentComponent.isSelected()
        self._connectionItems = []
    
    def _importSettings(self, settings : PinItemSettings):
        self._radius = settings.RADIUS
        self._color = settings.COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._draggingColor = settings.DRAGGING_COLOR
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
    
    def getparentComponent(self):
        return self._parentComponent
    
    def getType(self):
        return self._type
    
    def getIndex(self):
        return self._index
    
    @property 
    def isParentSelected(self):
        return self._isParentSelected
    
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
    
    def _getRelX(self):
        width = self._parentComponent.getWidth()
        if self._type == "output":
            return width/2
        else:
            return -width/2
    
    def _getRelY(self):
        height = self._parentComponent.getHeight()
        if self._type == "output":
            pinAmount = self._parentComponent.componentVM.component.getNumOutputs()
        else:
            pinAmount = self._parentComponent.componentVM.component.getNumInputs()
        
        step = height / (pinAmount+1)
        y = (self._index+1)*step
        return y - height/2