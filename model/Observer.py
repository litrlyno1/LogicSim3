from typing import Protocol, List

class IObservable(Protocol):
    def onChange(self) -> None:
        self.notify()

class Observer(Protocol):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
            self.notify()

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
            self.notify()

    def notify(self):
        for observer in self._observers:
            observer.onChange()