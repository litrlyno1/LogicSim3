from typing import Protocol, List

class Observer(Protocol):
    def onChange(self) -> None:
        ...

class IObservable(Protocol):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.onChange()