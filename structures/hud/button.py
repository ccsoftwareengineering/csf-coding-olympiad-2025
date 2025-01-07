from typing import Optional, Tuple
from typing import TYPE_CHECKING

import pygame

from structures.event_emitter import EventEmitter

if TYPE_CHECKING:
    from structures.game import Game
from structures.hud.hud_object import HudObject


class Button(HudObject, EventEmitter):
    def __init__(
            self,
            game: 'Game',
            surface: pygame.Surface,
            pos: Optional[Tuple[int, int]] = (0, 0),
            scale: Optional[float] = 1,
            select_cursor: Optional[str] = 'HIGHLIGHT',
            parent: Optional[HudObject] = None,
            object_id: Optional[str] = None
    ):
        super().__init__(game, surface, pos, scale, object_id=object_id, parent=parent)
        EventEmitter.__init__(self)
        # Press Events
        self.on_press_start = False
        self.on_press_end = False
        self.pressing = False

        # Hover Events
        self.on_hover_start = False
        self.on_hover_end = False
        self.hovering = False
        self.darker_surface = self.get_darker_surface()
        self.select_cursor = select_cursor

    def get_darker_surface(self, surface=None):
        if surface is None:
            surface = self.surface
        darker_surface = surface.copy()
        mask = pygame.mask.from_surface(surface).to_surface(setcolor=(0, 0, 0), unsetcolor=(255, 255, 255))
        mask.set_colorkey((255, 255, 255))
        mask.set_alpha(int(255 * 0.15))
        darker_surface.blit(mask, (0, 0))
        return darker_surface

    def reset_events(self):
        self.on_press_start = False
        self.on_press_end = False
        self.on_hover_start = False
        self.on_hover_end = False

    def handle_events(self):
        if not self.enabled:
            self.reset_events()
            return
        if self.on_hover_start:
            self.emit('on_hover_start', self)
            self.game.input_handler.buttons.emit('on_hover_start', self)
        if self.hovering:
            self.emit('hovering', self)
            self.game.input_handler.buttons.emit('hovering', self)
        if self.on_press_start:
            self.emit('on_press_start', self)
            self.game.input_handler.buttons.emit('on_press_start', self)
        if self.pressing:
            self.emit('pressing', self)
            self.game.input_handler.buttons.emit('pressing', self)
        if self.on_press_end:
            self.emit('on_press_end', self)
            self.game.input_handler.buttons.emit('on_press_end', self)
        if self.on_hover_end:
            self.emit('on_hover_end', self)
            self.game.input_handler.buttons.emit('on_hover_end', self)

        self.reset_events()

    def predraw(self):
        pos = pygame.mouse.get_pos()

        self.handle_events()

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
