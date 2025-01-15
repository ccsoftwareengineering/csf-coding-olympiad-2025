from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from structures.game import Game


class DisasterHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.hurricane = game.asset_handler(1)['assets/hurricane.png']
        self.animating = False

    def initialize_hurricane(self):
        pass

    def draw(self):
        pass

