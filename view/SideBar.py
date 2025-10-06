from PySide6.QtWidgets import QWidget
from typing import List 

from view.settings.SideBarSettings import SideBarSettings


class SideBar(QWidget):
    
    def __init__(self, settings: SideBarSettings):
        super().__init()
    
    def addGateButtons(self, gates: List[str]):
        pass
        def addGateButton(self, gate : str):
            pass
    
    def 