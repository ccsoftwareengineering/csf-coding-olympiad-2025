from typing import TYPE_CHECKING, Optional

import pygame
from pygame import Surface

from modules.constants import white
from modules.more_utilities.text import TextOptions, IconOptions
from structures.hud.hud_object import HudObject
from structures.hud.types import Text

if TYPE_CHECKING:
    from structures.game import Game

import modules.utilities as u


class IconValue(HudObject):
    def __init__(
            self,
            game: 'Game',
            text_options: TextOptions,
            icon: IconOptions | Surface,
            gap: Optional[int] = 10,
            text: Optional[str] = "",
            position: (int, int) = (0, 0),
            parent=None,
            object_id=None,
            attributes=None,
            **kwargs
    ):
        super().__init__(
            game,
            Surface((0, 0)),
            position,
            1,
            parent,
            object_id,
            True,
            attributes,
            **kwargs
        )
        self.text_object = Text.from_options(game, text_options, {
            'color': white,
        })
        self.text_object.wrap = False
        self.text_object.text = text
        self.gap = gap
        self.icon = icon if isinstance(icon, Surface) else u.load_scale(
            icon['path'],
            size=icon['size'],
            factor=icon['factor'] or 1)
        self.icon_rect = self.icon.get_rect()

    def predraw(self):
        self.text_object.predraw()
        surf = Surface((
            self.icon_rect.w + self.gap + self.text_object.rect.w,
            max(self.text_object.rect.h, self.icon.get_height()),
        ), pygame.SRCALPHA)
        center_y = surf.get_height() // 2
        self.icon_rect.midleft = (0, center_y)
        surf.blit(self.icon, self.icon_rect)
        self.text_object.rect.midleft = (self.icon_rect.w + self.gap, center_y)
        surf.blit(self.text_object.surface, self.text_object.rect)
        self.surface = surf
        self.rect.size = self.surface.get_size()
