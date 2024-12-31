import typing

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

    def __init__(self, game: 'Game'):
        self.tilemap = u.load_scale('assets/cursor_map.png', factor=self.factor)
        self.game = game
        self.cursors = {
            'NORMAL': self.get_cursor_icon(1, 7),  # u.load_scale('assets/cursor.png', factor=2),
            'HIGHLIGHT': self.get_cursor_icon(8, 17), #u.load_scale('assets/cursor_highlight.png', factor=2),
            'INPUT': u.load_scale('assets/cursor_type.png', factor=2)
        }
        self.cursor = self.cursors['NORMAL']

    def set_cursor(self, cursor: str):
        _cursor = self.cursors.get(cursor)
        if _cursor:
            self.cursor = _cursor
        else:
            row, col = [int(x) for x in cursor.split(',')]
            self.cursor = self.get_cursor_icon(row, col)
