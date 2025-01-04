from enum import Enum
from typing import TYPE_CHECKING, Optional

import pygame

import modules.more_utilities.easings as easings
import modules.utilities as u

if TYPE_CHECKING:
    from structures.game import Game


class LoadingHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.loading_screen = game.panels
        self.transition_state_to: Optional[Enum] = None
        self.transition_progress = 0
        self.direction = 1
        self.loading_surface = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        self.loading_surface.fill((255, 255, 255))
        self.title = u.rescale(game.title, factor=1)
        self.transition_length = 70
        # self.easing_function = lambda x: easings.stepwise(x, 10)
        self.easing_function = easings.ease_in_out
        self.is_transitioning = False

    def transition_to(self, state: Enum):
        if self.transition_state_to is not None:
            return
        self.game.cursor_handler.cursor = 'NORMAL'
        self.transition_state_to = state
        self.transition_progress = 0
        self.is_transitioning = True

    def draw(self):
        if self.transition_state_to is not None and not self.game.input_handler.modal:
            if self.transition_progress == self.transition_length:
                self.direction = -1
                self.game.set_state(self.transition_state_to)
            elif self.transition_progress == 0 and self.direction == -1:
                self.transition_state_to = None
                self.direction = 1
                self.is_transitioning = False
                return
            self.loading_surface.fill((255, 255, 255))
            range360 = self.easing_function(self.transition_progress / self.transition_length) * (
                        self.direction == -1 and 360 * 2 or 360)
            range255 = self.easing_function(self.transition_progress / self.transition_length) * 255
            u.center_blit(self.loading_surface,
                          pygame.transform.rotate(self.title, range360))
            self.loading_surface.set_alpha(round(range255))
            self.game.screen.blit(self.loading_surface, (0, 0))
            self.transition_progress += self.direction
