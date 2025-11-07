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

p = QPointF(0, 0)
p1 = QPointF(1, 0)
p2 = QPointF(3,3)

can = CanvasVM()
cmd = CommandManager(can)

#cmd.createCommand(commandType= "AddComponent", componentType = "Switch", pos = p)
#cmd.createCommand(commandType= "AddComponent", componentType = "Switch", pos = p1)
#cmd.createCommand(commandType= "AddComponent", componentType = "AndGate", pos = p2)
#cmd.createCommand(commandType= "AddComponent", componentType = "Bulb", pos = p)

switch1 = SwitchVM(ComponentFactory.createComponent("Switch"), p)
switch2 = SwitchVM(ComponentFactory.createComponent("Switch"), p)
andGate = CircuitComponentVM(ComponentFactory.createComponent("AndGate"), p)
bulb = CircuitComponentVM(ComponentFactory.createComponent("Bulb"), p)

can.addComponent(switch1)
can.addComponent(switch2)
can.addComponent(andGate)
can.addComponent(bulb)

switch1.toggle()
switch2.toggle()

cmd.createCommand(commandType="CreateConnection", pinVM1 = switch1.outputPins[0], pinVM2 = andGate.inputPins[0])
cmd.createCommand(commandType="CreateConnection", pinVM1 = switch2.outputPins[0], pinVM2 = andGate.inputPins[1])
cmd.createCommand(commandType="CreateConnection", pinVM1 = andGate.outputPins[0], pinVM2 = bulb.inputPins[0])
cmd.undo()
cmd.redo()
cmd.undo()
cmd.undo()
cmd.undo()

'''

conn1 = ConnectionVM(switch1.outputPins[0], andGate.inputPins[0])
conn2 = ConnectionVM(switch1.outputPins[0], andGate.inputPins[1])
conn3 = ConnectionVM(bulb.inputPins[0], andGate.outputPins[0])

can.addConnection(conn1)
can.addConnection(conn2)
can.addConnection(conn3)

switch1.toggle()
switch2.toggle()

print("****")

cmd.createCommand(commandType="RemoveConnections", connectionIds = [conn1.id])
cmd.createCommand(commandType="CreateConnection", pinVM1 = switch1.outputPins[0], pinVM2 = andGate.inputPins[0])
cmd.createCommand(commandType="RemoveComponents", componentIds = [andGate.id])

print("****")
print(f"Values : {switch1._propagatorRelay._propagatorObserver.propagator.value, switch2._propagatorRelay._propagatorObserver.propagator.value}")
#print(f"Values : {andGate._propagatorRelay._propagatorObserver.propagator.value}")
print(f"Values : {bulb._propagatorRelay._propagatorObserver.propagator.value}")

print("****")
print(f"Values : {switch1._propagatorRelay._propagatorObserver.propagator.value, switch2._propagatorRelay._propagatorObserver.propagator.value}")
#print(f"Values : {andGate._propagatorRelay._propagatorObserver.propagator.value}")
print(f"Values : {bulb._propagatorRelay._propagatorObserver.propagator.value}")
'''

'''
class_attrs = {k: v for k, v in bulb.__class__.__dict__.items() if not callable(v) and not k.startswith('__')}
print("Class attributes:")
for name, value in class_attrs.items():
    print(f"{name} = {value}")

instance_attrs = bulb.__dict__
print("\nInstance attributes:")
for name, value in instance_attrs.items():
    print(f"{name} = {value}")
'''