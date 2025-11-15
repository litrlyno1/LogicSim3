from logicsimulator.view.settings.CircuitComponentItem import CircuitComponentItemSettings

class LogicGateItemSettings(CircuitComponentItemSettings):
    
    def __init__(self,
                size,
                fontSize,
                textColor,
                color,
                selectedColor,
                borderColor,
                borderWidth):

        super().__init__(size,
                fontSize,
                textColor,
                color,
                selectedColor,
                borderColor,
                borderWidth)
    
    @classmethod
    def default(cls):
        return CircuitComponentItemSettings.default()