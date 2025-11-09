from typing import List, Dict
from PySide6.QtCore import QPointF, Signal

from view.ComponentItem import ComponentItem
from view.settings.CircuitComponentItem import CircuitComponentItemSettings
from view.PinItem import InputPinItem, OutputPinItem

class CircuitComponentItem(ComponentItem):
    pinSelected = Signal(str, bool)

    def __init__(self, id : str, type : str, pos : QPointF, inputPinIds : List[str], outputPinIds : List[str], settings: CircuitComponentItemSettings = CircuitComponentItemSettings.default()):
        super().__init__(id, type, pos, settings)
        print(f"Initializing CircuitComponentItem with {self.width} width and {self.height} height")
        self._initPinItems(inputPinIds, outputPinIds)
    
    def _initPinItems(self, inputPinIds : List[str], outputPinIds : List[str]):
        self._initInputPins(inputPinIds)
        self._initOutputPins(outputPinIds)
    
    def _initInputPins(self, inputPinIds : List[str]):
        self._numInputs = len(inputPinIds) 
        self._inputPins : Dict[str, InputPinItem] = {}
        for index in range(self._numInputs):
            id = inputPinIds[index]
            relativePos = self.inputPinPos(self.width, self.height, index, self._numInputs)
            pinItem = InputPinItem(parentItem=self, id=id, relativePos=relativePos)
            self._inputPins[inputPinIds[index]] = pinItem
    
    def _initOutputPins(self, outputPinIds : List[str]):
        self._numOutputs = len(outputPinIds)
        self._outputPins : Dict[str, OutputPinItem] = {}
        for index in range(self._numOutputs):
            id = outputPinIds[index]
            relativePos = self.outputPinPos(self.width, self.height, index, self._numOutputs)
            pinItem = OutputPinItem(parentItem=self, id=id, relativePos=relativePos)
            self._outputPins[outputPinIds[index]] = pinItem
    
    @property
    def inputPinItems(self):
        return self._inputPins
    
    @property
    def outputPinItems(self):
        return self._outputPins

    def inputPinPos(self, width: float, height: float, index: int, pinNum: int):
        return QPointF(self.inputRelX(width, index, pinNum), self.inputRelY(height, index, pinNum))
    
    def inputRelX(self, width: float, index : int, pinNum : int) -> float:
        return -width/2
    
    def inputRelY(self, height: float, index: int, pinNum : int) -> float:
        step = height / (pinNum+1)
        y = (index+1)*step
        return y - height/2
    
    def outputPinPos(self, width: float, height: float, index: int, pinNum: int):
        return QPointF(self.outputRelX(width, index, pinNum), self.outputRelY(height, index, pinNum))
    
    def outputRelX(self, width: float, index : int, pinNum : int) -> float:
        return width/2
    
    def outputRelY(self, height: float, index : int, pinNum: int) -> float:
        step = height / (pinNum+1)
        y = (index+1)*step
        return y - height/2