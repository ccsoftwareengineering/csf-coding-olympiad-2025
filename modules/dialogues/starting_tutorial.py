from typing import TYPE_CHECKING, cast

import modules.utilities as u
from modules.more_utilities.enums import Direction, GameState
from modules.more_utilities.guide_helpers import igi

if TYPE_CHECKING:
    from structures.game import Game
    from scenes.main_scene import MainScene


def starting_tutorial(game: 'Game'):
    main_scene: 'MainScene' = cast(any, game.scenes[GameState.MAIN])
    return (
        [
            (
                ("Firstly, your yearly budget allocation. "
                 "Every year in-game you are given more money which is used for creating new plants as well as "
                 "Funding the upkeep of pre-existing"),
                igi({}, u.expand_rect_outline(main_scene.tr_ui.rect, 3), Direction.LEFT)
            )
        ], {'guide': True}
    )
