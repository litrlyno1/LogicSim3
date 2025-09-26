from LogicGate import LogicGate
from AndGate import AndGate
from LeverComponent import Lever

gate1 = AndGate()
lever1 = Lever()
print(lever1.getOutput())
lever1.switchValue()
print(lever1.getOutput())
lever2 = Lever()
lever2.switchValue()
gate1.setInputConnection(component = lever1, connectionIndex = 0)
gate1.setInputConnection(component = lever2, connectionIndex = 1)
print(gate1.getOutput())
print("####")
gate1.deleteInputConnection(connectionIndex= 1)
print(gate1.getOutput())