import pygame
from pygame import Rect
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from structures.game import Game


class HudObject:
    def __init__(
            self,
            game: 'Game',
            surface: pygame.Surface,
            pos: (int, int) = (0, 0),
            scale: float = 1,
            parent=None,
            name=None
    ):
        self.should_preserve = False
        self.to_draw_surface = None
        self.parent = None
        self.visible = True
        self.children = set()
        self.name = name
        if parent is not None:
            parent.add_child(self)
        self.game = game
        self.surface = pygame.transform.scale_by(surface, scale)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (pos[0], pos[1])

        self.hovering = False
        self.on_hover_start = False
        self.on_hover_end = False

        self.cached_abs_rect = None

    @property
    def absolute_rect(self):
        if self.cached_abs_rect:
            return self.cached_abs_rect
        left = self.rect.left
        top = self.rect.top
        rect: Rect = self.rect.copy()
        if self.parent is not None:
            rect.topleft = (left + self.parent.rect.left, top + self.parent.rect.top)
        self.cached_abs_rect = rect
        return rect

    @property
    def patriarch(self):
        if self.parent is not None:
            return self.parent.patriarch
        else:
            return self

    @property
    def is_child(self):
        return self.parent is not None

    def add_child(self, child, keep_preservation=False):
        self.children.add(child)
        if not keep_preservation:
            self.should_preserve = True
        child.parent = self

    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None
        if len(self.children) == 0:
            self.should_preserve = False

    def destroy(self):
        self.parent.remove_child(self)
        del self

    def draw_children(self, surface: pygame.Surface = None):
        if len(self.children) == 0:
            return
        else:
            for child in self.children:
                child.draw(draw_surface=surface)

    def preserve(self):
        if self.should_preserve:
            return (self.to_draw_surface or self.surface).copy()
        else:
            return self.to_draw_surface or self.surface

    @property
    def enabled(self):
        if self.game.input_handler.modal is not None and self.patriarch is not self.game.input_handler.modal:
            return False
        return True and self.visible

    def draw(self, draw_surface: pygame.Surface = None):
        if self.absolute_rect.collidepoint(pygame.mouse.get_pos()):
            self.on_hover_start = not self.hovering
            self.hovering = True
        else:
            self.on_hover_end = self.hovering
            self.hovering = False

        if not self.visible:
            return
        if draw_surface:
            surf = self.preserve()
            self.draw_children(surface=surf)
            draw_surface.blit(surf, self.rect)
        else:
            surf = self.preserve()
            self.draw_children(surface=surf)
            self.game.screen.blit(surf, self.rect)
        self.to_draw_surface = None
        self.cached_abs_rect = None
