import typing

import pygame
from pygame import Surface

from modules import utilities as u
from modules.constants import text_multiplier
from modules.more_utilities.enums import HorizontalAlignment

if typing.TYPE_CHECKING:
    from structures.game import Game
from structures.hud.hud_object import HudObject


class Text(HudObject):
    def __init__(
            self,
            game: 'Game',
            size: int,
            text: typing.Optional[str] = "",
            pos: tuple[int, int] = (0, 0),
            end_padding=0,
            parent: typing.Optional[HudObject] = None,
            color: typing.Optional[u.TupleColor] = (255, 255, 255),
            wrap: typing.Optional[bool] = True,
            outline: typing.Optional[int] = 0,
            # bottom_stack: typing.Optional[int] = 0,
            align: HorizontalAlignment = HorizontalAlignment.LEFT,
            max_width: int = 0,
            outline_color: typing.Optional[u.TupleColor] = (0, 0, 0),
    ):
        self.color = color or (0, 0, 0)
        self.end_padding = end_padding
        self.max_width = max_width
        self._size = size
        self.text = text or ""
        self.wrap = wrap
        self.align = align
        self.outline = outline or 0
        self.outline_color = outline_color or (0, 0, 0)
        self.font = u.get_main_font(size)
        super().__init__(game, Surface((0, 0)), parent=parent, pos=pos)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self.font = u.get_main_font(value)

    def calculate_surface(self, color=None):
        if not color:
            color = self.color
        if not self.wrap:
            return self.font.render(self.text, False, color)
        words = (self.text or '').split(' ')
        allowed_width = self.max_width or (self.game.screen.get_width() - self.rect.x - self.end_padding)
        if self.parent is not None:
            allowed_width = self.max_width or (self.parent.surface.get_width() - self.rect.x - self.end_padding)
        lines = []
        while len(words) > 0:
            line_words = []
            while len(words) > 0:
                word = words.pop(0)
                chunked = word.split('\n')
                if len(chunked) > 1:
                    line_words.append(chunked[0])
                    for word in chunked[1:]:
                        words.insert(0, word)
                    break
                line_words.append(word)
                fw, fh = self.font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width or '\n' in word:
                    break
            line = ' '.join(line_words)
            lines.append(line)

        _, font_height = self.font.size('A')
        surf = pygame.Surface((allowed_width, len(lines) * font_height), pygame.SRCALPHA)
        surf.get_rect().topleft = self.surface.get_rect().topleft

        y_offset = 0
        half_aw = allowed_width//2
        for line in lines:
            # fw, fh = self.font.size(line)
            # topleft_x = self.rect.x - fw / 2
            # topleft_y = self.rect.y + y_offset
            line_surface = self.font.render(line, False, color)
            if self.align == HorizontalAlignment.LEFT:
                surf.blit(line_surface, (0, y_offset))
            elif self.align == HorizontalAlignment.RIGHT:
                surf.blit(line_surface, (allowed_width - line_surface.get_width(), y_offset))
            else:
                surf.blit(line_surface, (half_aw - line_surface.get_width()//2, y_offset))
            y_offset += line_surface.get_height()
        return surf

    def predraw(self):
        surf = self.calculate_surface().convert_alpha()
        if self.outline > 0:
            outline_surf = self.calculate_surface(self.outline_color)
            size = surf.get_size()
            double_outline = self.outline * 2
            text_surf = pygame.Surface((size[0] + double_outline, size[1] + double_outline), pygame.SRCALPHA)
            text_rect = text_surf.get_rect()
            offsets = [(ox, oy)
                       for ox in range(-self.outline, double_outline, self.outline)
                       for oy in range(-self.outline, double_outline, self.outline)
                       if ox != 0 or ox != 0
                       ]
            for ox, oy in offsets:
                px, py = text_rect.center
                text_surf.blit(outline_surf, outline_surf.get_rect(center=(px+ox, py+oy)))
            text_surf.blit(surf, surf.get_rect(center=text_rect.center))
            self.surface = text_surf
        else:
            self.surface = surf
        self.rect.size = self.surface.get_size()
        super().predraw()
        return surf
