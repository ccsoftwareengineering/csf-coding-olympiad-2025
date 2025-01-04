import pygame

from modules.more_utilities.enums import Direction


def inject_guide_info(opts, rect: pygame.Rect, text_placement: Direction):
    opts['guide_info'] = {'rect': rect, 'text_placement': text_placement}


igi = inject_guide_info
