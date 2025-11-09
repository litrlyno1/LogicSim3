from model.Bulb import Bulb
from model.Switch import Switch
from model.CircuitComponent import CircuitComponent
from model.Component import Component
from model.Gates import AndGate, OrGate, XorGate, NotGate
from model.Pin import Connection
from core.registry import ComponentRegistry

from viewmodel.CircuitComponentVM import CircuitComponentVM
from viewmodel.SwitchVM import SwitchVM
from viewmodel.ConnectionVM import ConnectionVM
from viewmodel.CanvasVM import CanvasVM
from viewmodel.command.CommandManager import CommandManager
from viewmodel.CanvasVM import CanvasVM

from PySide6.QtCore import QPointF

from model.ComponentFactory import ComponentFactory

from view.PinItem import InputPinItem, OutputPinItem
from view.LogicGateItem import LogicGateItem
from view.ConnectionItem import ConnectionItem

c1 = LogicGateItem(id = "1a", type = "AndGate", pos = QPointF(0 ,0), inputPinIds= ["in1", "in2"], outputPinIds= ["out1"])
c2 = LogicGateItem(id = "2a", type = "OrGate", pos = QPointF(1 ,0), inputPinIds= ["in3", "in4"], outputPinIds= ["out2"])
pin1 = c1._outputPins[0]
pin2 = c2._inputPins[1]

conn = ConnectionItem(id = "conn1", pinItem1=pin1, pinItem2=pin2)
print(conn.__dict__)