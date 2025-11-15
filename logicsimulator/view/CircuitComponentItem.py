from typing import List, Dict
from PySide6.QtCore import QPointF, Signal, Qt

from logicsimulator.view.ComponentItem import ComponentItem
from logicsimulator.view.settings.CircuitComponentItem import CircuitComponentItemSettings
from logicsimulator.view.PinItem import InputPinItem, OutputPinItem

class CircuitComponentItem(ComponentItem):
    """Graphical representation of a circuit component with pins.

    This class extends ComponentItem to include input and output pins, their
    positions, and visual updates based on the component's logic value.
    It manages PinItems as children and provides helper methods to calculate
    their relative positions.
    """

    def __init__(self, id: str, type: str, pos: QPointF,
                 inputPinIds: List[str], outputPinIds: List[str],
                 value: bool,
                 settings: CircuitComponentItemSettings = CircuitComponentItemSettings.default()):
        """Initialize the circuit component item.

        Args:
            id (str): Unique ID of the component.
            type (str): Component type (e.g., 'AndGate', 'Switch').
            pos (QPointF): Initial position on the scene.
            inputPinIds (List[str]): List of input pin IDs.
            outputPinIds (List[str]): List of output pin IDs.
            value (bool): Initial logical value of the component.
            settings (CircuitComponentItemSettings, optional): Visual settings.
        """
        super().__init__(id=id, type=type, pos=pos, settings=settings)
        self._initPinItems(inputPinIds, outputPinIds)
        self._value = value

    def _initPinItems(self, inputPinIds: List[str], outputPinIds: List[str]):
        """Initialize all input and output pins."""
        self._initInputPins(inputPinIds)
        self._initOutputPins(outputPinIds)

    def _initInputPins(self, inputPinIds: List[str]):
        """Create and position all input pins.

        Args:
            inputPinIds (List[str]): List of input pin IDs.
        """
        self._numInputs = len(inputPinIds)
        self._inputPins: Dict[str, InputPinItem] = {}
        for index in range(self._numInputs):
            id = inputPinIds[index]
            relativePos = self.inputPinPos(self.width, self.height, index, self._numInputs)
            pinItem = InputPinItem(parentItem=self, id=id, relativePos=relativePos)
            self._inputPins[id] = pinItem

    def _initOutputPins(self, outputPinIds: List[str]):
        """Create and position all output pins.

        Args:
            outputPinIds (List[str]): List of output pin IDs.
        """
        self._numOutputs = len(outputPinIds)
        self._outputPins: Dict[str, OutputPinItem] = {}
        for index in range(self._numOutputs):
            id = outputPinIds[index]
            relativePos = self.outputPinPos(self.width, self.height, index, self._numOutputs)
            pinItem = OutputPinItem(parentItem=self, id=id, relativePos=relativePos)
            self._outputPins[id] = pinItem

    @property
    def value(self) -> bool:
        """bool: Current logical value of the component."""
        return self._value

    @value.setter
    def value(self, newValue: bool):
        """Update the component's value and refresh visuals.

        Args:
            newValue (bool): The new logical value.
        """
        self._value = newValue
        self.updateVisuals(newValue)
        self.update()

    def updateVisuals(self, newValue: bool):
        """Update the component's visual representation based on value.

        Args:
            newValue (bool): Logical value used to update appearance.

        Note:
            Implementation should update colors or other visual indicators.
        """
        pass

    @property
    def inputPinItems(self) -> Dict[str, InputPinItem]:
        """Dict[str, InputPinItem]: Dictionary of input pins keyed by ID."""
        return self._inputPins

    @property
    def outputPinItems(self) -> Dict[str, OutputPinItem]:
        """Dict[str, OutputPinItem]: Dictionary of output pins keyed by ID."""
        return self._outputPins

    @property
    def pinItems(self) -> Dict[str, InputPinItem | OutputPinItem]:
        """Dict[str, PinItem]: Combined dictionary of all pins (inputs and outputs)."""
        return self._inputPins | self._outputPins

    # -------------------- Pin position helpers --------------------

    def inputPinPos(self, width: float, height: float, index: int, pinNum: int) -> QPointF:
        """Compute the absolute position of an input pin.

        Args:
            width (float): Component width.
            height (float): Component height.
            index (int): Index of the pin.
            pinNum (int): Total number of input pins.

        Returns:
            QPointF: Pin position relative to component center.
        """
        return QPointF(self.inputRelX(width, index, pinNum), self.inputRelY(height, index, pinNum))

    def inputRelX(self, width: float, index: int, pinNum: int) -> float:
        """X-coordinate of input pin (always on left edge)."""
        return -width / 2

    def inputRelY(self, height: float, index: int, pinNum: int) -> float:
        """Y-coordinate of input pin, distributed evenly along height."""
        step = height / (pinNum + 1)
        y = (index + 1) * step
        return y - height / 2

    def outputPinPos(self, width: float, height: float, index: int, pinNum: int) -> QPointF:
        """Compute the absolute position of an output pin."""
        return QPointF(self.outputRelX(width, index, pinNum), self.outputRelY(height, index, pinNum))

    def outputRelX(self, width: float, index: int, pinNum: int) -> float:
        """X-coordinate of output pin (always on right edge)."""
        return width / 2

    def outputRelY(self, height: float, index: int, pinNum: int) -> float:
        """Y-coordinate of output pin, distributed evenly along height."""
        step = height / (pinNum + 1)
        y = (index + 1) * step
        return y - height / 2