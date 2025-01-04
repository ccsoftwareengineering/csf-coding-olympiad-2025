from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from structures.game import Game


class GuideHandler:
    def __init__(self, game: 'Game'):
        self.game = game

    def draw(self):
        # draws the mask and stuff and whatever... this isn't supposed to do dialogue it
        # just uses dialogue information to SHOW it over the main ui
        pass
