from view.LogicGateItem import LogicGateItem
from view.CircuitComponentItem import CircuitComponentItem
from view.ComponentItem import ComponentItem 
from view.BulbItem import BulbItem
from view.SwitchItem import SwitchItem

from PySide6.QtCore import QPointF

view_vm = {
    "Bulb" : BulbItem,
    "Switch" : SwitchItem,
}

logicGateComponents = ("AndGate", "OrGate", "NotGate", "XorGate", "NandGate")

class ComponentItemFactory:
    
    @staticmethod
    def createComponentItem(id : str, type: str, pos: QPointF):
        type = id.split('_', 1)[0]
        if type in view_vm:
            return view_vm[type](id)
        else:
            if type in logicGateComponents:
                return LogicGateItem(id)
            else:
                return ComponentItem(id)