import datetime
import pygame
from modules import utilities as u
from modules.utilities import get_main_font
from structures.game import Game

def draw_skipping_factory(game: Game, duration: float):
    initial = None
    skip_icon = u.load_scale('assets/skip.png', factor=5)
    font = get_main_font(32)

    def draw_skipping():
        game.cursor_handler.set_cursor('NORMAL')
        nonlocal initial
        if not initial:
            initial = datetime.datetime.now()
        u.draw_tiles(game.screen, game.bg_tile_scaled, game.tile_offset)
        game.tile_offset += 0.5
        u.center_blit(game.screen, skip_icon)
        difference = duration - (datetime.datetime.now() - initial).total_seconds()
        font_render = font.render(f'Player found! Skipping to main screen in {difference:.1f} seconds.', False, pygame.Color('white'))
        u.center_blit(game.screen, font_render, offsets=(None, skip_icon.get_height() - 40))
        if difference <= 0.1:
            game.set_state('main')

    return draw_skipping