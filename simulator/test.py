from LogicGate import LogicGate
from AndGate import AndGate
from OrGate import OrGate
from NotGate import NotGate
from BulbGate import BulbGate
from LeverComponent import Lever

lever1 = Lever()
lever2 = Lever()
lever3 = Lever()
lever4 = Lever()
gate1 = OrGate()
gate2 = OrGate()
gate3 = AndGate()
gate4 = NotGate()
gate5 = BulbGate()
gate1.setInputConnection(component = lever1, connectionIndex = 0)
gate1.setInputConnection(component = lever2, connectionIndex = 1)
gate2.setInputConnection(component = lever3, connectionIndex = 0)
gate2.setInputConnection(component = lever4, connectionIndex = 1)
gate3.setInputConnection(component = gate1, connectionIndex=0)
gate3.setInputConnection(component= gate2, connectionIndex=1)
lever1.switchValue()
lever3.switchValue()
gate5.setInputConnection(component = gate3, connectionIndex=0)
print(gate5.getOutput())