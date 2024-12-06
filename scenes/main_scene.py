import utilities as u
import pygame

from structures.hud.button import Button
from structures.game import Game, game_states

play_button_surface = u.load_scale('assets/play_button.png', None, 1.6)


def draw_tiles(g: Game, scr: pygame.Surface, tile: pygame.Surface, offset: int):
    width_increment = -offset
    while width_increment < g.screen.get_width() + 64:
        height_increment = -offset
        while height_increment < g.screen.get_height() + 64:
            scr.blit(tile, (width_increment, height_increment))
            height_increment = height_increment + 64
        width_increment += 64


tile_offset = 0


def draw_main_factory(game: Game):

    def draw_main():
        global tile_offset
        draw_tiles(game, game.screen, game.bg_tile_scaled, tile_offset)
        tile_offset += 0.5

    return draw_main