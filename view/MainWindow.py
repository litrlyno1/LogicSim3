from PySide6.QtWidgets import QWidget
from view.settings.MainWindow import MainWindowSettings
from view.Canvas import Canvas

class MainWindow(QWidget):
    
    def __init__(self, settings : MainWindowSettings, centralWidget : QWidget):
        super().__init__()
        self.setWindowTitle(settings.TITLE)
        self.setLayout(settings.LAYOUT)
        self.resize(settings.RESOLUTION)
    
    @classmethod
    def create(cls, settings : MainWindowSettings, centralWidget = Canvas):
        return cls(settings)
    
    @classmethod
    def createDefault(cls):
        return cls(MainWindowSettings.getDefault())
