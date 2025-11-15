import sys
from PySide6.QtWidgets import QApplication
from view.MainWindow import MainWindow
from viewmodel.command.CommandManager import CommandManager
from viewmodel.EventHandler import EventHandler
from viewmodel.CanvasVM import CanvasVM

def main():
    """
    Entry point for the circuit editor application.
    Sets up the QApplication, MainWindow, Canvas ViewModel, command manager, and event handler.
    """

    # Create the Qt application instance
    app = QApplication(sys.argv)

    # Initialize the ViewModel for the canvas
    # This manages the underlying data of components, circuits, and connections
    canvasVM = CanvasVM()
    
    # Create the main application window
    window = MainWindow()

    # Retrieve the canvas widget from the main window
    canvas = window.getCanvas()

    # Connect the canvas to its ViewModel
    # Ensures that UI updates reflect the underlying data model
    canvas.connectCanvasVM(canvasVM=canvasVM)

    # Create the command manager to handle undo/redo operations
    commandManager = CommandManager(canvasVM=canvasVM)

    # Create the event handler to listen to the canvas EventBus and dispatch commands
    # This allows user actions (e.g., drag/drop, toggle, add/remove components) to modify the ViewModel
    eventHandler = EventHandler(eventBus=window.getCanvas().eventBus, commandManager=commandManager)
    
    # Show the main application window
    window.show()

    # Start the Qt event loop
    sys.exit(app.exec())

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()