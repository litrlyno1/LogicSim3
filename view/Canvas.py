from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPainter, QPen, QBrush, QDropEvent, QDragEnterEvent
from PySide6.QtCore import Signal, QPointF, Slot, Qt

from view.EventBus import EventBus
from view.settings.Canvas import CanvasSettings
from view.GateItem import GateItem

from viewmodel.CanvasVM import CanvasVM
from viewmodel.LogicGateVM import LogicGateVM

class Canvas(QGraphicsView):
    itemDropped = Signal(str, QPointF)
    itemMoved = Signal(LogicGateVM, QPointF)
    
    def __init__(self, canvasVM : CanvasVM = None, parent = None, settings : CanvasSettings = CanvasSettings.default()):
        super().__init__(parent)
        self._createEventBus()
        self._connectEventBus()
        self._importSettings(settings)
        self._setupGraphics()
        self.connectCanvasVM(canvasVM) #this connection serves an input-only purpose: canvas (view) visually reacts to changes in the VM
        self.update()
        
        self._lastGateMoved = None
    
    def _importSettings(self, settings: CanvasSettings = CanvasSettings.default()) -> None:
        self._sceneRect = settings.SCENE_RECT
        self._zoom = settings.ZOOM
        self._zoomMin = settings.ZOOM_MIN
        self._zoomMax = settings.ZOOM_MAX
        self._zoomStep = settings.ZOOM_STEP
        self._backgroundColor = settings.BACKGROUND_COLOR
        self._gridColor = settings.GRID_COLOR
        self._gridDarkColor = settings.GRID_COLOR
        self._gridSize = settings.GRID_SIZE
        self._gridMajorFactor = settings.GRID_MAJOR_FACTOR
    
    def _createEventBus(self) -> None:
        self._eventBus = EventBus()
    
    def _connectEventBus(self) -> None:
        self.itemDropped.connect(lambda gateType, pos: self._eventBus.emit(eventName = "ItemDropped", gateType = gateType, pos = pos))
        self.itemMoved.connect(lambda gate, pos: self._eventBus.emit(eventName = "ItemMoved", gate = gate, pos = pos))
    
    def _setupGraphics(self) -> None:
        self._scene = QGraphicsScene(self)
        self._scene.setSceneRect(self._sceneRect)
        self.setScene(self._scene)
        self._scene.installEventFilter(self)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setMouseTracking(True)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setInteractive(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QBrush(self._backgroundColor))
    
    def getEventBus(self) -> EventBus:
        return self._eventBus

    def connectCanvasVM(self, canvasVM: CanvasVM):
        self._canvasVM = canvasVM
        if self._canvasVM is not None:
            self._canvasVM.gateAdded.connect(self.addGateItem)
            self._canvasVM.gateMoved.connect(self.gateMovedUpdate)
    
    @Slot(LogicGateVM)
    def addGateItem(self, logicGateVM):
        print("Placing GateItem: ")
        logicGateVM = GateItem(logicGateVM)
        self._scene.addItem(logicGateVM)
        logicGateVM.signals.moved.connect(self.gateMoved)
    
    @Slot(GateItem, QPointF)
    def gateMoved(self, gateItem, pos):
        print("Canvas got signal : gate moved")
        self._lastGateMoved = gateItem
        self.itemMoved.emit(gateItem.getLogicGateVM(), pos)
    
    @Slot(GateItem, QPointF)
    def gateMovedUpdate(self, gate, pos):
        print("canvas got answer from canvasVM")
        self._lastGateMoved.setPos(pos)
    
    def drawBackground(self, painter: QPainter, rect):
        super().drawBackground(painter, rect)
        painter.setBrush(QBrush(self._backgroundColor))
        painter.drawRect(self._scene.sceneRect())
        left = int(rect.left()) - (int(rect.left()) % self._gridSize)
        top = int(rect.top()) - (int(rect.top()) % self._gridSize)

        painter.setPen(QPen(self._gridColor, 0))
        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self._gridSize

        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self._gridSize

        major = self._gridSize * self._gridMajorFactor
        painter.setPen(QPen(self._gridDarkColor, 0))
        x = int(rect.left()) - (int(rect.left()) % major)
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += major
        y = int(rect.top()) - (int(rect.top()) % major)
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += major
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta == 0:
            return
        factor = self._zoomStep if delta > 0 else 1 / self._zoomStep
        newZoom = self._zoom * factor
        if newZoom < self._zoomMin or newZoom > self._zoomMax:
            return
        self.scale(factor, factor)
        self._zoom = newZoom
        event.accept()

    def resetZoom(self):
        self.resetTransform()
        self._zoom = 1.0
    
    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        item = self._scene.itemAt(scenePos, self.transform())
        if not event.modifiers() & Qt.ShiftModifier: #if shift is not pressed
            self.unselectAllItems(exceptionItem= item)
            print("Unselected all")
        super().mousePressEvent(event)
    
    def unselectAllItems(self, exceptionItem = None):
        for item in self._scene.items():
            if item is not exceptionItem:
                item.unselect()
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            gateType = event.mimeData().text()
            pos = self.mapToScene(event.position().toPoint())
            print(f"Dropped {gateType} at {pos}")
            self.itemDropped.emit(gateType, pos)
            event.acceptProposedAction()
        else:
            event.ignore()