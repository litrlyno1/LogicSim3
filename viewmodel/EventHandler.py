from view.EventBus import EventBus
from viewmodel.command.CommandManager import CommandManager

event_command_dict = {
    "ItemDropped" : "AddComponent", 
    "ItemsMoved" : "MoveComponents",
    "ConnectionCreated" : "CreateConnection"
}

class EventHandler:
    
    def __init__(self, eventBus : EventBus, commandManager : CommandManager):
        self._eventBus = eventBus
        self._commandManager = commandManager
        print("EventHandler initialized")
        
        for eventName in event_command_dict:
            self._eventBus.subscribe(eventName=eventName, handler = self._commandManager.createCommand(commandType= event_command_dict[eventName]))