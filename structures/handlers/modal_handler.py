from enum import Enum
from typing import TYPE_CHECKING, Optional, TypedDict, NotRequired, Callable

import pygame
from pygame import Surface

import modules.utilities as u
from modules.constants import default_emulated_x, ui_color, white, black
from modules.utilities import empty
from structures.hud.dynamic_button import DynamicButton
from structures.hud.hud_object import HudObject
from structures.hud.input_box import InputBox
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game


class ModalType(Enum):
    SIMPLE = 0,
    CUSTOM = 1,
    MULTI_SIMPLE = 2,


class MultiModalData(TypedDict):
    body: str
    title: NotRequired[str]
    input_visible: NotRequired[bool]
    after: Callable


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
        self.gap = 18
        self.modal_object = HudObject(game, self.modal_surface)
        self.input_box = InputBox(
            game,
            (self.box_size[0] - self.gap * 2, 40),
            (131, 177, 236),
            ui_color,
            white,
            black,
            text_size=18,
            override_y=True,
            parent=self.modal_object)
        self.input_box.visible = False
        center_pos = u.center_blit_pos(game.screen, self.regular_modal)
        self.modal_object.rect.topleft = center_pos
        self.title = Text(game, size=28, color=(255, 255, 255), wrap=False, parent=self.modal_object)
        self.body = Text(game, size=self.gap, color=(0, 0, 0), pos=(self.gap, 100), wrap=True, parent=self.modal_object,
                         end_padding=self.gap)
        ok_button_pos = u.relative_pos(self.regular_modal.get_size(), (-self.button_offset[0], self.button_offset[1]),
                                       from_xy='center-bottom')
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
            text='OKAY!',
            text_options={'size': 20},
            pos=ok_button_pos,
            parent=self.modal_object,
        )
        self.input_gap = 20

    def setup_simple_modal(self, body: str, title: Optional[str] = None, input_visible: Optional[bool] = False):
        self.title.visible = title is not None
        self.title.text = title
        self.body.text = body
        if input_visible:
            self.input_box.visible = True
        if not title:
            self.body.rect.topleft = (self.gap, 40)
        else:
            self.body.rect.topleft = (self.gap, 90)
            self.title.text = title
            self.title.predraw()
            self.title.rect.topleft = u.center_blit_pos(self.title_surface, self.title.surface)
        self.game.input_handler.modal = self.modal_object
        self.modal_object.surface.blit(self.title_modal if title is not None else self.regular_modal, (0, 0))

    def show_simple_modal(
            self,
            body: str,
            title=None,
            on_close=empty,
            input_visible=False,
            pre_cleanup=empty,
            post_cleanup=empty
    ):
        self.curr_modal = {
            'body': body,
            'title': title,
            'pre_cleanup': on_close or pre_cleanup,
            'post_cleanup': post_cleanup,
            'type': ModalType.SIMPLE,
            'input_visible': input_visible
        }
        self.setup_simple_modal(body, title, input_visible)

    def show_simple_multi_modal(
            self,
            modals: list[MultiModalData] | tuple[MultiModalData, ...],
            pre_cleanup=empty,
            post_cleanup=empty,
    ):
        if len(modals) == 0:
            return
        self.curr_modal = {
            'modals': modals,
            'curr_index': 0,
            'type': ModalType.MULTI_SIMPLE,
            'pre_cleanup': pre_cleanup,
            'post_cleanup': post_cleanup,
        }
        first = modals[0]
        self.setup_simple_modal(first['body'], first.get('title'), first.get('input_visible') or False)
        self.update_button()

    def update_button(self):
        if self.curr_modal['type'] == ModalType.MULTI_SIMPLE and self.curr_modal['curr_index'] < len(
                self.curr_modal['modals']) - 1:
            self.okay_button.text_object.text = 'NEXT'
            self.okay_button.select_cursor = 'NEXT'
        else:
            self.okay_button.text_object.text = 'OKAY!'
            self.okay_button.select_cursor = 'NORMAL'

    def show_custom_modal(self, hud_object: HudObject, on_close=None, pre_cleanup=empty, post_cleanup=empty):
        self.game.input_handler.modal = hud_object
        self.curr_modal = {
            'object': hud_object,
            'type': ModalType.CUSTOM,
            'pre_cleanup': on_close or pre_cleanup,
            'post_cleanup': post_cleanup or empty,
        }

    def cancel_modal(self):
        self.to_cancel = True

    def modal_cleanup(self):
        self.curr_modal = None
        self.game.input_handler.modal = None
        self.game.just_ended_modal = True
        self.to_cancel = False
        self.input_box.visible = False
        self.input_box.clear_text()
        self.okay_button.predraw()
        self.game.cursor_handler.cursor = 'NORMAL'

    def draw(self):
        if self.curr_modal and not self.game.loading_handler.is_transitioning:
            if self.curr_modal['type'] == ModalType.SIMPLE:
                if self.okay_button.on_press_end or self.game.input_handler.key_on_down.get(
                        pygame.K_RETURN) or self.to_cancel:
                    if self.curr_modal['input_visible'] and self.input_box.data == '':
                        self.input_box.error = 'Input cannot be empty!'
                    else:
                        post_cleanup = self.curr_modal['post_cleanup']
                        self.curr_modal['pre_cleanup']()
                        self.modal_cleanup()
                        post_cleanup()
                        return
                if self.curr_modal['input_visible']:
                    self.input_box.rect.topleft = (
                        self.body.rect.left, self.body.rect.top + self.body.rect.height + self.input_gap)
                self.modal_object.draw()
            elif self.curr_modal['type'] == ModalType.CUSTOM:
                if self.to_cancel:
                    post_cleanup = self.curr_modal['post_cleanup']
                    self.curr_modal['pre_cleanup']()
                    self.modal_cleanup()
                    post_cleanup()
                    return
                self.curr_modal['object'].draw()
            elif self.curr_modal['type'] == ModalType.MULTI_SIMPLE:
                if self.okay_button.on_press_end or self.game.input_handler.key_on_down.get(
                        pygame.K_RETURN):
                    curr_index = self.curr_modal['curr_index']
                    if curr_index < len(self.curr_modal['modals']) - 1:
                        (self.curr_modal['modals'][curr_index].get('after') or empty)()
                        self.curr_modal['curr_index'] += 1
                        curr = self.curr_modal['modals'][curr_index + 1]
                        self.setup_simple_modal(curr['body'], curr.get('title'), curr.get('input_visible') or False)
                        self.update_button()
                    else:
                        (self.curr_modal['modals'][curr_index].get('after') or empty)()
                        self.curr_modal['pre_cleanup']()
                        post = self.curr_modal['post_cleanup']
                        self.modal_cleanup()
                        post()
                        return
                self.modal_object.draw()
