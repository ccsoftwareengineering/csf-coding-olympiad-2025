from pygame import Rect

import modules.utilities as u
from modules.more_utilities.enums import Direction
from modules.more_utilities.guide_helpers import inject_guide_info

starting_tutorial = lambda game: (
    [
        (
            ("Firstly, your yearly budget allocation. "
             "Every year in-game you are given more money which is used for creating new plants as well as "
             "Funding the upkeep of pre-existing"),
            inject_guide_info({}, u.rect_factory((990, 5), (290, 85), 'left-top'), Direction.LEFT)
        )
    ], {'guide': True}
)
