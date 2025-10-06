from PySide6.QtCore import Signal

class Deletable:
    deleted = Signal()
    
    def delete(self) -> None:
        self.deleted.emit()