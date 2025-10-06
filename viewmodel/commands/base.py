from abc import ABC, abstractmethod

class Command(ABC):
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class CommandManager:
    
    def __init__(self):
        self._executedStack = [] #stack of executed commands
        self._undoneStack = [] #stack of undone commands
    
    def do(self, command: Command):
        command.execute()
        self._executedStack.append(command)
        self._undoneStack.clear()

    def undo(self):
        if self._executedStack:
            cmd = self._executedStack.pop()
            cmd.undo()
            self._undoneStack.append(cmd)

    def redo(self):
        if self._undoneStack:
            cmd = self._undoneStack.pop()
            cmd.execute()
            self._executedStack.append(cmd)