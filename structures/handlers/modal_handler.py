from enum import Enum
from typing import TYPE_CHECKING

import pygame
from pygame import Surface

import modules.utilities as u
from modules.constants import default_emulated_x
from modules.utilities import empty
from structures.hud.dynamic_button import DynamicButton
from structures.hud.hud_object import HudObject
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game


class ModalType(Enum):
    SIMPLE = 0,
    CUSTOM = 1,


class ModalHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.curr_modal = None
        self.regular_modal = u.load_scale('assets/modal2.png', factor=3.6)
        self.title_modal = u.load_scale('assets/title_modal2.png', factor=3.6)
        self.box_size = self.regular_modal.get_size()
        self.okay_surface = u.rescale(game.okay_surface, factor=0.5)
        self.button_offset = (round(self.okay_surface.get_width() / 2), round(self.okay_surface.get_height() / 2))
        self.modal_surface = Surface(
            (self.regular_modal.get_width(),
             self.regular_modal.get_height() + self.button_offset[1]),
            pygame.SRCALPHA
        )
        self.modal_object = HudObject(game, self.modal_surface)
        center_pos = u.center_blit_pos(game.screen, self.regular_modal)
        self.modal_object.rect.topleft = center_pos
        self.title = Text(game, size=28, color=(255, 255, 255), wrap=False, parent=self.modal_object)
        self.body = Text(game, size=18, color=(0, 0, 0), pos=(18, 100), wrap=True, parent=self.modal_object,
                         end_padding=18)
        ok_button_pos = u.relative_pos(self.regular_modal.get_size(), (-self.button_offset[0], self.button_offset[1]),
                                       from_xy="center-bottom")
        self.title_surface = Surface((self.box_size[0], 70), pygame.SRCALPHA)
        self.to_cancel = False
        self.okay_button = DynamicButton(
            game,
            size=self.okay_surface.get_size(),
            rect_template=u.rounded_rect_template(
                (255, 255, 255),
                emulated_x=default_emulated_x,
                double_bottom=True,
                outline=1,
                radius=8,
            ),
            text="OKAY!",
            text_options={"size": 20},
            pos=ok_button_pos,
            parent=self.modal_object,
        )

    def show_simple_modal(self, body: str, title=None, on_close=empty):
        self.curr_modal = {"body": body, "title": title, "on_close": on_close, "type": ModalType.SIMPLE}
        self.title.visible = title is not None
        self.title.text = title
        self.body.text = body
        if not title:
            self.body.rect.topleft = (20, 40)
        else:
            self.body.rect.topleft = (20, 90)
            self.title.text = title
            self.title.predraw()
            self.title.rect.topleft = u.center_blit_pos(self.title_surface, self.title.surface)
        self.game.input_handler.modal = self.modal_object
        self.modal_object.surface.blit(self.title_modal if title is not None else self.regular_modal, (0, 0))

    def show_custom_modal(self, hud_object: HudObject, on_close=empty):
        self.game.input_handler.modal = hud_object
        self.curr_modal = {
            "object": hud_object,
            "type": ModalType.CUSTOM,
            "on_close": on_close
        }

    def cancel_modal(self):
        self.to_cancel = True

    def modal_cleanup(self):
        self.curr_modal = None
        self.game.cursor_handler.cursor = "NORMAL"
        self.game.input_handler.modal = None
        self.game.just_ended_modal = True
        self.to_cancel = False

    def draw(self):
        if self.curr_modal and not self.game.loading_handler.is_transitioning:
            if self.curr_modal['type'] == ModalType.SIMPLE:
                if self.okay_button.on_press_end or self.game.input_handler.key_on_down.get(
                        pygame.K_RETURN) or self.to_cancel:
                    self.curr_modal['on_close']()
                    self.modal_cleanup()
                    return
                self.modal_object.draw()
            elif self.curr_modal['type'] == ModalType.CUSTOM:
                if self.to_cancel:
                    self.curr_modal['on_close']()
                    self.modal_cleanup()
                    return
                self.curr_modal['object'].draw()
