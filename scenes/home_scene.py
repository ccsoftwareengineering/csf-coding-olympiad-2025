from modules import utilities as u
from modules.constants import dims
from modules.more_utilities.enums import GameState
from structures.hud.button import Button
from structures.scene import Scene


class HomeScene(Scene):
    def __init__(self, g):
        self.play_button_surface = u.load_scale('assets/play_button.png', None, 1.6)
        self.programmed_by_pos = u.relative_pos(dims, (10, 10), from_xy='left-bottom')
        super().__init__(g)

    def define_game_variables(self):
        return {
            'play_button': Button(self.game, self.play_button_surface, scale=0.8,
                                  pos=u.cbp(self.game.screen, self.play_button_surface, offsets=(None, 1 / 3)),
                                  object_id="PlayButton"),
            'rescaled_country': u.rescale(self.game.country_detail, factor=9),
            'rescaled_title': u.rescale(self.game.title, factor=1.3),
            'programmed_by': self.game.main_font.render(
                'Programmed by: Campion College Island Swallowtails',
                False,
                (20, 0, 0))
        }

    def draw(self):
        game, play_button, rescaled_country, rescaled_title, programmed_by = (
            self.game, self.g_vars['play_button'], self.g_vars['rescaled_country'], self.g_vars['rescaled_title'], self.g_vars['programmed_by'])

        if play_button.on_press_end:
            if not game.player:
                game.initiate_dialogue('introduction')
                game.loading_handler.transition_to(GameState.DIALOGUE)
            else:
                game.loading_handler.transition_to(GameState.MAIN)

        u.draw_tiles(game.screen, game.bg_tile_scaled, game.tile_offset)
        u.center_blit(game.screen, rescaled_country, offsets=(None, 20))
        u.center_blit(game.screen, rescaled_title, offsets=(None, -0.6 / 3))
        game.tile_offset += 0.5
        if game.tile_offset == 64:
            game.tile_offset = 0
        play_button.draw()
        # print(len(play_button.children))
        game.screen.blit(
            programmed_by,
            (self.programmed_by_pos[0], self.programmed_by_pos[1] - programmed_by.get_height())
        )
