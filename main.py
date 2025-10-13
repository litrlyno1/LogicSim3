import sys
from PySide6.QtWidgets import QApplication
from view.MainWindow import MainWindow
from viewmodel.command.CommandManager import CommandManager
from viewmodel.EventHandler import EventHandler
from viewmodel.CanvasVM import CanvasVM

from core.registry import GateRegistry

def main():
    app = QApplication(sys.argv)
    canvasVM = CanvasVM()
    
    window = MainWindow()
    canvas = window.getCanvas()
    canvas.connectCanvasVM(canvasVM=canvasVM)

    commandManager = CommandManager(canvasVM = canvasVM)
    eventHandler = EventHandler(eventBus= window.getCanvas().getEventBus(), commandManager = commandManager)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()