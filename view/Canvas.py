from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPainter, QPen, QBrush, QDropEvent, QDragEnterEvent
from PySide6.QtCore import Signal, QPointF, Slot, Qt

from view.EventBus import EventBus
from view.settings.Canvas import CanvasSettings
from view.GateItem import GateItem
from view.PinItem import PinItem

from viewmodel.CanvasVM import CanvasVM
from viewmodel.LogicGateVM import LogicGateVM

class Canvas(QGraphicsView):
    itemDropped = Signal(str, QPointF)
    itemMoved = Signal(GateItem, QPointF)
    
    def __init__(self, canvasVM : CanvasVM = None, parent = None, settings : CanvasSettings = CanvasSettings.default()):
        super().__init__(parent)
        self._createEventBus()
        self._connectEventBus()
        self._importSettings(settings)
        self._setupGraphics()
        self._gateRegistry: dict[str, GateItem] = {}
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
            self._canvasVM.gatePosUpdated.connect(self.gateMovedUpdate)
    
    @Slot(LogicGateVM)
    def addGateItem(self, logicGateVM):
        print("Placing GateItem: ")
        item = GateItem(logicGateVM)
        print(f"Gate Item added with id {logicGateVM.getId()}")
        self._gateRegistry[logicGateVM.getId()] = item 
        self._scene.addItem(item)
        item.signals.moved.connect(self.gateMoved)
    
    @Slot(GateItem, QPointF)
    def gateMoved(self, gateItem, pos):
        print("Canvas got signal : gate moved")
        print("Registry (canvas view): ")
        print(self._gateRegistry)
        self.itemMoved.emit(gateItem, pos)
    
    @Slot(str, QPointF)
    def gateMovedUpdate(self, id, pos):
        print(f"Moving gate with id {id}")
        self._gateRegistry[id].setPos(pos)
    
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
        print(item)
        if not event.modifiers() & Qt.ShiftModifier: 
            if isinstance(item, GateItem):
                self.unselectAllItems(exceptionItems = [item] + item.getInputPins() + item.getOutputPins())
            elif isinstance(item, PinItem):
                self.unselectAllItems()
            else:
                self.unselectAllItems()
            #print("Unselected all")
        super().mousePressEvent(event)
    
    def unselectAllItems(self, exceptionItems = []):
        print(self._scene.items())
        for item in self._scene.items():
            if item not in exceptionItems:
                print("unselecting this one")
                item.setSelected(False)
    
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