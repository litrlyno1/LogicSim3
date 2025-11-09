from view.CircuitComponentItem import CircuitComponentItem
from view.LogicGateItem import LogicGateItem
from view.BulbItem import BulbItem
from view.SwitchItem import SwitchItem

from PySide6.QtCore import QPointF

others = {
    "Bulb": BulbItem,
    "Switch": SwitchItem
}

logicGates = ("AndGate", "OrGate", "NotGate", "XorGate", "NandGate")

class CircuitComponentItemFactory:
    
    @staticmethod
    def createCircuitComponentItem(id: str, type: str, pos: QPointF, inputPinIds: list, outputPinIds: list):
        if type in others:
            return others[type](id, type, pos, inputPinIds, outputPinIds)
        elif type in logicGates:
            return LogicGateItem(id, type, pos, inputPinIds, outputPinIds)