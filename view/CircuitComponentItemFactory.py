from view.CircuitComponentItem import CircuitComponentItem
from view.LogicGateItem import LogicGateItem
from view.BulbItem import BulbItem
from view.SwitchItem import SwitchItem

from PySide6.QtCore import QPointF

# Mapping of simple circuit components to their corresponding view classes
others = {
    "Bulb": BulbItem,
    "Switch": SwitchItem
}

# Supported logic gate types
logicGates = ("AndGate", "OrGate", "NotGate", "XorGate", "NandGate")

class CircuitComponentItemFactory:
    """Factory class to create visual circuit component items.

    This factory returns the appropriate QGraphics-based view object for
    a given circuit component type, including Bulbs, Switches, and logic gates.
    """

    @staticmethod
    def createCircuitComponentItem(id: str, type: str, pos: QPointF, inputPinIds: list, outputPinIds: list, value: bool):
        """Create a circuit component item for the canvas.

        Args:
            id (str): Unique identifier for the component instance.
            type (str): Component type (e.g., "Bulb", "Switch", "AndGate").
            pos (QPointF): Initial position of the component on the scene.
            inputPinIds (list): List of input pin IDs for the component.
            outputPinIds (list): List of output pin IDs for the component.
            value (bool): Initial logic value for the component (used for Bulbs and Switches).

        Returns:
            CircuitComponentItem: An instance of the appropriate visual component class.

        Notes:
            - For simple components like Bulbs and Switches, the `value` parameter is used.
            - For logic gates, the factory returns a LogicGateItem and ignores `value`.
        """
        if type in others:
            # Return specialized view class for Bulb or Switch
            return others[type](id, type, pos, inputPinIds, outputPinIds, value)
        elif type in logicGates:
            # Return a LogicGateItem for logic gate components
            return LogicGateItem(id, type, pos, inputPinIds, outputPinIds)