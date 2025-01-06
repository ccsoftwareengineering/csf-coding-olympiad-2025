from typing import TYPE_CHECKING

import pygame
from pygame import Surface

import modules.utilities as u

from structures.hud.hud_object import HudObject

if TYPE_CHECKING:
    from structures.game import Game


class DynamicHudObject(HudObject):
    def __init__(
            self,
            game: 'Game',
            size: tuple[int, int],
            rect_template: u.RectTemplate = None,
            position: (int, int) = (0, 0),
            scale: float = 1,
            parent=None,
            object_id=None,
            children_enabled=True,
            **kwargs
    ):
        self.rect_template = rect_template
        self._size = size
        surf = Surface(size, pygame.SRCALPHA)
        if rect_template:
            surf.blit(rect_template(size), (0, 0))
        super().__init__(game, surf, position, scale, parent, object_id, children_enabled)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value
        self.rect.size = value
        surf = Surface(value, pygame.SRCALPHA)
        if self.rect_template:
            surf.blit(self.rect_template(value), (0, 0))
