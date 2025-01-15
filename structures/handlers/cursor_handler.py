import typing

import pygame
from pygame import Surface

import modules.utilities as u
from modules.more_utilities.enums import ActionState

if typing.TYPE_CHECKING:
    from structures.game import Game


class CursorHandler:
    cursor_cache_map = {}
    factor = 2
    translation = factor * 16
    cols = 19
    rows = 10

    def get_cursor_icon(self, rc: tuple[int, int]):
        row, col = rc
        the = self.cursor_cache_map.get(rc)
        if the:
            return the
        which = self.tilemap.subsurface(
            (col * self.translation, row * self.translation, self.translation, self.translation))
        self.cursor_cache_map[rc] = which
        return which

    def get_cursor_and_offsets(self, rc: tuple[int, int], offsets=(0, 0)):
        return self.get_cursor_icon(rc), offsets

    def __init__(self, game: 'Game'):
        self.tilemap = u.load_scale('assets/cursor_map.png', factor=self.factor)
        self.cursor_font = u.get_main_font(14)
        self.text = ''
        self.game = game
        self.cursors = {
            'NORMAL': self.get_cursor_and_offsets((1, 6)),
            'HIGHLIGHT': self.get_cursor_and_offsets((6, 17), (-5, 0)),
            'INPUT': self.get_cursor_and_offsets((7, 1)),
            'NEXT': self.get_cursor_and_offsets((3, 12)),
            'ADD': self.get_cursor_and_offsets((6, 2), (-8, 0)),
            'POINTER_QUESTION': self.get_cursor_and_offsets((8, 3)),
            'POINTER_CONFIG': self.get_cursor_and_offsets((8, 5)),
            'MODIFY': self.get_cursor_and_offsets((6, 12)),
            'X': self.get_cursor_and_offsets((0, 17), (-3, -3)),
            'REPAIR': self.get_cursor_and_offsets((6, 12)),
            'NONE': (Surface((0, 0)), (0, 0))
        }
        self._cursor = 'NORMAL'
        self.cursor_icon = self.cursors['NORMAL'][0]
        self.cursor_offset = self.cursors['NORMAL'][1]
        self.action_cursor_map = {
            ActionState.NONE: 'inherit',
            ActionState.DESTROYING: 'X',
            ActionState.PLACING: 'NONE',
            ActionState.UPGRADING: 'REPAIR'
        }

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor: str | tuple[int, int]):
        if self._cursor == cursor or cursor == 'inherit':
            return
        if cursor == 'NONE':
            self._cursor = 'NONE'
            return
        _cursor = self.cursors.get(cursor)
        if _cursor:
            self.cursor_icon = _cursor[0]
            self.cursor_offset = _cursor[1]
            self._cursor = cursor
        elif type(cursor) is tuple:
            self.cursor_icon = self.get_cursor_icon(cursor)
            self.cursor_offset = (0, 0)
            self._cursor = cursor
        else:
            self.cursor_icon, self.cursor_offset = self.cursors.get('NORMAL')
            self._cursor = 'NORMAL'

    def draw(self):
        if self._cursor == 'NONE':
            return
        self.cursor = self.action_cursor_map[self.game.observable_handler['action_state'].value]
        pos = pygame.mouse.get_pos()
        self.game.screen.blit(self.game.cursor_handler.cursor_icon,
                              (pos[0] + self.cursor_offset[0], pos[1] + self.cursor_offset[1]))
        self.game.screen.blit(
            self.cursor_font.render(self.text, False, (255, 255, 255)),
            (pos[0], pos[1] + self.game.cursor_handler.cursor_icon.get_height())
        )
