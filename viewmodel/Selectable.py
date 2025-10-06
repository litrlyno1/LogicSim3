from PySide6.QtCore import Signal

class Selectable:
    selectedChanged = Signal(bool)
    
    def __init__(self, selected : bool = True):
        super().__init__()
        self._selected = selected
    
    def select(self) -> None:
        if self._selected == False:
            self._selected = True
            self.selectedChanged.emit(self)
    
    def unselect(self) -> None:
        if self._selected == True:
            self._selected == False
            self.selectedChanged.emit(self)
    
    def isSelected(self) -> bool:
        return self._selected