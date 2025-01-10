from math import inf
from typing import TYPE_CHECKING, Optional, Tuple

import pygame
from pygame import Surface

import modules.utilities as u
from modules.more_utilities.enums import AnchorPoint, Direction, HorizontalAlignment, anchor_map

if TYPE_CHECKING:
    from structures.game import Game
from structures.hud.hud_object import HudObject


class ListLayout(HudObject):
    def __init__(
            self,
            game: 'Game',
            min_size: Optional[Tuple[int, int]] = (0, 0),
            max_size: Optional[Tuple[int, int]] = (inf, inf),
            size: Optional[Tuple[int, int]] = None,
            direction: Direction = Direction.DOWN,
            position: Optional[Tuple[int, int]] = (0, 0),
            scale: Optional[float] = 1,
            gap: Optional[int] = 0,
            parent: Optional[HudObject] = None,
            side: Optional[HorizontalAlignment] = HorizontalAlignment.RIGHT,
            object_id: Optional[str] = None,
            anchor_point: Optional[AnchorPoint] = AnchorPoint.TOP_LEFT,
            rect_template: Optional[u.RectTemplate] = None,
            padding: Optional[int] = 0,
    ):
        self.direction = direction
        self._anchor_point = anchor_point
        self.gap = gap
        self.padding = padding
        self.min_size = min_size
        self.max_size = max_size
        if size:
            self.min_size = size
            self.max_size = size
        self.rect_template = rect_template
        self.children_list: list[HudObject] = []
        self.direction_multiplier = 1 if self.direction in (Direction.DOWN, Direction.RIGHT) else -1
        self.vertical = self.direction in (self.direction.DOWN, self.direction.UP)
        self._side = side
        self.child_anchor_point = 'topleft' if side == HorizontalAlignment.RIGHT else 'topright'
        if self.vertical:
            self.axis_function = 'get_height'
            self.axis_value_placement = lambda v: (self.padding, v + self.padding * self.direction_multiplier)
        else:
            self.axis_function = 'get_width'
            self.axis_value_placement = lambda v: (v + self.padding * self.direction_multiplier, self.padding)
        self.anchor_calc_map = {
            AnchorPoint.TOP_LEFT: lambda x_offset, y_offset: (x_offset, y_offset),
            AnchorPoint.TOP_CENTER: lambda x_offset, y_offset: (self.rect.width / 2 + x_offset, y_offset),
            AnchorPoint.TOP_RIGHT: lambda x_offset, y_offset: (self.rect.width + x_offset, y_offset),
            AnchorPoint.MID_LEFT: lambda x_offset, y_offset: (x_offset, self.rect.height / 2 + y_offset),
            AnchorPoint.MID_CENTER: lambda x_offset, y_offset: (
                self.rect.width / 2 + x_offset, self.rect.height / 2 + y_offset),
            AnchorPoint.MID_RIGHT: lambda x_offset, y_offset: (
                self.rect.width + x_offset, self.rect.height / 2 + y_offset),
            AnchorPoint.BOTTOM_LEFT: lambda x_offset, y_offset: (
                x_offset, self.rect.height / 2 + y_offset + self.padding),
            AnchorPoint.BOTTOM_CENTER: lambda x_offset, y_offset: (
                self.rect.width / 2 + x_offset, self.rect.height + y_offset),
            AnchorPoint.BOTTOM_RIGHT: lambda x_offset, y_offset: (
                x_offset + self.rect.width - self.padding * 2, self.rect.height / 2 + y_offset + self.padding),
        }
        self.calc_function = self.anchor_calc_map[self._anchor_point]
        super().__init__(game, Surface(min_size, pygame.SRCALPHA), pos=position, object_id=object_id, parent=parent, scale=scale)
        setattr(self.rect, anchor_map[anchor_point.value], position)  # type: ignore[int]

        # supposed to be able to list elements with a gap in any direction and work regardless of the lists anchor point
        # basically save the position to an attribute too.
        # make all the children's anchor points the same as the list layout for easier placement
        # for direction, x = left right, y = up down, 1 = down, right -1 = up left
        # so change their rect position based on that
        # as well as resize and clamp between min and max

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        self._side = value
        self.child_anchor_point = 'topleft' if self._side == HorizontalAlignment.RIGHT else 'topright'

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

        total_width = max(self.min_size[0], min(total_width + self.padding * 2, self.max_size[0]))
        total_height = max(self.min_size[1], min(total_height + self.padding * 2, self.max_size[1]))

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
        # set size
        old_pos = getattr(self.rect, anchor_map[self.anchor_point.value])
        calculated_size = self.calculate_total_size()
        self.surface = pygame.Surface((calculated_size[0], calculated_size[1] + 1), pygame.SRCALPHA)
        if self.rect_template:
            self.surface.blit(self.rect_template(calculated_size), (0, 0))
        self.rect.size = self.surface.get_size()
        setattr(self.rect, anchor_map[self.anchor_point.value], old_pos)

        # firstly the positions
        accumulated_offset = 0
        for child in self.children_list:
            setattr(child.rect, self.child_anchor_point,
                    self.calc_function(*self.axis_value_placement(accumulated_offset)))
            # child it up with the anchor points
            val = (getattr((child.to_draw_surface or child.surface),
                           self.axis_function)() + self.gap) * self.direction_multiplier
            accumulated_offset += val
        super().predraw()
