import pygame
from modules import utilities as u
import typing
if typing.TYPE_CHECKING:
    from structures.game import Game
from structures.hud.hud_object import HudObject

text_cache = {}


class Text(HudObject):
    def __init__(
            self,
            game: 'Game',
            size: int,
            text: str = "",
            pos: (int, int) = (0, 0),
            parent=None,
            color=None,
            wrap=True
    ):
        self.color = color or (0, 0, 0, 100)
        self.end_padding = 0
        self.size = size
        self.text = text
        self.wrap = wrap
        self.font = text_cache.get(size) or pygame.font.Font(u.resource_path('assets/fonts/main_reg.ttf'), size)
        super().__init__(game, self.font.render(text, False, self.color), parent=parent, pos=pos)

    def set_size(self, size: int):
        self.font = text_cache.get(size) or pygame.font.Font(u.resource_path('assets/fonts/main_reg.ttf'), size)
        self.size = size

    def draw(self, draw_surface: pygame.Surface = None):
        if not self.wrap:
            self.surface = self.font.render(self.text, False, self.color)
            super().draw(draw_surface)
            return
        words = self.text.split(' ')
        allowed_width = self.game.screen.get_width() - self.rect.x
        if self.parent is not None:
            allowed_width = self.parent.surface.get_width() - self.rect.x
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
        for line in lines:
            fw, fh = self.font.size(line)
            topleft_x = self.rect.x - fw / 2
            topleft_y = self.rect.y + y_offset
            line_surface = self.font.render(line, False, self.color)
            surf.blit(line_surface, (0, y_offset))
            y_offset += line_surface.get_height()

        self.surface = surf
        super().draw(draw_surface)
