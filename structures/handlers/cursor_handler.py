import typing

import modules.utilities as u

if typing.TYPE_CHECKING:
    from structures.game import Game


class CursorHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.cursors = {
            'NORMAL': u.load_scale('assets/cursor.png', factor=2),
            'HIGHLIGHT': u.load_scale('assets/cursor_highlight.png', factor=2),
            'INPUT': u.load_scale('assets/cursor_type.png', factor=2)
        }
        self.cursor = self.cursors['NORMAL']

    def set_cursor(self, cursor):
        self.cursor = self.cursors.get(cursor) or self.cursors.get('NORMAL')