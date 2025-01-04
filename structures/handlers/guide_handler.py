from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from structures.game import Game


class GuideHandler:
    def __init__(self, game: 'Game'):
        self.game = game

    def draw(self):
        pass
        # draws the mask and stuff and whatever... this isn't supposed to do dialogue it
        # just uses dialogue information to SHOW it over the main ui
        # if self.game.in_dialogue and self.game.dialogue_handler:
        #     pygame.display.set_gamma(1.0)
