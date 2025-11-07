from viewmodel.command.base import Command
from viewmodel.command.CommandFactory import CommandFactory

from viewmodel.CanvasVM import CanvasVM

class CommandManager:
    
    def __init__(self, canvasVM : CanvasVM):
        self.connectCanvasVM(canvasVM)
        self._executedStack = [] #stack of executed commands
        self._undoneStack = [] #stack of undone commands
        print("Command Manager initialized")
    
    def connectCanvasVM(self, canvasVM : CanvasVM):
        self._canvasVM = canvasVM
    
    def do(self, command: Command):
        if command: #if not None
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
        command = CommandFactory.createCommand(commandType, canvasVM = self._canvasVM, **kwargs)
        self.do(command)