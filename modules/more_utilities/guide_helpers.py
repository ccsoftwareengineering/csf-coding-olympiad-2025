from typing import TYPE_CHECKING
from typing import TypedDict

import pygame

if TYPE_CHECKING:
    from structures.game import Game
from modules.more_utilities.enums import Direction, HorizontalAlignment, VerticalAlignment

alignment_conversion_table = {
    HorizontalAlignment.LEFT: VerticalAlignment.TOP,
    HorizontalAlignment.CENTER: VerticalAlignment.CENTER,
    HorizontalAlignment.RIGHT: VerticalAlignment.BOTTOM,
}


def inject_guide_info(
        opts,
        rect: pygame.Rect,
        text_placement: Direction,
        text_offset: tuple[int, int] = (0, 0),
        button_alignment: HorizontalAlignment = None,
        text_box_alignment: VerticalAlignment | HorizontalAlignment = VerticalAlignment.TOP,
        text_alignment: HorizontalAlignment = HorizontalAlignment.LEFT,
        gui_enabled: bool = False,
):
    if isinstance(text_box_alignment, HorizontalAlignment):
        text_box_alignment = alignment_conversion_table[text_box_alignment]

    opts['guide_info'] = {
        'rect': rect,
        'text_placement': text_placement,
        'text_offset': text_offset,
        'button_alignment': button_alignment,
        'text_box_alignment': text_box_alignment,
        'gui_enabled': gui_enabled,
        'text_alignment': text_alignment,
    }
    return opts


class GuideInfo(TypedDict):
    rect: pygame.Rect
    text_placement: Direction
    text_offset: tuple[int, int]
    button_alignment: HorizontalAlignment
    text_box_alignment: VerticalAlignment
    text_alignment: HorizontalAlignment
    gui_enabled: bool


def get_curr_guide_info(game: 'Game') -> GuideInfo:
    return game.curr_dialogue.curr_block[1].get("guide_info")


igi = inject_guide_info
