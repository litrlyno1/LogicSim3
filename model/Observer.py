from typing import Protocol, List

class Observer(Protocol):
    def onChange(self) -> None:
        ...

class SignalPropagator:
    #singleton
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SignalPropagator, cls).__new__(cls)
            cls._instance._observers: List[Observer] = []
        return cls._instance
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def propagate(self):
        # copy of observers list for consistency
        for observer in list(self._observers):
            observer.onChange()