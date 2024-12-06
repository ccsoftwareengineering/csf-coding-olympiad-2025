import os
import sys

import pygame.transform
from pygame.image import load


# Magic to make files work with compilation!
def resource_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Shorthand load image function
def load_image(path):
    return load(resource_path(path))


# Calculates the x and y position necessary to blit one surface to the center of another
# surface given x and y overrides and offsets
def center_blit_pos(surf: pygame.Surface, surf2: pygame.Surface, xy=(None, None), offsets=(None, None)):
    _x = round(surf.get_width() / 2 - surf2.get_width() / 2)
    _y = round(surf.get_height() / 2 - surf2.get_height() / 2)
    if xy[0] is not None:
        _x = xy[0]
    if xy[1] is not None:
        _y = xy[1]
    if offsets[0] is not None:
        offset = offsets[0]
        if abs(offsets[0]) < 1:
            offset = round(offsets[0] * (surf.get_width() / 2))
        _x += offset
    if offsets[1] is not None:
        offset = offsets[1]
        if abs(offsets[1]) < 1:
            offset = round(offsets[1] * (surf.get_height() / 2))
        _y += offset
    return _x, _y


# Shorthand
cbp = center_blit_pos


# Does the blit of what was calculated above
def center_blit(surf: pygame.Surface, surf2: pygame.Surface, xy=(None, None), offsets=(None, None)):
    _x, _y = center_blit_pos(surf, surf2, xy, offsets)
    surf.blit(surf2, (_x, _y))


# A shorthand to load an image and rescale
def load_scale(path, size=None, factor=None):
    if not size:
        return pygame.transform.scale_by(load_image(path).convert_alpha(), factor)
    return pygame.transform.scale(load_image(path).convert_alpha(), size)


# Shorthand rescale function
def rescale(surf, size=None, factor=None):
    if size is None:
        return pygame.transform.scale_by(surf, factor)
    return pygame.transform.scale(surf, size)


# Draws the ocean tiles which are very common
def draw_tiles(g, scr: pygame.Surface, tile: pygame.Surface, offset: int):
    width_increment = -offset
    while width_increment < g.screen.get_width() + 64:
        height_increment = -offset
        while height_increment < g.screen.get_height() + 64:
            scr.blit(tile, (width_increment, height_increment))
            height_increment = height_increment + 64
        width_increment += 64
