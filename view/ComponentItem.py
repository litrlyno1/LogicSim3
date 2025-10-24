from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import Qt, Signal, QPointF, QObject

from view.PinItem import PinItem
from viewmodel import ComponentVM

class ComponentSignals(QObject):
    moved = Signal(object, QPointF)

class ComponentItem(QGraphicsItem):
    
    def __init__(self, componentVM : ComponentVM):
        super().__init__()
        self._signals = ComponentSignals()
        self._componentVM = componentVM
        self.setPos(self._componentVM.pos)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable | # we don't set the flag selectable, because we implement our own logic
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        self.setAcceptedMouseButtons(Qt.LeftButton)
    
    @property
    def componentVM(self):
        return self._componentVM

    @property
    def signals(self):
        return self._signals
    
    def getHeight(self):
        return self._rect.height()

    def getWidth(self):
        return self._rect.width()
    
    def initPinItems(self):
        self.initInputPins()
        self.initOutputPins()
    
    def initInputPins(self):
        self._inputPins = []
        for index in range(self._componentVM.component.getNumInputs()):
            self._inputPins.append(PinItem(parentComponent=self, type = "input", index = index))
        
    def initOutputPins(self):
        self._outputPins = []
        for index in range(self._componentVM.component.getNumOutputs()):
            self._outputPins.append(PinItem(parentComponent=self, type = "output", index = index))
    
    def getInputPins(self):
        return self._inputPins
    
    def getOutputPins(self):
        return self._outputPins
    
    def getInputPin(self, index : int):
        return self._inputPins[index]
    
    def getOutputPin(self, index : int):
        return self._outputPins[index]
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            print(f"Component selection : {value}")
            self._brush = self._selectedColor if value else self._color
            for pin in self._inputPins + self._outputPins:
                pin.isParentSelected = value
            self.update()
        elif change == QGraphicsItem.ItemPositionChange:
            self._signals.moved.emit(self, self.pos())
        return super().itemChange(change, value)

    def onItemMoved(self):
        for pin in self._inputPins:
            pin.onParentMoved()
        for pin in self._outputPins:
            pin.onParentMoved()