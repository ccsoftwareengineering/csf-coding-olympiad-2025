from typing import TYPE_CHECKING
import pygame
import modules.utilities as u
from modules.constants import default_emulated_x
from modules.more_utilities.guide_helpers import get_curr_guide_info

if TYPE_CHECKING:
    from structures.game import Game


class GuideHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.rect_template = u.rounded_rect_template((255, 255, 255), emulated_x=default_emulated_x, radius=8)
        self.dark_surface = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        self.dark_surface.set_colorkey((255, 255, 255))
        self.dark_surface.set_alpha(255//2)

    def draw(self):
        curr_guide_info = get_curr_guide_info(self.game)
        self.dark_surface.fill((0, 0, 0))
        self.dark_surface.blit(self.rect_template(curr_guide_info['rect'].size), curr_guide_info['rect'].topleft)
        self.game.screen.blit(self.dark_surface, (0, 0))
        # draws the mask and stuff and whatever... this isn't supposed to do dialogue it
        # just uses dialogue information to SHOW it over the main ui
        # if self.game.in_dialogue and self.game.dialogue_handler:
        #     pygame.display.set_gamma(1.0)
