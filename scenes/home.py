import utilities as u
import pygame

from structures.button import Button
from structures.game import Game, game_states

play_button_surface = u.load_scale('assets/playbtn.png', None, 1.6)


def draw_tiles(g: Game, scr: pygame.Surface, tile: pygame.Surface, offset: int):
    width_increment = -offset
    while width_increment < g.screen.get_width() + 64:
        height_increment = -offset
        while height_increment < g.screen.get_height() + 64:
            scr.blit(tile, (width_increment, height_increment))
            height_increment = height_increment + 64
        width_increment += 64


tile_offset = 0


def draw_home_factory(game: Game):
    play_button = Button(game, u.center_blit_pos(game.screen, play_button_surface, offsets=(None, 1 / 3)),
                         play_button_surface)

    def draw_home():
        if play_button.on_press_end:
            game.curr_state = game_states['main']
        global tile_offset
        draw_tiles(game, game.screen, game.bg_tile_scaled, tile_offset)
        u.center_blit(game.screen, u.rescale(game.country_detail, factor=9), offsets=(None, 20))
        u.center_blit(game.screen, u.rescale(game.title, factor=1.3), offsets=(None, -0.6 / 3))
        tile_offset += 0.5
        play_button.draw()
        game.screen.blit(
            game.main_font.render(
                'Programmed by: Campion College Island Swallowtails',
                False,
                (20, 0, 0)),
            (10, game.dims[1] - (24 + 5))
        )

    return draw_home
