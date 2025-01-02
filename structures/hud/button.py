from typing import Optional, Tuple

import pygame
from structures.hud.hud_object import HudObject

from structures.game import Game


class Button(HudObject):
    def __init__(
            self,
            game: Game,
            surface: pygame.Surface,
            pos: Optional[Tuple[int, int]] = (0, 0),
            scale: Optional[float] = 1,
            select_cursor: Optional[str] = 'HIGHLIGHT',
            parent: Optional[HudObject] = None,
            name: Optional[str] = None
    ):
        # Press Events
        self.on_press_start = False
        self.on_press_end = False
        self.pressing = False

        # Hover Events
        self.on_hover_start = False
        self.on_hover_end = False
        self.hovering = False
        super().__init__(game, surface, pos, scale, name=name, parent=parent)
        self.darker_surface = self.surface.copy()
        self.select_cursor = select_cursor
        mask = pygame.mask.from_surface(self.surface).to_surface(setcolor=(0, 0, 0), unsetcolor=(255, 255, 255))
        mask.set_colorkey((255, 255, 255))
        mask.set_alpha(int(255 * 0.15))
        self.darker_surface.blit(mask, (0, 0))

    def predraw(self):
        pos = pygame.mouse.get_pos()

        if self.absolute_rect.collidepoint(pos) and self.enabled:
            self.game.cursor_handler.cursor = self.select_cursor
            self.on_hover_start = not self.hovering
            self.hovering = True

            if pygame.mouse.get_pressed()[0]:
                self.on_press_start = not self.pressing
                self.pressing = True
            else:
                self.on_press_end = self.pressing
                self.pressing = False
                self.to_draw_surface = self.darker_surface
        else:
            if self.hovering:
                self.game.cursor_handler.cursor = 'NORMAL'
            self.on_hover_end = self.hovering
            self.hovering = False
        super().predraw()
