from typing import Optional, Tuple
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from structures.game import Game
from structures.hud.hud_object import HudObject


class Button(HudObject):
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
        # Press Events
        self.on_press_start = False
        self.on_press_end = False
        self.pressing = False

        # Hover Events
        self.on_hover_start = False
        self.on_hover_end = False
        self.hovering = False
        self.event_dict_map = {}
        super().__init__(game, surface, pos, scale, object_id=object_id, parent=parent)
        self.darker_surface = self.get_darker_surface()
        self.select_cursor = select_cursor

    def subscribe(self, event, function, event_id="default"):
        if event not in self.event_dict_map:
            self.event_dict_map[event] = {}
        self.event_dict_map[event][event_id] = function

    def unsubscribe(self, event, event_id="default"):
        self.event_dict_map[event][event_id] = None

    def run_events(self, event, value):
        event = self.event_dict_map.get(event)
        if not event:
            return
        for func in event.values():
            if func is not None:
                func(value)

    def get_darker_surface(self, surface=None):
        if surface is None:
            surface = self.surface
        darker_surface = surface.copy()
        mask = pygame.mask.from_surface(surface).to_surface(setcolor=(0, 0, 0), unsetcolor=(255, 255, 255))
        mask.set_colorkey((255, 255, 255))
        mask.set_alpha(int(255 * 0.15))
        darker_surface.blit(mask, (0, 0))
        return darker_surface

    def handle_events(self):
        if self.on_hover_start:
            self.run_events('on_hover_start', self)
        if self.hovering:
            self.run_events('hovering', self)
        if self.on_press_start:
            self.run_events('on_press_start', self)
        if self.pressing:
            self.run_events('pressing', self)
        if self.on_press_end:
            self.run_events('on_press_end', self)
        if self.on_hover_end:
            self.run_events('on_hover_end', self)

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
