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
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemIsMovable | # we don't set the flag selectable, because we implement our own logic
            QGraphicsRectItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        
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
        self._brush = self._color
    
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
        print("gateitem: clicked")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        print("gateitem : released")
        super().mouseReleaseEvent(event)
    
    def itemChange(self, change, value):
        print(f"GateItem: change = {change}")
        if change == QGraphicsItem.ItemSelectedHasChanged:
            print(f"GateItem selection : {value}")
            self._brush = self._selectedColor if value else self._color
            for pin in self._inputPins + self._outputPins:
                pin.isParentSelected = value
            self.update()
        elif change == QGraphicsItem.ItemPositionChange:
            self.signals.moved.emit(self, self.pos())
        return super().itemChange(change, value)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawRect(self.rect())

        painter.setFont(self._font)
        painter.setPen(self._textPen)
        gate_type = self._logicGateVM.getGateType()
        painter.drawText(self.rect(), Qt.AlignCenter, gate_type)