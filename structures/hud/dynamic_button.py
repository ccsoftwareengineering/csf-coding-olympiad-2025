from typing import TYPE_CHECKING, Optional, TypedDict, NotRequired

import pygame
from pygame import Surface

import modules.utilities as u
from structures.hud.button import Button
from structures.hud.hud_object import HudObject
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game


class TextOptions(TypedDict):
    color: NotRequired[u.TupleColor]
    outline: NotRequired[int]
    outline_color: NotRequired[u.TupleColor]
    size: int


class DynamicButton(Button):
    def __init__(
            self,
            game: 'Game',
            size: tuple[int, int],
            text_options: TextOptions,
            text="",
            box_template: Optional[u.RectTemplate] = None,
            pos: Optional[tuple[int, int]] = (0, 0),
            scale: Optional[float] = 1,
            select_cursor: Optional[str] = 'HIGHLIGHT',
            parent: Optional[HudObject] = None,
            name: Optional[str] = None
    ):
        self.size = size
        self.box_template = box_template
        self.text_options = text_options
        self.text_object = Text(
            game,
            size=text_options['size'],
            color=text_options.get('color'),
            outline=text_options.get('outline'),
            outline_color=text_options.get('outline_color'),
            wrap=False
        )
        super().__init__(game, Surface((0, 0), pygame.SRCALPHA), pos, scale, select_cursor, parent, name)
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
        u.center_blit(darkened, text_surf, offsets=(0, -3))
        u.center_blit(surf, text_surf, offsets=(0, -3))
        return surf, darkened

    def predraw(self):
        self.surface, self.darker_surface = self.calculate_surface()
        self.rect.size = self.surface.get_size()
        super().predraw()
