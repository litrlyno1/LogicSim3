from logicsimulator.view.LogicGateItem import LogicGateItem
from logicsimulator.view.CircuitComponentItem import CircuitComponentItem
from logicsimulator.view.ComponentItem import ComponentItem 
from logicsimulator.view.BulbItem import BulbItem
from logicsimulator.view.SwitchItem import SwitchItem

from PySide6.QtCore import QPointF

# Mapping of simple components to their respective view classes
view_vm = {
    "Bulb": BulbItem,
    "Switch": SwitchItem,
}

# List of logic gate component types
logicGateComponents = ("AndGate", "OrGate", "NotGate", "XorGate", "NandGate")

class ComponentItemFactory:
    """Factory class to create visual component items for the canvas.

    This factory returns the appropriate QGraphics-based view object
    for a given component type (Bulb, Switch, Logic Gate, or generic Component).
    """

    @staticmethod
    def createComponentItem(id: str, type: str, pos: QPointF):
        """Create a visual component item for the given ID and type.

        Args:
            id (str): Unique identifier for the component instance (used to infer type).
            type (str): Component type string (currently not used; type inferred from ID).
            pos (QPointF): Initial position of the component on the canvas.

        Returns:
            ComponentItem: An instance of the appropriate visual component class.
        """
        # Infer the component type from the ID prefix (e.g., "Switch_1" → "Switch")
        type = id.split('_', 1)[0]

        if type in view_vm:
            # Return specific view class for Bulb or Switch
            return view_vm[type](id)
        else:
            if type in logicGateComponents:
                # Return a LogicGateItem for logic gate components
                return LogicGateItem(id)
            else:
                # Return a generic ComponentItem for any other type
                return ComponentItem(id)