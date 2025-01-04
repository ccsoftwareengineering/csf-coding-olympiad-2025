from typing import TYPE_CHECKING, cast

import modules.utilities as u
from modules.more_utilities.enums import Direction, GameState, HorizontalAlignment, VerticalAlignment
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
                 "funding the upkeep of pre-existing plants."),
                igi({},
                    u.rect_from_to((12, 533), (375, 705)),
                    Direction.RIGHT,
                    text_alignment=VerticalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.LEFT)
            )
        ], {'guide': True}
    )
