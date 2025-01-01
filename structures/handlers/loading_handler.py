from typing import TYPE_CHECKING

import pygame

import modules.utilities as u
from modules.more_utilities.easing import ease_in_out_circ

if TYPE_CHECKING:
    from structures.game import Game


class LoadingHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.loading_screen = game.panels
        self.transition_state_to = None
        self.transition_progress = 0
        self.direction = 1
        self.loading_surface = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        self.loading_surface.fill((255, 255, 255))
        self.title = u.rescale(game.title, factor=1)
        self.transition_length = 70

    def transition_to(self, state):
        if self.transition_state_to is not None:
            return
        self.transition_state_to = state
        self.transition_progress = 0

    def draw(self):
        if self.transition_state_to is not None and not self.game.input_handler.modal:
            if self.transition_progress == self.transition_length:
                self.direction = -1
                self.game.set_state(self.transition_state_to)
            elif self.transition_progress == 0 and self.direction == -1:
                self.transition_state_to = None
                self.direction = 1
                return
            self.loading_surface.fill((255, 255, 255))
            range360 = ease_in_out_circ(self.transition_progress / self.transition_length) * 360
            range255 = ease_in_out_circ(self.transition_progress / self.transition_length) * 255
            u.center_blit(self.loading_surface,
                          pygame.transform.rotate(self.title, range360))
            self.loading_surface.set_alpha(round(range255))
            self.game.screen.blit(self.loading_surface, (0, 0))
            self.transition_progress += self.direction
