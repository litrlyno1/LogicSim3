from viewmodel import ComponentVM

class ComponentItem:
    
    def __init__(self, componentVM : ComponentVM):
        self._componentVM = componentVM
    
    @property
    def componentVM(self):
        return self._componentVM