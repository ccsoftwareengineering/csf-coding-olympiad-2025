from typing import TYPE_CHECKING, cast

import modules.utilities as u
from modules.more_utilities.enums import Direction, GameState, HorizontalAlignment, VerticalAlignment
from modules.more_utilities.guide_helpers import igi

if TYPE_CHECKING:
    from structures.game import Game
    from scenes.main_scene import MainScene


def starting_tutorial(game: 'Game'):
    main_scene: 'MainScene' = cast(any, game.scenes[GameState.MAIN])
    f = u.expand_rect_outline(main_scene.bl_ui.rect, 5)
    print(f.size, f.left, f.top, f.right, f.bottom)
    return (
        [
            (
                ("Firstly, your yearly budget allocation. "
                 "Every year in-game you are given more money which is used for creating new plants as well as "
                 "funding the upkeep of pre-existing plants."),
                igi({},
                    u.rect_from_to((15, 550), (325, 705)), #u.rect_from_to((12, 533), (375, 705)),
                    Direction.RIGHT,
                    text_box_alignment=VerticalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.LEFT)
            ),
            (
                ("Here is where you can see the year you're currently in. "
                 "Pressing ADVANCE YEAR makes you enter the new year in-game, allowing you to see the results or "
                 "consequences of your actions in the previous year. "),
                igi({},
                    u.expand_rect_outline(main_scene.tc_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.CENTER,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                ("You will also receive your yearly budget allo"
                 "cation as well as see other metric updates.  Only press this button when you're certain you have"
                 " finished your actions for that year. You will also receive a confirmation prompt."),
                igi({},
                    u.expand_rect_outline(main_scene.tc_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.CENTER,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                ("Here is the menu in which you can adjust settings, see player information, as well as use "
                 "the create button to make campaigns, power plants, and infrastructure."),
                igi({},
                    u.expand_rect_outline(main_scene.tr_ui.rect, 5),
                    Direction.DOWN,
                    text_box_alignment=HorizontalAlignment.RIGHT,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            )
        ], {'guide': True}
    )
