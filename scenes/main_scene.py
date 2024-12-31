from pygame import Surface

from modules import utilities as u
import pygame
from structures.game import Game

play_button_surface = u.load_scale('assets/play_button.png', None, 1.6)


def draw_main_tiles_factory(main_surface, tile, distance):
    c = main_surface.copy()
    u.draw_tiles(c, tile, 0, distance=distance)

    def draw_main_tiles(offset: int, zoom: float):
        if zoom < 0.46:
            main_surface.fill((0, 132, 227))
        else:
            main_surface.blit(c, (offset, offset))

    return draw_main_tiles


def draw_main_factory(game: Game):
    factor = 8
    distance = 16*factor
    main_surface = Surface((64 * 50, 64 * 50))
    country = u.rescale(game.country_detail, factor=12)
    draw_tiles = draw_main_tiles_factory(main_surface, u.rescale(game.sea_tile, factor=factor), distance)
    zoom_factor = 0.46

    def mouse_scroll(ev: pygame.event.Event):
        nonlocal zoom_factor
        if game.curr_state == 'main':
            zoom_factor += ev.y * (zoom_factor < 0.1 and 0.1 or 0.04)
        zoom_factor = round(u.clamp(zoom_factor, 0.46, 0.86), 2)
        game.telemetry_handler.set_value('zoom', zoom_factor)

    game.input_handler.subscribe('mouse_wheel', mouse_scroll, 'main_zoom')

    def draw_main():
        draw_tiles(game.tile_offset, zoom_factor)
        game.tile_offset -= 1
        if game.tile_offset <= -distance:
            game.tile_offset = 0
        u.center_blit(main_surface, country)
        game.screen.fill((0, 132, 227))
        u.center_blit(game.screen, u.rescale(main_surface, factor=zoom_factor))

    return draw_main
