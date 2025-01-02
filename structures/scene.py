from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from structures.game import Game
from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, game: 'Game'):
        self.game = game
        self.g_vars = self.define_game_variables()

    @abstractmethod
    def draw(self):
        pass

    def init(self):
        pass

    def cleanup(self):
        pass

    def define_game_variables(self):
        return {}
