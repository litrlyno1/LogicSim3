from view.EventBus import EventBus
from viewmodel.command.CommandManager import CommandManager

events = ("AddComponents", "MoveComponents", "RemoveComponents", "CreateConnection", "RemoveConnections")

class EventHandler:
    
    def __init__(self, eventBus : EventBus, commandManager : CommandManager):
        self._eventBus = eventBus
        self._commandManager = commandManager
        print("EventHandler initialized")
        
        for eventName in events:
            self._eventBus.subscribe(eventName, lambda eventName, **kwargs: self._commandManager.createCommand(commandType=eventName, **kwargs))