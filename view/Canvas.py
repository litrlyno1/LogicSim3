from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QPainter, QPen, QBrush, QDropEvent, QDragEnterEvent
from PySide6.QtCore import Signal, QPointF, Slot, Qt

from view.EventBus import EventBus
from view.settings.Canvas import CanvasSettings
from view.ComponentItem import ComponentItem
from view.CircuitComponentItem import CircuitComponentItem
from view.SwitchItem import SwitchItem
from view.BulbItem import BulbItem
from view.PinItem import PinItem, InputPinItem, OutputPinItem
from view.ConnectionItem import ConnectionItem
from view.ComponentItemFactory import ComponentItemFactory
from view.CircuitComponentItemFactory import CircuitComponentItemFactory

from viewmodel.CanvasVM import CanvasVM
from viewmodel.ConnectionVM import ConnectionVM

from typing import List

from viewmodel.CircuitComponentVM import ComponentVM

class Canvas(QGraphicsView):
    addComponentsRequest = Signal(list, list)
    #type list, pos list
    moveComponentsRequest = Signal(list, list)
    #ids, newPosList
    removeComponentsRequest = Signal(list)
    #ids
    createConnectionRequest = Signal(str, str, str)
    #id1, id2
    removeConnectionsRequest = Signal(list)
    #ids
    
    def __init__(self, canvasVM : CanvasVM = None, parent = None, settings : CanvasSettings = CanvasSettings.default()):
        super().__init__(parent)
        self._initRegistries()
        self._createEventBus()
        self._importSettings(settings)
        self._setupGraphics()
        self.connectCanvasVM(canvasVM)
        self._initComponentDragging()
        self.update()

    def _initRegistries(self):
        self._componentRegistry: dict[str, ComponentItem] = {}
        self._connectionRegistry : dict[str, ComponentItem] = {}
        self._inputPinRegistry : dict[str, InputPinItem] = {}
        self._outputPinRegistry : dict[str, OutputPinItem] = {}

    def _initComponentDragging(self):
        self._dragStartPos = None
        self._dragging = False
    
    @property
    def pinRegistry(self):
        return self._inputPinRegistry | self._outputPinRegistry
    
    def _importSettings(self, settings: CanvasSettings = CanvasSettings.default()) -> None:
        self._sceneRect = settings.SCENE_RECT
        self._zoom = settings.ZOOM
        self._zoomMin = settings.ZOOM_MIN
        self._zoomMax = settings.ZOOM_MAX
        self._zoomStep = settings.ZOOM_STEP
        self._wheelNotchData = settings.WHEEL_NOTCH_DATA
        self._backgroundColor = settings.BACKGROUND_COLOR
        self._gridColor = settings.GRID_COLOR
        self._gridDarkColor = settings.GRID_COLOR
        self._gridSize = settings.GRID_SIZE
        self._gridMajorFactor = settings.GRID_MAJOR_FACTOR
    
    def _createEventBus(self) -> None:
        self._eventBus = EventBus()
        self.addComponentsRequest.connect(lambda componentTypeList, posList: self._eventBus.emit(eventName="AddComponents", componentTypeList=componentTypeList, posList=posList))
        self.moveComponentsRequest.connect(lambda ids, newPosList: self._eventBus.emit(eventName="MoveComponents", componentIds=ids, newPosList=newPosList))
        self.removeComponentsRequest.connect(lambda ids: self._eventBus.emit(eventName="RemoveComponents", componentIds=ids))
        self.createConnectionRequest.connect(lambda parentPinPair1, parentPinPair2: self._eventBus.emit(eventName="CreateConnection", parentPinPair1=parentPinPair1, parentPinPair2=parentPinPair2))
        self.removeConnectionsRequest.connect(lambda ids: self._eventBus.emit(eventName="RemoveConnections", connectionIds = ids))
    
    @property
    def eventBus(self):
        return self._eventBus
    
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

    def connectCanvasVM(self, canvasVM: CanvasVM):
        self._canvasVM = canvasVM
        if self._canvasVM is not None:
            self._canvasVM.componentAdded.connect(self.addComponent)
            self._canvasVM.circuitComponentAdded.connect(self.addCircuitComponent)
            self._canvasVM.componentPosUpdated.connect(self.moveComponent)
            self._canvasVM.connectionAdded.connect(self.addConnection)

    @Slot(str, str, QPointF)
    def addComponent(self, id, type, pos):
        item = ComponentItemFactory.createComponentItem(id, type, pos)
        self._componentRegistry[id] = item
        self._scene.addItem(item)
    
    @Slot(str, str, QPointF, list, list)
    def addCircuitComponent(self, id, type, pos, inputPinIds, outputPinIds):
        item = CircuitComponentItemFactory.createCircuitComponentItem(id, type, pos, inputPinIds, outputPinIds)
        self._componentRegistry[id] = item
        self._scene.addItem(item)
        for pinItem in item.inputPinItems.values():
            self._inputPinRegistry[pinItem.id] = pinItem
        for pinItem in item.outputPinItems.values():
            self._outputPinRegistry[pinItem.id] = pinItem
    
    @Slot(str, QPointF)
    def moveComponent(self, id, pos):
        item = self._componentRegistry[id]
        item.setPos(pos)
    
    @Slot(str, tuple, tuple)
    def addConnection(self, id, pinId1, pinId2):
        connection = ConnectionItem(id, self.pinRegistry[pinId1], self.pinRegistry[pinId2])
        self._connectionRegistry[id] = connection
        self._scene.addItem(connection)
    
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
        factor = self._zoomStep ** (delta / self._wheelNotchData)
        newZoom = self._zoom * factor
        if newZoom < self._zoomMin or newZoom > self._zoomMax:
            return
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale(factor, factor)
        self._zoom = newZoom
        event.accept()

    def resetZoom(self):
        self.resetTransform()
        self._zoom = 1.0
    
    def mousePressEvent(self, event):
        print("Canvas : mouse pressed")
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            scenePos = self.mapToScene(event.pos())
            item = self._scene.itemAt(scenePos, self.transform())
            if isinstance(item, ComponentItem):
                self._dragging = True
                self._dragStartPos = scenePos
                self._createGhosts(components=self._scene.selectedItems())
    
    def mouseMoveEvent(self, event):
        if self._dragging and self._dragStartPos:
            currentPos = self.mapToScene(event.pos())
            delta = currentPos - self._dragStartPos
            self._dragStartPos = currentPos
            for ghost in self._ghosts:
                ghost.setPos(ghost.pos() + delta)
            event.accept()
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if self._dragging:
            delta = self.mapToScene(event.pos()) - self._dragStartPos
            ids = []
            newPosList = []
            for ghost in self._ghosts:
                ids.append(self._ghosts[ghost].id)
                newPosList.append(ghost.pos()+delta)
                self.scene().removeItem(ghost)
            self._ghosts.clear()
            self._dragStartPos = None
            self._dragging = False
            print(f"Canvas: emitting move components request with ids: {ids} and newPosList {newPosList}")
            self.moveComponentsRequest.emit(ids, newPosList)
            event.accept()
        super().mouseReleaseEvent(event)
    
    def unselectAllItems(self, exceptionItems = []):
        for item in self._scene.items():
            if item not in exceptionItems:
                item.setSelected(False)

    def _createGhosts(self, components: List[ComponentItem]):
        self._ghosts = {}
        for component in components:
            ghost = component.ghost()
            self._ghosts[ghost] = component
            self._scene.addItem(ghost)
    
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
            self.addComponentsRequest.emit([componentType], [pos]) 
            event.acceptProposedAction()
        else:
            event.ignore()