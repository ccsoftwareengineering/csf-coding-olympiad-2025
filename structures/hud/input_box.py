from typing import TYPE_CHECKING, Optional

import pygame

import modules.utilities as u
from structures.hud.hud_object import HudObject

if TYPE_CHECKING:
    from structures.game import Game


# add ops means additional options btw
def input_data(input_id: str, input_type="text", placeholder="", required=True, options=None):
    if options is None:
        options = {}
    return {
        "id": input_id,
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
                 radius=4,
                 outline=1,
                 pos: Optional[tuple[int, int]] = (0, 0),
                 scale: float = 1,
                 parent: Optional[HudObject] = None,
                 name=None):
        self.radius = radius
        self.outline = outline
        self.color = color
        self.selected_color = selected_color
        self.outline_color = outline_color
        self.size = size
        self.data = ""
        self.selected = False
        surface = u.rounded_rect(pos, color, round(size[0] / 200 * 64), radius, outline, outline_color)
        super().__init__(game, surface, pos, scale, parent, name)

    def on_mouse_up(self, event):
        if event.button != 1:
            return
        self.set_selected(u.pos_in_rect(event.pos, self.rect))

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

    def calculate_surface(self):
        return u.rounded_rect(self.rect.topleft, self.color, round(self.size[0] / 200 * 64), self.radius, self.outline,
                              self.selected and self.selected_color or self.outline_color)

    def process_up(self, up_event: pygame.event.Event):
        if up_event.key == pygame.K_ESCAPE:
            self.set_selected(False)

    def process_down(self, down_event: pygame.event.Event):
        if down_event.key == pygame.K_BACKSPACE:
            self.data = self.data[:-1]
        else:
            self.data += down_event.unicode

    def draw(self, draw_surface: pygame.Surface = None):
        self.surface = self.calculate_surface()
        self.rect = self.surface.get_rect()
        super().draw(draw_surface)
