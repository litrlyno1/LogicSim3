from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import Qt, Signal, QPointF, QObject

from view.PinItem import PinItem
from viewmodel.CircuitComponentVM import CircuitComponentVM
from view.ComponentItem import ComponentItem

from typing import List

class CircuitComponentItem(ComponentItem):
    
    def __init__(self, id : str, pos : QPointF, inputPinIds : List[str], outputPinIds : List[str]):
        super().__init__(id = id, pos = pos)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable | # we don't set the flag selectable, because we implement our own logic
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        self.setAcceptedMouseButtons(Qt.LeftButton)
    
    @property
    def height(self):
        return self._rect.height()

    @property
    def width(self):
        return self._rect.width()
    
    def initPinItems(self, inputPinIds : List[str], outputPinIds : List[str]):
        self.initInputPins(inputPinIds)
        self.initOutputPins(outputPinIds)
    
    def initInputPins(self, inputPinIds : List[str]):
        self._numInputs = len(inputPinIds) 
        self._inputPins = list()
        
        for index in range(len(inputPinIds)):
            pinId = inputPinIds[index]
            pinRelativePos = QPointF(_inputPinRelX(self.width), CircuitComponentItem._inputPinRelY(index, self._numInputs, ))
            self._inputPins.append(PinItem(parentItem=self, id=pinId, relativePos=pinRelativePos))
    
    def initOutputPins(self, outputPinIds : List[str]):
        self._numOutputs = len(outputPinIds)
        self._outputPins = list()
        
        for index in range(len(outputPinIds)):
            pinId = outputPinIds[index]
            pinRelativePos = QPointF()
    
    
    
    def initOutputPins(self):
        self._outputPins = []
        for index in range(self._componentVM.component.numOutputs):
            self._outputPins.append(PinItem(parentComponent=self, type = "output", index = index))

    
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
    
    def _getRelPinX(self, pinType : str):
        if pinType == "output":
            return self.width/2
        else:
            return -width/2
    
    def _getPinY(self):
        if self._type == "output":
            pinAmount = self._parentComponent.componentVM.component.numOutputs
        else:
            pinAmount = self._parentComponent.componentVM.component.numInputs
        
        step = self.height / (pinAmount+1)
        y = (self._index+1)*step
        return y - self.height/2