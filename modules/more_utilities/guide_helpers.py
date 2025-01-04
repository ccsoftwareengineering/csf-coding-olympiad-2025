import pygame
from structures.game import Game
from modules.more_utilities.enums import Direction


def inject_guide_info(opts, rect: pygame.Rect, text_placement: Direction):
    opts['guide_info'] = {'rect': rect, 'text_placement': text_placement}


def get_curr_guide_rect(game: 'Game'):
    return game.curr_dialogue.curr_block[1].get("rect")


igi = inject_guide_info
