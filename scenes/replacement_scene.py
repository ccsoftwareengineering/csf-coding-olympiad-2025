from typing import TYPE_CHECKING

from modules.constants import default_emulated_x, dims
from modules.more_utilities.enums import HorizontalAlignment, GameState
from structures.hud.dynamic_button import DynamicButton
from structures.hud.text import Text
from structures.scene import Scene

if TYPE_CHECKING:
    from structures.game import Game

import modules.utilities as u


class ReplacementScene(Scene):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.replaced = game.asset_handler(3.5)['assets/replaced.png']
        self.font = Text(
            game,
            20,
            max_width=800,
            align=HorizontalAlignment.CENTER,
            outline=2,
            outline_color=(0, 0, 0)
        )
        self.font.text = (
            "Oops! You've been replaced. What does this mean?\n\nYou've made choices which have resulted"
            " in your approval being consistently low. Ensure that your yearly energy output exceeds that of your "
            "country's energy demand! Balance this with keeping emissions low for optimum approval and use that"
            " as a measure of how well you're doing your job.")
        self.font.predraw()
        self.rendered = self.font.surface
        white_template = u.rounded_rect_template(
            color=(230, 230, 255, 230),  # (255, 162, 112),
            emulated_x=default_emulated_x,
            outline=1,
            radius=20,
        )
        self.play_again = DynamicButton(
            game,
            (300, 75),
            {"size": 24, "color": (0, 0, 0)},
            "BACK TO HOME",
            white_template
        )

        self.play_again.predraw()
        self.play_again.rect.midbottom = u.relative_pos(dims, (0, 100), from_xy="center-bottom")

    def draw(self):
        if self.play_again.on_press_end:
            self.game.player = None
            self.game.loading_handler.transition_to(GameState.HOME)
        game = self.game
        u.draw_tiles(game.screen, game.bg_tile_scaled, game.tile_offset)
        game.tile_offset += game.tile_increase
        if game.tile_offset == 64:
            game.tile_offset = 0

        u.center_blit(game.screen, self.replaced, offsets=(None, -1.2 / 3))
        u.center_blit(game.screen, self.rendered, offsets=(None, 0.5 / 4))
        self.play_again.draw()

    def init(self):
        pass

    def cleanup(self):
        pass
