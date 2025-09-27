from Component import Component

class Lever(Component):
    
    def __init__(self):
        super().__init__()
        self._value = False
    
    def switchValue(self):
        if self._value == False:
            self._value = True
        else:
            self._value = False
    
    def getOutput(self):
        return self._value