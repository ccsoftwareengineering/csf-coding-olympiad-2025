from typing import TYPE_CHECKING

import pygame
from pygame import Surface

import modules.utilities as u
from modules.utilities import empty
from structures.hud.button import Button
from structures.hud.hud_object import HudObject
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game


class ModalHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.curr_modal = None
        self.regular_modal = game.modal
        self.title_modal = game.title_modal
        self.box_height = self.regular_modal.get_height()
        self.okay_surface = u.rescale(game.okay_surface, factor=0.5)
        self.button_offset = round(self.okay_surface.get_height() / 2)
        self.modal_surface = Surface(
            (self.regular_modal.get_width(),
             self.regular_modal.get_height() + self.button_offset),
            pygame.SRCALPHA
        )
        self.modal_object = HudObject(game, self.modal_surface)
        self.modal_object.rect.center = u.center_blit_pos(game.screen, self.modal_surface,
                                                          offsets=(0, -self.button_offset))
        self.title = Text(game, size=32, color=(255, 255, 255), wrap=False, parent=self.modal_object)
        self.body = Text(game, size=24, color=(0, 0, 0), pos=(20, 100), wrap=False, parent=self.modal_object)
        self.okay_button = Button(
            game,
            self.okay_surface,
            u.relative_pos(self.regular_modal.get_size(), (0, 0), from_xy="center-bottom"),
            parent=self.modal_object,
        )

    def show_modal(self, body: str, title=None, on_close=empty):
        self.curr_modal = {"body": body, "title": title, "on_close": on_close}
        self.title.visible = title is not None
        self.title.text = title
        self.body.text = body
        self.modal_object.surface.blit(self.title_modal if title is not None else self.regular_modal, (0, 0))

    def draw(self):
        if self.okay_button.on_press_end:
            self.curr_modal = None
            self.game.cursor_handler.cursor = "NORMAL"
        if self.curr_modal and not self.game.loading_handler.is_transitioning:
            self.game.telemetry_handler.set_values({
                'modal_object_pos': self.modal_object.rect.center
            })
            self.modal_object.draw()


