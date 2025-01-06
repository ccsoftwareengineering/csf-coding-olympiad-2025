import datetime
from typing import TYPE_CHECKING, Optional

import pygame
from pygame import Surface

import modules.utilities as u
from modules.utilities import get_main_font, lerp_colors
from structures.hud.hud_object import HudObject
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game


# add ops means additional options btw
def input_data(input_id: str, input_type="text", placeholder="", required=True, options=None):
    if options is None:
        options = {}
    return {
        "object_id": input_id,
        "type": input_type,
        "placeholder": placeholder,
        "required": required,
        "options": options,
    }


class InputBox(HudObject):
    def __init__(self,
                 game: 'Game',
                 size: tuple[int, int],
                 color: tuple[int, int, int, int] = (255, 162, 112, 255),
                 outline_color: tuple[int, int, int, int] = (211, 70, 0, 255),
                 selected_color: tuple[int, int, int, int] = (54, 65, 99, 255),
                 text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
                 error_color: tuple[int, int, int, int] = (150, 0, 0, 255),
                 error_text_size: int = 12,
                 error_expiry_time: int = 2,
                 text_size: int = 20,
                 data=None,
                 radius=4,
                 outline=1,
                 pos: Optional[tuple[int, int]] = (0, 0),
                 scale: float = 1,
                 override_y=True,
                 parent: Optional[HudObject] = None,
                 object_id=None):
        self.game = game
        self.override_y = override_y
        self.radius = radius
        self.outline = outline
        self.color = color
        self.selected_color = selected_color
        self.outline_color = outline_color
        self._size = size
        self.data = ""
        self._error = None
        self.selected = False
        self.error_set_time = None
        self.backspace_timer = None
        self.text_color = text_color
        self.error_text_surface = None
        self.input_data: dict = data or {}
        self.text_size = text_size
        self.error_color = error_color
        self.error_expiry_time = error_expiry_time
        self.error_text = get_main_font(error_text_size)
        surface = u.rounded_rect(size, color, round(size[0] / 200 * 64), radius, outline, outline_color)
        super().__init__(game, surface, pos, scale, parent, object_id)
        self.text = Text(game, parent=self, size=text_size, color=text_color, pos=(10, 10))

    @property
    def size(self):
        return self.surface.get_size()

    @size.setter
    def size(self, value):
        self.rect.size = value
        self.surface = self.calculate_surface()

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value
        if value is not None:
            self.error_set_time = datetime.datetime.now()
            self.error_text_surface = self.error_text.render(self.error, False, self.error_color)
        else:
            self.error_set_time = None
            self.error_text_surface = None

    def on_mouse_up(self, event):
        if event.button != 1:
            return
        self.set_selected(self.hovering and self.enabled)

    def set_selected(self, selected: bool):
        if self.selected == selected:
            return
        self.selected = selected
        if self.selected:
            if self.game.input_handler.selected_input_box:
                self.game.input_handler.selected_input_box.set_selected(False)
            self.game.input_handler.selected_input_box = self
            self.game.input_handler.subscribe("mouse_on_up", self.on_mouse_up, "input_box_selection")
        else:
            self.game.input_handler.selected_input_box = None
            self.game.input_handler.unsubscribe("mouse_on_up", "input_box_selection")

    def calculate_surface(self, y=None):
        return u.rounded_rect(
            (self.size[0], y or self.size[1]),
            self.color,
            round(self.size[0] / 200 * 64),
            self.radius,
            self.outline,
            self.error is not None and self.error_color or (self.selected and self.selected_color or self.outline_color)
        )

    def process_up(self, up_event: pygame.event.Event):
        if up_event.key == pygame.K_ESCAPE:
            self.set_selected(False)
        elif up_event.key == pygame.K_BACKSPACE:
            self.backspace_timer = None

    acceptable = set(
        list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()-_=+`~[]\\{}|;\':",./<>? '))

    def backspace(self):
        self.data = self.data[:-1]

    def process_down(self, down_event: pygame.event.Event):
        if down_event.key == pygame.K_BACKSPACE:
            self.backspace()
            self.backspace_timer = datetime.datetime.now()
        elif down_event.unicode in self.acceptable:
            self.data += down_event.unicode

    def periodic(self):
        if self.error_set_time and (
                datetime.datetime.now() - self.error_set_time).total_seconds() >= self.error_expiry_time:
            self.error = None

        if self.hovering:
            if self.on_hover_start:
                self.game.cursor_handler.cursor = 'INPUT'
            if pygame.mouse.get_pressed()[0]:
                self.set_selected(True)
        elif self.on_hover_end:
            self.game.cursor_handler.cursor = 'NORMAL'

        if self.selected and self.backspace_timer is not None:
            if (datetime.datetime.now() - self.backspace_timer).microseconds >= 400_000:
                self.backspace()

    def predraw(self):
        self.periodic()

        self.text.text = self.data or self.input_data.get('placeholder')
        y = self.size[1]
        if self.override_y:
            y = self.text.calculate_surface().get_height() + 20
        surf = self.calculate_surface(y=y)
        surf_size = surf.get_size()

        if self.error:
            error_size = self.error_text_surface.get_size()
            big_surf = Surface(
                (max([surf_size[0], error_size[0]]), surf_size[1] + error_size[1] + 20),
                pygame.SRCALPHA,
            )
            big_surf.blit(surf, (0, 0))
            big_surf.blit(self.error_text_surface, (0, surf_size[1] + 10))
            self.to_draw_surface = big_surf
        else:
            self.surface = surf
        if self.data == "":
            self.text.color = lerp_colors(self.color, self.text_color, 0.65)
        else:
            self.text.color = self.text_color
        super().predraw()