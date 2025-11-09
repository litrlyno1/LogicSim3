from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, Signal, QRect
from PySide6.QtGui import QPen, QPainter

from view.settings.PinItem import PinItemSettings, InputPinItemSettings, OutputPinItemSettings

class PinItem(QGraphicsObject):
    parentMoved = Signal(QPointF)
    selected = Signal(str)
    
    def __init__(self, parentItem : "CircuitComponentItem", id: str, relativePos: QPointF, settings : PinItemSettings = PinItemSettings.default()):
        self._importSettings(settings)
        super().__init__()
        self._id = id
        self.setParentItem(parentItem)
        parentItem.moved.connect(lambda pos: self.parentMoved.emit(pos))
        parentItem.selected.connect(lambda val: self.setParentSelected(val))
        self._setupGraphics(relativePos)
        self.setFlags(
            QGraphicsObject.ItemIsSelectable |
            QGraphicsObject.ItemSendsGeometryChanges
        )
        self._parentSelected = parentItem.isSelected()
    
    def _importSettings(self, settings : PinItemSettings):
        self._radius = settings.RADIUS
        self._color = settings.COLOR
        self._parentSelectedColor = settings.PARENT_SELECTED_COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._draggingColor = settings.DRAGGING_COLOR
        self._borderColor = settings.BORDER_COLOR
        self._borderWidth = settings.BORDER_WIDTH
    
    def _setupGraphics(self, relativePos : QPointF):
        self._rect = QRect(-self._radius, -self._radius, 2*self._radius, 2*self._radius)
        self.setPos(relativePos)
        self._brush = self._color
        self._pen = QPen(self._borderColor, self._borderWidth)
        self.setZValue(2)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
    
    def boundingRect(self):
        return self._rect
    
    @property
    def center(self) -> QPointF:
        return self.sceneBoundingRect().center
    
    @property
    def type(self) -> str:
        raise NotImplementedError("Pin subclasses must define their type")

    @property
    def id(self):
        return self._id
    
    def setSelected(self, value : bool) -> None:
        super().setSelected(value)
        if value:
            self.selected.emit(self._id)
            self._brush = self._selectedColor
        else:
            self._brush = self._parentSelectedColor if self.parentSelected else self._color
        self.update()
    
    @property
    def parentSelected(self) -> bool:
        return self._parentSelected
    
    def setParentSelected(self, value : bool):
        self._parentSelected = value
        self._brush = self._parentSelectedColor if value else self._color
        self.update()

    def paint(self, painter : QPainter, option, widget = None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(self._rect)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.setSelected(value)
        return super().itemChange(change, value)

class InputPinItem(PinItem):
    def __init__(self, parentItem : "CircuitComponentItem", id: str, relativePos: QPointF, settings : PinItemSettings = InputPinItemSettings.default()):
        super().__init__(parentItem, id, relativePos)
        print(f"Initialized inputPinItem with {relativePos}")

class OutputPinItem(PinItem):
    def __init__(self, parentItem : "CircuitComponentItem", id: str, relativePos: QPointF, settings : PinItemSettings = OutputPinItemSettings.default()):
        super().__init__(parentItem, id, relativePos)
        print(f"Initialized outputPinItem with {relativePos}")