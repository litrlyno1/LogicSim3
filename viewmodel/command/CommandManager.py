from viewmodel.command.base import Command
from viewmodel.command.registry import CommandRegistry

from viewmodel.CanvasVM import CanvasVM

class CommandManager:
    
    def __init__(self, canvasVM : CanvasVM):
        self._executedStack = [] #stack of executed commands
        self._undoneStack = [] #stack of undone commands
        self._canvasVM = canvasVM
        print("Command Manager initialized")
    
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
    
    def createCommand(self, commandType : str, **kwargs):
        #print(**kwargs)
        command = CommandRegistry.getCommand(commandType)(canvasVM = self._canvasVM, **kwargs)
        print("Command created: ")
        #print(command.__dict__)
        self.do(command)