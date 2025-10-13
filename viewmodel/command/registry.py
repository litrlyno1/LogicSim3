import inspect
import importlib

class CommandRegistry:
    _registry = {}

    @classmethod
    def _loadCommands(cls, module_name = "viewmodel.command.Commands"):
        if not cls._registry:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module_name:
                    cls._registry[name] = obj
        print(f"COMMAND REGISTRY: {cls._registry}")
        return cls._registry

    @classmethod
    def getAllCommands(cls):
        return list(cls._loadCommands().keys())
    
    @classmethod
    def getCommand(cls, name: str):
        return cls._loadCommands()[name]