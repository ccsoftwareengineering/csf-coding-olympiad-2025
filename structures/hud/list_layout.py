from math import inf
from typing import TYPE_CHECKING, Optional

import pygame
from pygame import Surface

from modules.more_utilities.enums import AnchorPoint, Direction, anchor_map

if TYPE_CHECKING:
    from structures.game import Game
from structures.hud.hud_object import HudObject


class ListLayout(HudObject):
    def __init__(
            self,
            game: 'Game',
            min_width: (int, int) = (0, 0),
            max_width: (int, int) = (inf, inf),
            direction: Direction = Direction.DOWN,
            position: Optional[(int, int)] = (0, 0),
            scale: Optional[float] = 1,
            gap: Optional[int] = 0,
            parent: Optional[HudObject] = None,
            name: Optional[str] = None,
            anchor_point: Optional[AnchorPoint] = AnchorPoint.TOP_LEFT
    ):
        self.direction = direction
        self._anchor_point = anchor_point
        self.gap = gap
        self.min_size = min_width
        self.max_size = max_width
        self.children_list: list[HudObject] = []
        self.direction_multiplier = (self.direction in (self.direction.DOWN, self.direction.RIGHT)) and 1 or -1
        self.vertical = self.direction in (self.direction.DOWN, self.direction.UP)
        if self.vertical:
            self.axis_function = 'get_height'
            self.axis_value_placement = lambda v: (0, v)
        else:
            self.axis_function = 'get_width'
            self.axis_value_placement = lambda v: (v, 0)
        self.anchor_calc_map = {
            AnchorPoint.TOP_LEFT: lambda x_offset, y_offset: (
                self.rect.topleft[0] + x_offset, self.rect.topleft[1] + y_offset),
            AnchorPoint.TOP_CENTER: lambda x_offset, y_offset: (
                self.rect.centerx + x_offset, self.rect.topleft[1] + y_offset),
            AnchorPoint.TOP_RIGHT: lambda x_offset, y_offset: (
                self.rect.topright[0] + x_offset, self.rect.topleft[1] + y_offset),
            AnchorPoint.MID_LEFT: lambda x_offset, y_offset: (
                self.rect.topleft[0] + x_offset, self.rect.centery + y_offset),
            AnchorPoint.MID_CENTER: lambda x_offset, y_offset: (
                self.rect.centerx + x_offset, self.rect.centery + y_offset),
            AnchorPoint.MID_RIGHT: lambda x_offset, y_offset: (
                self.rect.topright[0] + x_offset, self.rect.centery + y_offset),
            AnchorPoint.BOTTOM_LEFT: lambda x_offset, y_offset: (
                self.rect.topleft[0] + x_offset, self.rect.bottomleft[1] + y_offset),
            AnchorPoint.BOTTOM_CENTER: lambda x_offset, y_offset: (
                self.rect.centerx + x_offset, self.rect.bottomleft[1] + y_offset),
            AnchorPoint.BOTTOM_RIGHT: lambda x_offset, y_offset: (
                self.rect.topright[0] + x_offset, self.rect.bottomleft[1] + y_offset),
        }
        self.calc_function = self.anchor_calc_map[self._anchor_point]
        super().__init__(game, Surface(min_width, pygame.SRCALPHA), pos=position, name=name, parent=parent, scale=scale)
        setattr(self.rect, anchor_map[anchor_point.value], position)  # type: ignore[int]

        # supposed to be able to list elements with a gap in any direction and work regardless of the lists anchor point
        # basically save the position to an attribute too.
        # make all the children's anchor points the same as the list layout for easier placement
        # for direction, x = left right, y = up down, 1 = down, right -1 = up left
        # so change their rect position based on that
        # as well as resize and clamp between min and max

    @property
    def anchor_point(self) -> AnchorPoint:
        return self._anchor_point

    @anchor_point.setter
    def anchor_point(self, value: AnchorPoint):
        self._anchor_point = value
        self.calc_function = self.anchor_calc_map[self._anchor_point]

    def calculate_total_size(self):
        total_width = 0
        total_height = 0

        if self.vertical:
            total_height += (len(self.children) - 1) * self.gap
            for child in self.children_list:
                child.predraw()
                child_size = (child.to_draw_surface or child.surface).get_size()
                total_width = max(total_width, child_size[0])
                total_height += child_size[1]
        else:
            total_width += (len(self.children) - 1) * self.gap
            for child in self.children_list:
                child.predraw()
                child_size = (child.to_draw_surface or child.surface).get_size()
                total_height = max(total_height, child_size[1])
                total_width += child_size[0]

        total_width = max(self.min_size[0], min(total_width, self.max_size[0]))
        total_height = max(self.min_size[1], min(total_height, self.max_size[1]))

        return total_width, total_height

    def insert_child(self, child, index):
        self.children_list.insert(index, child)
        super().add_child(child, False)

    def add_child(self, child, _=False):
        self.children_list.append(child)
        super().add_child(child, False)

    def remove_child(self, child):
        self.children_list.remove(child)
        super().remove_child(child)

    def predraw(self):
        # firstly the positions
        accumulated_offset = 0
        for child in self.children_list:
            child.rect.topleft = self.calc_function(*self.axis_value_placement(accumulated_offset))
            # child it up with the anchor points
            accumulated_offset += getattr((child.to_draw_surface or child.surface), self.axis_function)() + self.gap
        super().predraw()
