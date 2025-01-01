from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from structures.game import Game


class ModalHandler:
    def __init__(self, game: 'Game'):
        self.game = game

    def draw(self):
        pass
