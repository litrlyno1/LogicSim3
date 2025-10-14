from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import QRectF, Qt, QPointF, Signal, QObject
from viewmodel.LogicGateVM import LogicGateVM
from view.settings.GateItem import GateItemSettings
from view.PinItem import PinItem

class GateItemSignals(QObject):
    moved = Signal(object, QPointF)

class GateItem(QGraphicsRectItem):
    
    def __init__(self, logicGateVM: LogicGateVM, settings: GateItemSettings = GateItemSettings.default()):
        self._logicGateVM = logicGateVM
        self._importSettings(settings)
        self.signals = GateItemSignals()
        super().__init__(self._boundingRect)
        self.initPinItems()

        self.setPos(self._logicGateVM.getPos())
        self.setFlags(
            QGraphicsRectItem.ItemIsMovable | # we don't set the flag selectable, because we implement our own logic
            QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        
        self.setSelected(False)
        self._dragStartPos = None  #for movement tracking

    def _importSettings(self, settings: GateItemSettings):
        size = settings.SIZE
        self._boundingRect = QRectF(
            -size.width() / 2,
            -size.height() / 2,
            size.width(),
            size.height()
        )
        self._font = QFont()
        self._font.setPointSize(settings.FONT_SIZE)
        self._pen = QPen(settings.BORDER_COLOR, settings.BORDER_WIDTH)
        self._textPen = QPen(settings.TEXT_COLOR)
        self._color = settings.COLOR
        self._selectedColor = settings.SELECTED_COLOR
    
    def getHeight(self):
        return self._boundingRect.height()

    def getWidth(self):
        return self._boundingRect.width()
    
    def initPinItems(self):
        self.initInputPins()
        self.initOutputPins()
    
    def initInputPins(self):
        self._inputPins = []
        #print(f"Number of input pins: {self._logicGateVM.getGate().getNumInputs()}")
        for index in range(self._logicGateVM.getGate().getNumInputs()):
            self._inputPins.append(PinItem(parentGate=self, type = "input", index = index))
        
    def initOutputPins(self):
        self._outputPins = []
        #print(f"Number of output pins: {self._logicGateVM.getGate().getNumOutputs()}")
        for index in range(self._logicGateVM.getGate().getNumOutputs()):
            self._outputPins.append(PinItem(parentGate=self, type = "output", index = index))
    
    def getInputPins(self):
        return self._inputPins
    
    def getOutputPins(self):
        return self._outputPins
    
    def getLogicGateVM(self):
        return self._logicGateVM

    def mousePressEvent(self, event):
        print("gateitem clicked")
        self._dragStartPos = self.pos()
        super().mousePressEvent(event)
        self.toggleSelected()

    def mouseReleaseEvent(self, event):
        if self._dragStartPos and self.pos() != self._dragStartPos:
            self.signals.moved.emit(self, self.pos())
        self._dragStartPos = None
        super().mouseReleaseEvent(event)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.setSelected(True)
            self.update()
        return super().itemChange(change, value)

    def setSelected(self, selected : bool):
        self.setFlag(QGraphicsItem.ItemIsSelectable, selected)
        for pin in self._inputPins:
            pin.setSelected(selected)
        for pin in self._outputPins:
            pin.setSelected(selected)
        self.update()
    
    def toggleSelected(self):
        if self.isSelected():
            self.setSelected(False)
        else:
            self.setSelected(True)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        if self.isSelected():
            painter.setBrush(self._selectedColor)
        else:
            painter.setBrush(self._color)
        painter.setPen(self._pen)
        painter.drawRect(self.rect())

        painter.setFont(self._font)
        painter.setPen(self._textPen)
        gate_type = self._logicGateVM.getGateType()
        painter.drawText(self.rect(), Qt.AlignCenter, gate_type)