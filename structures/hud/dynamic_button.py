from typing import TYPE_CHECKING, Optional

import pygame
from pygame import Surface

import modules.utilities as u
from modules.more_utilities.types import TextOptions
from structures.hud.button import Button
from structures.hud.hud_object import HudObject
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game

class DynamicButton(Button):
    def __init__(
            self,
            game: 'Game',
            size: tuple[int, int],
            text_options: TextOptions,
            text="",
            rect_template: Optional[u.RectTemplate] = None,
            pos: Optional[tuple[int, int]] = (0, 0),
            scale: Optional[float] = 1,
            select_cursor: Optional[str] = 'HIGHLIGHT',
            parent: Optional[HudObject] = None,
            object_id: Optional[str] = None,
            attributes: Optional[dict[str, any]] = None,
            wrap: Optional[int] = False,
            max_text_width: Optional[int] = None
    ):
        self.size = size
        self.box_template = rect_template
        self.text_options = text_options
        self.text_object = Text(
            game,
            size=text_options['size'],
            color=text_options.get('color'),
            outline=text_options.get('outline'),
            outline_color=text_options.get('outline_color'),
            max_width=max_text_width,
            wrap=wrap
        )
        super().__init__(game, Surface((0, 0), pygame.SRCALPHA), pos, scale, select_cursor, parent, object_id,
                         attributes=attributes)
        self.surface, self.darker_surface = self.calculate_surface()
        self.rect.size = self.surface.get_size()
        self.text_object.text = text
        self.predraw()

    def calculate_surface(self):
        surf = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        if self.box_template:
            surf.blit(self.box_template(self.size), (0, 0))
        self.text_object.predraw()
        text_surf = self.text_object.surface
        darkened = surf.copy()
        darkened = self.get_darker_surface(darkened)
        u.center_blit(
            surf,
            text_surf,
            offsets=self.text_options.get('offsets') or (None, None),
            xy=self.text_options.get('xy') or (None, None)
        )
        u.center_blit(
            darkened,
            text_surf,
            offsets=self.text_options.get('offsets') or (None, None),
            xy=self.text_options.get('xy') or (None, None)
        )
        return surf, darkened

    def predraw(self):
        if self.object_id == 'add_button':
            self.game.telemetry_handler.set_value('add_button', (self.hovering, self.on_hover_start, self.on_hover_end,
                                                                 self.on_press_start, self.on_press_end))
        self.surface, self.darker_surface = self.calculate_surface()
        self.rect.size = self.surface.get_size()
        super().predraw()
