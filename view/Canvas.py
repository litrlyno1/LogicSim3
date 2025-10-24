from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPainter, QPen, QBrush, QDropEvent, QDragEnterEvent
from PySide6.QtCore import Signal, QPointF, Slot, Qt

from view.EventBus import EventBus
from view.settings.Canvas import CanvasSettings
from view.ComponentItem import ComponentItem
from view.GateItem import GateItem
from view.SwitchItem import SwitchItem
from view.BulbItem import BulbItem
from view.PinItem import PinItem
from view.ConnectionItem import ConnectionItem

from viewmodel.CanvasVM import CanvasVM
from viewmodel.LogicGateVM import LogicGateVM
from viewmodel.ConnectionVM import ConnectionVM
from viewmodel.SwitchVM import SwitchVM

from typing import List

# temporary dictionaries
from viewmodel.ComponentVM import ComponentVM
from viewmodel.BulbVM import BulbVM
# 

vm_view = {
    ComponentVM: ComponentItem,
    LogicGateVM: GateItem,
    BulbVM: BulbItem,
    SwitchVM : SwitchItem
}

class Canvas(QGraphicsView):
    itemDropped = Signal(str, QPointF)
    itemMoved = Signal(ComponentItem, QPointF)
    connectionCreated = Signal(PinItem, PinItem)
    
    def __init__(self, canvasVM : CanvasVM = None, parent = None, settings : CanvasSettings = CanvasSettings.default()):
        super().__init__(parent)
        self._createEventBus()
        self._connectEventBus()
        self._importSettings(settings)
        self._setupGraphics()
        self._componentRegistry: dict[str, ComponentItem] = {}
        self.connectCanvasVM(canvasVM) #this connection serves an input-only purpose: canvas (view) visually reacts to changes in the VM
        self.update()
        
        self._connectionDragging = False
        self._draggingPin = None
        self._lastComponentItemMoved = None
    
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
        self.itemDropped.connect(lambda componentType, pos: self._eventBus.emit(eventName = "ItemDropped", componentType = componentType, pos = pos))
        self.itemMoved.connect(lambda item, pos: self._eventBus.emit(eventName = "ItemMoved", component = item.componentVM, pos = pos))
        self.connectionCreated.connect(lambda pin1, pin2: self._eventBus.emit(eventName = "ConnectionCreated", 
                                                                                gate1 = pin1.getParentGate().componentItem.componentVM, type1 = pin1.getType(), index1 = pin1.getIndex(),
                                                                                gate2 = pin2.getParentGate().componentItem.componentVM, type2 = pin2.getType(), index2 = pin2.getIndex()))
    
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
            self._canvasVM.componentAdded.connect(self.addComponentItem)
            self._canvasVM.componentPosUpdated.connect(self.componentMovedUpdate)
            self._canvasVM.connectionAdded.connect(self.addConnectionItem)
    
    @Slot(ComponentVM)
    def addComponentItem(self, componentVM):
        print("Placing Component Item: ")
        item = vm_view[componentVM.__class__](componentVM)
        print(f"Component Item added with id {componentVM.id}")
        self._componentRegistry[componentVM.id] = item 
        self._scene.addItem(item)
        self.connectItem(item)
    
    @Slot(object)
    def addConnectionItem(self, connectionVM : ConnectionVM):
        print("Canvas: adding connection")
        pin1 = self._componentRegistry[connectionVM.getGate1().id].getInputPin(connectionVM._index1) if connectionVM._type1 == "input" else self._componentRegistry[connectionVM.getGate1().id].getOutputPin(connectionVM._index1)
        pin2 = self._componentRegistry[connectionVM.getGate2().id].getInputPin(connectionVM._index2) if connectionVM._type2 == "input" else self._componentRegistry[connectionVM.getGate2().id].getOutputPin(connectionVM._index2)
        item = ConnectionItem(pin1, pin2)
        self._scene.addItem(item)
    
    def connectItem(self, item : ComponentItem):
        item.signals.moved.connect(self.componentMoved)
        if hasattr(item, "_inputPins"):
            self.connectPins(item.getInputPins())
        if hasattr(item, "_outputPins"):
            self.connectPins(item.getOutputPins())
    
    def connectPins(self, pins : List[PinItem]):
        for pin in pins:
            pin.signals.mousePressed.connect(self._manageDragging)
    
    @Slot(ComponentItem, QPointF)
    def componentMoved(self, componentItem, pos):
        print("Canvas got signal : component moved")
        self.itemMoved.emit(componentItem, pos)
    
    @Slot(str, QPointF)
    def componentMovedUpdate(self, id, pos):
        print(f"Moving component with id {id}")
        item = self._componentRegistry[id]
        item.setPos(pos)
        item.onItemMoved()
    
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
        print("Canvas : mouse pressed")
        scenePos = self.mapToScene(event.pos())
        item = self._scene.itemAt(scenePos, self.transform())
        print(f"Canvas: clicked item {item}")
        #print("Unselected all")
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        print("Canvas : mouse released")
        if not isinstance(self._scene.itemAt(self.mapToScene(event.pos()), self.transform()), PinItem):
            self._abortDragging()
        super().mouseReleaseEvent(event)
    
    @Slot(PinItem)
    def _manageDragging(self, pin : PinItem):
        if not self._draggingPin:
            print("starting dragging")
            self._draggingPin = pin
            self.unselectAllItems(exceptionItems= [pin])
        else:
            print("finishing dragging")
            pins = [self._draggingPin, pin]
            if ConnectionItem.isViablePinPair(self._draggingPin, pin):
                self.connectionCreated.emit(self._draggingPin, pin)
            self._abortDragging()
    
    def _abortDragging(self):
        self._draggingPin = None
    
    def unselectAllItems(self, exceptionItems = []):
        for item in self._scene.items():
            if item not in exceptionItems:
                item.setSelected(False)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            componentType = event.mimeData().text()
            pos = self.mapToScene(event.position().toPoint())
            print(f"Dropped {componentType} at {pos}")
            self.itemDropped.emit(componentType, pos)
            event.acceptProposedAction()
        else:
            event.ignore()