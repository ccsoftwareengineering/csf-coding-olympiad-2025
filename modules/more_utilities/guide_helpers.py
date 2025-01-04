from typing import TypedDict

import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from structures.game import Game
from modules.more_utilities.enums import Direction


def inject_guide_info(opts, rect: pygame.Rect, text_placement: Direction):
    opts['guide_info'] = {'rect': rect, 'text_placement': text_placement}


class GuideInfo(TypedDict):
    rect: pygame.Rect
    text_placement: Direction


def get_curr_guide_info(game: 'Game') -> GuideInfo:
    return game.curr_dialogue.curr_block[1].get("guide_info")


igi = inject_guide_info
