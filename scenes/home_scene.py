from modules import utilities as u
from modules.more_utilities.enums import GameState
from structures.hud.button import Button
from structures.scene import Scene


class HomeScene(Scene):
    play_button_surface = u.load_scale('assets/play_button.png', None, 1.6)

    def define_game_variables(self):
        return {
            'play_button': Button(self.game, self.play_button_surface, scale=0.8,
                                  pos=u.cbp(self.game.screen, self.play_button_surface, offsets=(None, 1 / 3)),
                                  name="PlayButton"),
            'rescaled_country': u.rescale(self.game.country_detail, factor=9),
            'rescaled_title': u.rescale(self.game.title, factor=1.3)
        }

    def draw(self):
        game, play_button, rescaled_country, rescaled_title = (
            self.game, self.g_vars['play_button'], self.g_vars['rescaled_country'], self.g_vars['rescaled_title'])

        if play_button.on_press_end:
            if not game.player:
                game.initiate_dialogue('introduction')
                game.set_state(GameState.DIALOGUE)
            else:
                game.loading_handler.transition_to(GameState.MAIN)
            return

        u.draw_tiles(game.screen, game.bg_tile_scaled, game.tile_offset)
        u.center_blit(game.screen, rescaled_country, offsets=(None, 20))
        u.center_blit(game.screen, rescaled_title, offsets=(None, -0.6 / 3))
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
