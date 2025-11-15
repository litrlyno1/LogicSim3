from logicsimulator.view.EventBus import EventBus
from logicsimulator.viewmodel.command.CommandManager import CommandManager

metaEvents = ("Undo", "Redo")
events = (
    "AddComponents",
    "MoveComponents",
    "RemoveComponents",
    "CreateConnection",
    "RemoveConnections",
    "ToggleComponent"
)

class EventHandler:
    """Handles application events by subscribing to the EventBus and
    forwarding them to the CommandManager.

    The ``EventHandler`` bridges the UI event system with the command
    pattern implementation. Standard component events (add, move,
    remove, connect, toggle) are translated into commands that can
    be undone/redone. Meta-events like "Undo" and "Redo" trigger
    the corresponding command manager actions.
    """

    def __init__(self, eventBus: EventBus, commandManager: CommandManager):
        """Initialize the event handler and subscribe to events.

        Args:
            eventBus (EventBus): The event bus that emits application events.
            commandManager (CommandManager): The manager that handles creating,
                undoing, and redoing commands.
        """
        self._eventBus = eventBus
        self._commandManager = commandManager

        # Subscribe standard events to create commands
        for eventName in events:
            self._eventBus.subscribe(
                eventName,
                lambda eventName, **kwargs: self._commandManager.createCommand(
                    commandType=eventName, **kwargs
                ),
            )

        # Subscribe meta-events for undo/redo
        self._eventBus.subscribe(eventName="Undo", handler=lambda eventName: self._commandManager.undo())
        self._eventBus.subscribe(eventName="Redo", handler=lambda eventName: self._commandManager.redo())