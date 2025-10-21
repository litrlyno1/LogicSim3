from view.EventBus import EventBus
from viewmodel.command.CommandManager import CommandManager

class EventHandler:
    
    def __init__(self, eventBus : EventBus, commandManager : CommandManager):
        self._eventBus = eventBus
        self._commandManager = commandManager
        print("EventHandler initialized")
        self._eventBus.subscribe(eventName= "ItemDropped", 
                                handler = lambda componentType, pos: self._commandManager.createCommand(commandType="AddComponent", componentType = componentType, pos = pos))
        self._eventBus.subscribe(eventName = "ItemMoved",
                                handler = lambda component, pos: self._commandManager.createCommand(commandType = "MoveComponent", component = component, oldPos = component.pos, newPos = pos))
        self._eventBus.subscribe(eventName= "ConnectionCreated",
                                handler = lambda gate1, type1, index1, gate2, type2, index2: self._commandManager.createCommand(commandType= "CreateConnection", gate1 = gate1, type1 = type1, index1 = index1, gate2 = gate2, type2 = type2, index2 = index2))