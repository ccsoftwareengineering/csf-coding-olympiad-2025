from typing import Callable

import modules.utilities as u
from structures.event_emitter import EventEmitter
from structures.store import Store


class Observable(EventEmitter):
    def __init__(self, handler: 'ObservableHandler', value):
        super().__init__()
        self.handler = handler
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            old = self._value
            self._value = value
            self.handler.emit('change', self)
            self.emit('change', value, old)

    def __eq__(self, other):
        return self.value == other.value


class Computed:
    def __init__(self, observable: 'Observable', mapper: Callable):
        self.id = u.random_string()
        self.observable = observable
        self.value = mapper(observable.value)
        self.map = mapper
        observable.on('change', self.changing, self.id)

    def changing(self, value):
        self.value = self.map(value)

    def __del__(self):
        self.observable.off('change', self.id)


class ObservableHandler(EventEmitter):
    def __init__(self):
        super().__init__()
        self.observables = Store()

    def __getitem__(self, observable_name) -> 'Observable':
        obs = self.observables[observable_name]
        if not obs:
            obs = Observable(self, observable_name)
            self.observables[observable_name] = obs
        return obs

    def __setitem__(self, key, value):
        if not self.observables.has(key):
            self.observables[key] = Observable(self, key)
        self.observables[key].value = value

    def __delitem__(self, key):
        del self.observables[key]
