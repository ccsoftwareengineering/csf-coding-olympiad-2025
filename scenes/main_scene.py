from modules import utilities as u
import pygame
from structures.game import Game

play_button_surface = u.load_scale('assets/play_button.png', None, 1.6)

tile_offset = 0


def draw_main_factory(game: Game):
    def draw_main():
        global tile_offset
        u.draw_tiles(game, game.screen, game.bg_tile_scaled, tile_offset)
        tile_offset += 0.5

    return draw_main
