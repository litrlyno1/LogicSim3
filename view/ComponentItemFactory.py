from view.CircuitComponentItem import CircuitComponentItem
from view.ComponentItem import ComponentItem 
from view.BulbItem import BulbItem
from view.SwitchItem import SwitchItem

view_vm = {
    "Bulb" : BulbItem,
    "Switch" : SwitchItem,
}

circuitComponents = set("AndGate", "OrGate", "NotGate", "XorGate", "NandGate")

class ComponentItemFactory:
    
    @classmethod
    def createComponentItem(id : str):
        type = id.split('_', 1)[0]
        if type in view_vm:
            return view_vm[type](id)
        else:
            if type in circuitComponents:
                return CircuitComponentItem(id)
            else:
                return ComponentItem(id)