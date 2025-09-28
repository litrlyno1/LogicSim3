from Switch import Switch
from Gates import AndGate
from Pin import ConnectionFactory

switch1 = Switch()
switch2 = Switch()
gate1 = AndGate()
ConnectionFactory.connect(switch1.getOutputPin(0), gate1.getInputPin(0))
print("###")
ConnectionFactory.connect(switch2.getOutputPin(0), gate1.getInputPin(1))
print("###")
switch1.toggle()