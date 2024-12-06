import pygame
from structures.hud.hud_object import HudObject

from structures.game import Game


class Button(HudObject):
    # Press Events
    on_press_start = False
    on_press_end = False
    pressing = False

    # Hover Events
    on_hover_start = False
    on_hover_end = False
    hovering = False

    def __init__(self, game: Game, surface: pygame.Surface, pos: (int, int) = (0, 0), scale: float = 1, name=None):
        super().__init__(game, surface, pos, scale, name=name)
        self.darker_surface = self.surface.copy()
        mask = pygame.mask.from_surface(self.surface).to_surface(setcolor=(0, 0, 0), unsetcolor=(255, 255, 255))
        mask.set_colorkey((255, 255, 255))
        mask.set_alpha(int(255 * 0.15))
        self.darker_surface.blit(mask, (0, 0))

    def draw(self):
        pos = pygame.mouse.get_pos()
        to_draw = self.surface

        if self.rect.collidepoint(pos):
            self.on_hover_start = not self.hovering
            self.hovering = True

            if pygame.mouse.get_pressed()[0]:
                self.on_press_start = not self.pressing
                self.pressing = True
            else:
                self.on_press_end = self.pressing
                self.pressing = False
                to_draw = self.darker_surface
        else:
            self.on_hover_end = self.hovering
            self.hovering = False

        self.game.screen.blit(to_draw, (self.rect.x, self.rect.y))
        self.draw_children()
