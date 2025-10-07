import sys
from PySide6.QtWidgets import QApplication
from view.MainWindow import MainWindow

from core.registry import GateRegistry

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    reg = GateRegistry()
    print(reg.getAllGates())
    sys.exit(app.exec())

if __name__ == "__main__":
    main()