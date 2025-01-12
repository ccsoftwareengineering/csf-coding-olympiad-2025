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
                ('Firstly, your yearly budget allocation. '
                 'Every year in-game you are given more money which is used for creating new plants as well as '
                 'funding the upkeep of pre-existing plants.'),
                igi({},
                    u.rect_from_to((15, 550), (325, 705)),  # u.rect_from_to((12, 533), (375, 705)),
                    Direction.RIGHT,
                    text_box_alignment=VerticalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.LEFT)
            ),
            (
                ('Here is where you can see the year you\'re currently in. '
                 'Pressing ADVANCE YEAR makes you enter the new year in-game, allowing you to see the results or '
                 'consequences of your actions in the previous year. '),
                igi({},
                    u.expand_rect_outline(main_scene.tc_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.CENTER,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                ('You will also receive your yearly budget allo'
                 'cation as well as see other metric updates.  Only press this button when you\'re certain you have'
                 ' finished your actions for that year. You will also receive a confirmation prompt.'),
                igi({},
                    u.expand_rect_outline(main_scene.tc_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.CENTER,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                ('Here is the menu in which you can adjust settings, see player information, as well as use '
                 'the create button to make campaigns, power plants, and infrastructure.'),
                igi({},
                    u.expand_rect_outline(main_scene.cr_ui.rect, 5),
                    Direction.DOWN,
                    text_box_alignment=HorizontalAlignment.RIGHT,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                'Down here is where you can see the important metrics to keep in mind whilst playing.',
                igi({},
                    u.rect_from_to((786, 559), (1275, 713)),  # u.expand_rect_outline(main_scene.br_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.TOP,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                'Firstly, your total pollution amount. This is measured in tCO2e, which means '
                '"tonnes of CO2 equivalent." This, as the name indicates, lets you know '
                'how much pollution your energy system produces. Try to keep it green!',
                igi({},
                    u.rect_from_to((786, 559), (1275, 713)),  # u.expand_rect_outline(main_scene.br_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.TOP,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                'Next, your yearly energy output. This is the combined energy output of all '
                'your current plants during the year.',
                igi({},
                    u.rect_from_to((786, 559), (1275, 713)),  # u.expand_rect_outline(main_scene.br_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.TOP,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                'If it is greater than or the same as the yearly '
                'energy requirement, that means your energy system is powerful enough to power the '
                'country!',
                igi({},
                    u.rect_from_to((786, 559), (1275, 713)),  # u.expand_rect_outline(main_scene.br_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.TOP,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                'Finally, the yearly energy requirement. This is how much energy is required yearly to meet '
                'the energy requirements of the country.',
                igi({},
                    u.rect_from_to((786, 559), (1275, 713)),  # u.expand_rect_outline(main_scene.br_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.TOP,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            ),
            (
                'It increases each year which requires your energy '
                'system to adapt whilst keeping pollution low. Doing all of these things increases your '
                'population approval.',
                igi({},
                    u.rect_from_to((786, 559), (1275, 713)),  # u.expand_rect_outline(main_scene.br_ui.rect, 5),
                    Direction.LEFT,
                    text_box_alignment=VerticalAlignment.TOP,
                    text_alignment=HorizontalAlignment.CENTER,
                    button_alignment=HorizontalAlignment.CENTER)
            )
        ], {'guide': True}
    )
