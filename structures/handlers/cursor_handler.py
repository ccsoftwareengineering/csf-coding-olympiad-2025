import typing

import pygame

import modules.utilities as u

if typing.TYPE_CHECKING:
    from structures.game import Game


class CursorHandler:
    cursor_cache_map = {}
    factor = 2
    translation = factor * 16
    cols = 19
    rows = 10

    def get_cursor_icon(self, row, col):
        key = f'{row},{col}'
        the = self.cursor_cache_map.get(key)
        if the:
            return the
        which = self.tilemap.subsurface(
            (col * self.translation, row * self.translation, self.translation, self.translation))
        self.cursor_cache_map[key] = which
        return which

    def get_cursor_and_offsets(self, row, col, offsets=(0, 0)):
        return self.get_cursor_icon(row, col), offsets

    def __init__(self, game: 'Game'):
        self.tilemap = u.load_scale('assets/cursor_map.png', factor=self.factor)
        self.game = game
        self.cursors = {
            'NORMAL': self.get_cursor_and_offsets(1, 6),
            'HIGHLIGHT': self.get_cursor_and_offsets(6, 17, (-3, 0)),
            'INPUT': self.get_cursor_and_offsets(7, 1),
            'NEXT': self.get_cursor_and_offsets(3, 12),
        }
        self._cursor = 'NORMAL'
        self.cursor_icon = self.cursors['NORMAL'][0]
        self.cursor_offset = self.cursors['NORMAL'][1]

    @property
    def cursor(self):
        return self._cursor

    def row_col_from_key(self, key):
        return (int(x) for x in self.cursor.split(','))

    @cursor.setter
    def cursor(self, cursor: str):
        _cursor = self.cursors.get(cursor)
        if _cursor:
            self.cursor_icon = _cursor[0]
            self.cursor_offset = _cursor[1]
        elif ',' in cursor:
            row, col = [int(x) for x in cursor.split(',')]
            self.cursor_icon = self.get_cursor_icon(row, col)
            self.cursor_offset = (0, 0)
        else:
            self.cursor_icon, self.cursor_offset = self.cursors.get('NORMAL')

    def draw(self):
        pos = pygame.mouse.get_pos()
        self.game.screen.blit(self.game.cursor_handler.cursor_icon,
                              (pos[0] + self.cursor_offset[0], pos[1] + self.cursor_offset[1]))
