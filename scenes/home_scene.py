from modules import utilities as u

from structures.hud.button import Button
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from structures.game import Game

play_button_surface = u.load_scale('assets/play_button.png', None, 1.6)


def draw_home_factory(game: 'Game'):
    play_button = Button(game, play_button_surface, scale=0.8, pos=u.cbp(game.screen, play_button_surface, offsets=(None, 1 / 3)), name="PlayButton")

    def draw_home():
        if play_button.on_press_end:
            if not game.player:
                game.initiate_dialogue('introduction')
                game.set_state('dialogue')
            else:
                game.set_state('skipping')

        u.draw_tiles(game.screen, game.bg_tile_scaled, game.tile_offset)
        u.center_blit(game.screen, u.rescale(game.country_detail, factor=9), offsets=(None, 20))
        u.center_blit(game.screen, u.rescale(game.title, factor=1.3), offsets=(None, -0.6 / 3))
        game.tile_offset += 0.5
        if game.tile_offset == 64:
            game.tile_offset = 0
        play_button.draw()
        # print(len(play_button.children))
        game.screen.blit(
            game.main_font.render(
                'Programmed by: Campion College Island Swallowtails',
                False,
                (20, 0, 0)),
            (10, game.dims[1] - (24 + 5))
        )

    return draw_home
