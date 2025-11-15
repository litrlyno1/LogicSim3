from viewmodel.command.Commands import *

commandRegistry = {
    "AddComponents" : AddComponents,
    "MoveComponents" : MoveComponents, 
    "CreateConnection" : CreateConnection,
    "RemoveComponents" : RemoveComponents,
    "RemoveConnections" : RemoveConnections,
    "ToggleComponent":  ToggleComponent
}

class CommandFactory:
    
    @staticmethod
    def createCommand(type : str, **kwargs):
        if type in commandRegistry:
            return commandRegistry[type](**kwargs)
        else:
            return None