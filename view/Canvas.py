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
    createConnectionRequest = Signal(tuple, tuple)
    #(parent id, pin id), (parent id, pin id),
    removeConnectionsRequest = Signal(list)
    #ids
    componentToggleRequest = Signal(str)
    
    def __init__(self, canvasVM : CanvasVM = None, parent = None, settings : CanvasSettings = CanvasSettings.default()):
        super().__init__(parent)
        self._initRegistries()
        self._createEventBus()
        self._importSettings(settings)
        self._setupGraphics()
        self.connectCanvasVM(canvasVM)
        self._initComponentDragging()
        self._initConnectionDragging()
        self.update()

    def _initRegistries(self):
        self._componentRegistry: dict[str, ComponentItem] = {}
        self._connectionRegistry : dict[str, ComponentItem] = {}

    def _initComponentDragging(self):
        self._componentDragStartPos = None
        self._componentDragging = False
    
    def _initConnectionDragging(self):
        self._connectionDragStartPin = None
        self._connectionDragging = False
    
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
        self._pasteOffset = settings.PASTE_OFFSET
    
    def _createEventBus(self) -> None:
        self._eventBus = EventBus()
        self.addComponentsRequest.connect(lambda componentTypeList, posList: self._eventBus.emit(eventName="AddComponents", componentTypeList=componentTypeList, posList=posList))
        self.moveComponentsRequest.connect(lambda ids, newPosList: self._eventBus.emit(eventName="MoveComponents", componentIds=ids, newPosList=newPosList))
        self.removeComponentsRequest.connect(lambda ids: self._eventBus.emit(eventName="RemoveComponents", componentIds=ids))
        self.createConnectionRequest.connect(lambda parentPinPair1, parentPinPair2: self._eventBus.emit(eventName="CreateConnection", parentPinPair1=parentPinPair1, parentPinPair2=parentPinPair2))
        self.removeConnectionsRequest.connect(lambda ids: self._eventBus.emit(eventName="RemoveConnections", connectionIds = ids))
        self.componentToggleRequest.connect(lambda id: self._eventBus.emit(eventName="ToggleComponent", componentId = id))
    
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
            self._canvasVM.componentRemoved.connect(self.removeComponent)
            self._canvasVM.circuitComponentAdded.connect(self.addCircuitComponent)
            self._canvasVM.componentPosUpdated.connect(self.moveComponent)
            self._canvasVM.connectionAdded.connect(self.addConnection)
            self._canvasVM.connectionRemoved.connect(self.removeConnection)
            self._canvasVM.componentValueUpdated.connect(self.updateComponentValue)

    @Slot(str, str, QPointF)
    def addComponent(self, id, type, pos):
        item = ComponentItemFactory.createComponentItem(id, type, pos)
        self._componentRegistry[id] = item
        self._scene.addItem(item)
    
    @Slot(str)
    def removeComponent(self, id):
        item = self._componentRegistry[id]
        self._scene.removeItem(item)
    
    @Slot(str, str, QPointF, list, list, bool)
    def addCircuitComponent(self, id, type, pos, inputPinIds, outputPinIds, value):
        item = CircuitComponentItemFactory.createCircuitComponentItem(id, type, pos, inputPinIds, outputPinIds, value)
        self._componentRegistry[id] = item
        self._scene.addItem(item)
        if isinstance(item, SwitchItem):
            item.toggleRequested.connect(lambda id: self.componentToggleRequest.emit(id))
    
    @Slot(str, QPointF)
    def moveComponent(self, id, pos):
        item = self._componentRegistry[id]
        item.setPos(pos)
    
    @Slot(str, tuple, tuple)
    def addConnection(self, id, parentPinPair1, parentPinPair2):
        pin1 = self._componentRegistry[parentPinPair1[0]].pinItems[parentPinPair1[1]]
        pin2 = self._componentRegistry[parentPinPair2[0]].pinItems[parentPinPair2[1]]
        connection = ConnectionItem(id, pin1, pin2)
        self._connectionRegistry[id] = connection
        self._scene.addItem(connection)
        print(connection.scene())
        print(connection.boundingRect())
    
    @Slot(str)
    def removeConnection(self, id):
        self._scene.removeItem(self._connectionRegistry[id])
        self._connectionRegistry.pop(id)
    
    @Slot(str, bool)
    def updateComponentValue(self, id, value):
        self._componentRegistry[id].value = value
    
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Backspace):
            self.removeSelected()
        if (event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier)):
            self.copySelectedComponents()
        elif (event.key() == Qt.Key_V and (event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier)):
            self.pasteSelectedComponents()
        elif (event.key() == Qt.Key_Z and event.modifiers() & Qt.ShiftModifier and (event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier)):
            self._eventBus.emit(eventName="Redo")
        elif (event.key() == Qt.Key_Z  and (event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier)):
            self._eventBus.emit(eventName="Undo")
        else:
            super().keyPressEvent(event)
    
    def copySelectedComponents(self):
        self._copiedComponents = [item for item in self._scene.selectedItems() if isinstance(item, ComponentItem)]
    
    def pasteSelectedComponents(self):
        if self._copiedComponents:
            typeList = [component.type for component in self._copiedComponents]
            posList = [component.pos()+self._pasteOffset for component in self._copiedComponents]
            self.addComponentsRequest.emit(typeList, posList)
    
    def removeSelected(self):
        componentIds = [item.id for item in self._scene.selectedItems() if isinstance(item, ComponentItem)]
        self.removeComponentsRequest.emit(componentIds)
    
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
            if isinstance(item, PinItem):
                self._connectionDragging = True
                self._connectionDragStartPin = item
                self._createConnectionGhost(self._connectionDragStartPin.scenePos(), scenePos)
            elif isinstance(item, ComponentItem):
                self._componentDragging = True
                self._componentDragStartPos = scenePos
                components = [component for component in self._scene.selectedItems() if isinstance(component, ComponentItem)]
                self._createComponentGhosts(components)
    
    def mouseMoveEvent(self, event):
        if self._componentDragging:
            currentPos = self.mapToScene(event.pos())
            delta = currentPos - self._componentDragStartPos
            self._componentDragStartPos = currentPos
            for ghost in self._ghostComponents:
                ghost.setPos(ghost.pos() + delta)
            event.accept()
        elif self._connectionDragging:
            currentPos = self.mapToScene(event.pos())
            self._updateConnectionGhost(newEnd = currentPos)
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        currentPos = self.mapToScene(event.pos())
        if self._componentDragging:
            delta = currentPos - self._componentDragStartPos
            ids = []
            newPosList = []
            for ghost in self._ghostComponents:
                ids.append(self._ghostComponents[ghost].id)
                newPosList.append(ghost.pos()+delta)
                self.scene().removeItem(ghost)
            self._ghostComponents.clear()
            self._componentDragStartPos = None
            self._componentDragging = False
            print(f"Canvas: emitting move components request with ids: {ids} and newPosList {newPosList}")
            self.moveComponentsRequest.emit(ids, newPosList)
            event.accept()
        elif self._connectionDragging:
            item = self._scene.itemAt(currentPos, self.transform())
            if isinstance(item, PinItem):
                self.createConnectionRequest.emit((self._connectionDragStartPin.parentItem().id, self._connectionDragStartPin.id), (item.parentItem().id, item.id))
            self._scene.removeItem(self._connectionGhost)
            self._connectionDragging = False
            self._connectionDragStartPin = None
            event.accept()
        super().mouseReleaseEvent(event)
    
    def unselectAllItems(self, exceptionItems = []):
        for item in self._scene.items():
            if item not in exceptionItems:
                item.setSelected(False)

    def _createComponentGhosts(self, components: List[ComponentItem]):
        self._ghostComponents = {}
        for component in components:
            ghost = component.ghost()
            self._ghostComponents[ghost] = component
            self._scene.addItem(ghost)
    
    def _createConnectionGhost(self, start: QPointF, end: QPointF):
        self._connectionGhost = ConnectionItem.CubicPath(start = start, end=end).ghost()
        self._scene.addItem(self._connectionGhost)
    
    def _updateConnectionGhost(self, newEnd: QPointF):
        self._connectionGhost.end = newEnd
    
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