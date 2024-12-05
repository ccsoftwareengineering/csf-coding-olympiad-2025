import utilities as u
import pygame
from structures.game import Game

play_button = u.load_scale('assets/playbtn.png', None, 1.6)


def draw_tiles(g: Game, scr: pygame.Surface, tile: pygame.Surface, offset: int):
    width_increment = -offset
    while width_increment < g.screen.get_width() + 64:
        height_increment = -offset
        while height_increment < g.screen.get_height() + 64:
            scr.blit(tile, (width_increment, height_increment))
            height_increment = height_increment + 64
        width_increment += 64


tile_offset = 0


def draw_home(g: Game):
    global tile_offset
    draw_tiles(g, g.screen, g.bg_tile_scaled, tile_offset)
    u.center_blit(g.screen, u.rescale(g.country_detail, factor=9), offsets=(None, 20))
    u.center_blit(g.screen, u.rescale(g.title, factor=1.3), offsets=(None, -0.6 / 3))
    tile_offset += 0.5
    u.center_blit(g.screen, play_button, offsets=(None, 1 / 3))
    g.screen.blit(
        g.main_font.render(
            'Programmed by: Campion College Island Swallowtails',
            False,
            (20, 0, 0)),
        (10, g.dims[1] - (24 + 5))
    )
