from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import Qt, Signal, QPointF, QRectF
from PySide6.QtGui import QFont, QPen

from view.settings.ComponentItem import ComponentItemSettings

class ComponentItem(QGraphicsObject):
    moved = Signal(QPointF)
    selected = Signal(bool)
    
    def __init__(self, id : str, type : str, pos : str, settings = ComponentItemSettings.default()):
        super().__init__()
        self._type = type
        self._id = id
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self._importSettings(settings)
        self.setPos(pos)
        self.setAcceptHoverEvents(True)
        self.setZValue(3)
        self.setAcceptedMouseButtons(Qt.LeftButton)
    
    def _importSettings(self, settings: ComponentItemSettings):
        self._settings = settings    
        size = settings.SIZE
        self._rect = QRectF(
            -size.width() / 2,
            -size.height() / 2,
            size.width(),
            size.height()
        )
        self._font = QFont()
        self._fontSize = settings.FONT_SIZE
        self._font.setPointSize(self._fontSize)
        self._borderColor = settings.BORDER_COLOR
        self._borderWidth = settings.BORDER_WIDTH
        self._pen = QPen(self._borderColor, self._borderWidth)
        self._textColor = settings.TEXT_COLOR
        self._textPen = QPen(self._textColor)
        self._color = settings.COLOR
        self._selectedColor = settings.SELECTED_COLOR
        self._brush = self._color
    
    @property
    def id(self):
        return self._id
    
    @property
    def type(self):
        return self._type
    
    @property
    def height(self):
        return self._rect.height()

    @property
    def width(self):
        return self._rect.width()

    def boundingRect(self) -> QRectF:
        return self._rect.adjusted(-1, -1, 1, 1)
    
    @property
    def rect(self) -> QRectF:
        return self._rect
    
    def setPos(self, pos:QPointF):
        super().setPos(pos)
        self.moved.emit(pos)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            print(f"Component selection : {value}")
            self._brush = self._selectedColor if value else self._color
            self.update()
            self.selected.emit(value)
        return super().itemChange(change, value)