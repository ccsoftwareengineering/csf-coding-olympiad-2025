from typing import TYPE_CHECKING

import pygame
from pygame import Rect

from modules.more_utilities.guide_helpers import get_curr_guide_info
from structures.store import Store

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
            object_id=None,
            children_enabled=True,
            attributes=None,
            **kwargs
    ):
        if not attributes:
            attributes = {}
        self.should_preserve = False
        self.to_draw_surface = None
        self.parent = None
        self.visible = True
        self.children = set()
        self.object_id = object_id
        if object_id:
            game.hud_object_store.set(object_id, self)
        if parent is not None:
            parent.add_child(self)
        self.game = game
        self.surface = pygame.transform.scale_by(surface, scale)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (pos[0], pos[1])

        self.hovering = False
        self.on_hover_start = False
        self.on_hover_end = False
        self.children_enabled = children_enabled
        self.attributes = Store(attributes)

    @property
    def current_surface(self):
        return self.to_draw_surface or self.surface

    @property
    def absolute_rect(self):
        left = self.rect.left
        top = self.rect.top
        rect: Rect = self.rect.copy()
        if self.parent is not None:
            rect.topleft = (left + self.parent.absolute_rect.left, top + self.parent.absolute_rect.top)
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
        if self.parent:
            self.parent.remove_child(self)
        del self

    def draw_children(self, surface: pygame.Surface = None, predraw=True):
        if len(self.children) == 0:
            return
        else:
            for child in self.children:
                child.draw(draw_surface=surface, predraw=predraw)

    def preserve(self):
        if self.should_preserve:
            return (self.to_draw_surface or self.surface).copy()
        else:
            return self.to_draw_surface or self.surface

    @property
    def enabled(self):
        if self.game.input_handler.modal is not None and self.patriarch is not self.game.input_handler.modal:
            return False
        if self.game.in_guide and self.object_id != 'ok_guide_button':
            curr_guide_info = get_curr_guide_info(self.game)
            if not curr_guide_info['rect'].colliderect(self.absolute_rect) or not curr_guide_info['gui_enabled']:
                return False
        return (
                True and self.visible and
                not self.game.loading_handler.is_transitioning and
                self.game.placement_info is None
        )

    def predraw(self):
        if self.absolute_rect.collidepoint(pygame.mouse.get_pos()):
            self.on_hover_start = not self.hovering
            self.hovering = True
        else:
            self.on_hover_end = self.hovering
            self.hovering = False

    def draw(self, draw_surface: pygame.Surface = None, predraw=True, children_predraw=True):
        if predraw:
            self.predraw()
        if not self.visible:
            return
        surf = self.preserve()
        self.draw_children(surface=surf, predraw=children_predraw)
        (draw_surface or self.game.screen).blit(surf, self.rect)
        # if draw_surface:
        #     draw_surface.blit(surf, self.rect)
        # else:
        #     self.game.screen.blit(surf, self.rect)
        self.to_draw_surface = None
