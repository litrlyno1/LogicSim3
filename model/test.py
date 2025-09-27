from Gates import AndGate, OrGate, NotGate, BulbGate
from SwitchComponent import Switch

switch1 = Switch()

switch1.toggle()
print(switch1.getOutput())
switch1.toggle()
print(switch1.getOutput())