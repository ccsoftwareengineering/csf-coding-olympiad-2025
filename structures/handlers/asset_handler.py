from functools import singledispatchmethod
from typing import TYPE_CHECKING, cast, Tuple

from pygame import Surface

if TYPE_CHECKING:
    from structures.game import Game

import modules.utilities as u


# this class is going to do some GNARLY stuff
class AssetHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.dict: dict[any, Surface] = {}
        self.scale = 1
        self.prefix = ''

    def __call__(self, scale=1, prefix=''):
        self.scale = scale
        self.prefix = prefix
        return self

    def update(self, *args, **kwargs):
        self.__call__(*args, **kwargs)

    def __getitem__(self, item: str) -> Surface:
        a = (item, self.scale)
        cache = self.dict.get(a)
        result = cache or u.load_scale(self.prefix + item, factor=self.scale)
        self.dict[a] = result
        self.scale = 1
        return cast(Surface, result)

    def load_reset(self, path):
        scale = self.scale
        prefix = self.prefix
        a = self.__getitem__(path)
        self.scale = scale
        self.prefix = prefix
        return a

    @singledispatchmethod
    def load(self, path):
        raise TypeError('Path should be a string or tuple of strings')

    @load.register
    def _(self, path: str) -> Surface:
        return self.__getitem__(path)

    @load.register
    def _(self, path: tuple) -> tuple[Surface, ...]:
        a = tuple(self.load_reset(path) for path in path)
        self.prefix = ''
        self.scale = 1
        return a
