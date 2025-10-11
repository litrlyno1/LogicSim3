from view.EventBus import EventBus
from viewmodel.command.CommandManager import CommandManager

class EventHandler:
    
    def __init__(self, eventBus : EventBus, commandManager : CommandManager):
        self._eventBus = eventBus
        self._commandManager = commandManager
        print("EventHandler initialized")
        self._eventBus.subscribe(eventName= "ItemDropped", 
                                handler = lambda gateType, pos: self._commandManager.createCommand(commandType="AddGate", gateType = gateType, pos = pos))
        self._eventBus.subscribe(eventName = "ItemMoved",
                                handler = lambda gate, pos: self._commandManager.createCommand(commandType = "MoveGate", gate = gate, oldPos = gate.getPos(), newPos = pos))