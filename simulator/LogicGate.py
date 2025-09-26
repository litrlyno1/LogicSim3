from abc import abstractmethod
from Component import Component

class LogicGate(Component):
    
    def __init__(self, numInputs : int):
        self._numInputs = numInputs
        self._inputConnections = [None]*numInputs
    
    def _getInputValues(self):
        inputValues = []
        for input in self._inputConnections:
            if input == None:
                inputValues.append(False)
            else:
                inputValues.append(input.getOutput())
        return inputValues
    
    def setInputConnection(self, component: Component, connectionIndex: int):
        if (connectionIndex < 0) or (connectionIndex >= self._numInputs):
            raise IndexError(f"Connection index out of range. Expected value within [0, {self._numInputs-1}], got {connectionIndex}")
        
        if component == None or not isinstance(component, Component):
            raise TypeError(f"Connected object must be a component. Except got {type(component)}.")
        
        component.attach(self)
        self._inputConnections[connectionIndex] = component
    
    def deleteInputConnection(self, connectionIndex: int):
        if (connectionIndex < 0) or (connectionIndex >= self._numInputs):
            raise IndexError(f"Connection index out of range. Index: {connectionIndex} not within interval [0, {self._numInputs-1}]")

        self._inputConnections[connectionIndex].detach(self)
        self._inputConnections[connectionIndex] = None
    
    def onChange(self):
        self.notify()