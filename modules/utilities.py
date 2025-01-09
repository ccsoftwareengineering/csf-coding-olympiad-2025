import os
import sys
from random import uniform
from typing import Optional, Callable, Tuple, Literal

import pygame.transform
from pygame import Surface
from pygame.image import load

from modules.constants import dims, font_name, text_multiplier, default_emulated_x


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
        if abs(offset) < 1:
            offset = round(offset * (surf.get_width() / 2))
        _x += offset
    if offsets[1] is not None:
        offset = offsets[1]
        if abs(offset) < 1:
            offset = round(offset * (surf.get_height() / 2))
        _y += offset
    return _x, _y


# Shorthand
cbp = center_blit_pos


# Does the blit of what was calculated above
def center_blit(surf: pygame.Surface, surf2: pygame.Surface, xy=(None, None), offsets=(None, None)):
    _x, _y = center_blit_pos(surf, surf2, xy, offsets)
    surf.blit(surf2, (_x, _y))


# A shorthand to load an image and rescale
def load_scale(path, size=None, factor=1):
    if not size:
        return pygame.transform.scale_by(load_image(path).convert_alpha(), factor)
    return pygame.transform.scale(load_image(path).convert_alpha(), size)


# Shorthand rescale function
def rescale(surf, size=None, factor=None):
    if size is None:
        return pygame.transform.scale_by(surf, factor)
    return pygame.transform.scale(surf, size)


# Draws the ocean tiles which are very common
def draw_tiles(scr: pygame.Surface, tile: pygame.Surface, offset: int, distance=64):
    width_increment = -offset
    while width_increment < scr.get_width() + distance:
        height_increment = -offset
        while height_increment < scr.get_height() + distance:
            scr.blit(tile, (width_increment, height_increment))
            height_increment = height_increment + distance
        width_increment += distance


# Allows for relative positions based on screen width
# E.g. relative_pos( (100, 100), (10, 10), from_xy="right-bottom" )
# Returns (90, 90) because it is 10 from the right and 10 from the bottom
def relative_pos(screen_size: (int, int), xy: (int, int) = (0, 0), pu: (int, int) = None, from_x="left", from_y="top",
                 from_xy: str = None):
    x = xy[0]
    y = xy[1]
    if pu is not None:
        x = pu[0] and pu[0] * screen_size[0]
        y = pu[1] and pu[1] * screen_size[1]
    x_offset = 0
    y_offset = 0
    if from_xy is not None:
        a = from_xy.split('-')
        from_x = a[0]
        from_y = a[1]
    if from_x == "center":
        x_offset = screen_size[0] / 2
    elif from_x == "right":
        x = -x
        x_offset = screen_size[0]

    if from_y == "center":
        y_offset = screen_size[1] / 2
    elif from_y == "bottom":
        y = -y
        y_offset = screen_size[1]

    return x + x_offset, y + y_offset


def round_div(a, b):
    return int(round(a / b))


# Generates a rounded rectangle with an outline (optionally)
# You may see parameters talking about "emulated"
# Emulated is simply saying what should it's resolution be
# Because sometimes even though it's drawing on the big screen you want it to still look pixelated to maintain the look
# So when it "emulates" an x it actually creates a rectangle of that width x and scales it up to the expected xy
# (first param). The emulated outline boolean is if it should divide the outline by the scale factor (x / emulated_x)
# Similar concept for emulated radius
def rounded_rect(
        xy: tuple[int, int],
        color=(255, 255, 255),
        emulated_x=None,
        radius: int = 0,
        outline: int = 0,
        outline_color=(0, 0, 0),
        emulate_outline=False,
        emulate_radius=False,
        double_bottom=False,
        behavior: Literal['out', 'in'] = 'in'
):
    # Make emulated x just the x if you don't want a pixelated look
    if not emulated_x:
        emulated_x = xy[0]

    scale = xy[0] / emulated_x
    scaled_xy = (emulated_x, round_div(xy[1], scale)) if xy[0] != xy[1] else (emulated_x, emulated_x)

    scaled_outline = round_div(outline, scale) if emulate_outline else outline
    scaled_outline_2x = scaled_outline * 2
    scaled_radius = round_div(radius, scale) if emulate_radius else radius

    # print(scaled_outline, scaled_outline_2x, radius)

    change = (1 if double_bottom else 0)

    surf = None
    if behavior == 'out':
        surf = Surface((scaled_xy[0] + scaled_outline_2x, scaled_xy[1] + scaled_outline_2x + change),
                       pygame.SRCALPHA)
        size: pygame.Rect = surf.get_rect().copy()
        size.size = (size.w, size.h - change)
        pygame.draw.rect(surf, outline_color, size, border_radius=scaled_radius)
        size.top += change
        pygame.draw.rect(surf, outline_color, size, border_radius=scaled_radius)
        pygame.draw.rect(surf, color, (scaled_outline, scaled_outline, scaled_xy[0], scaled_xy[1]),
                         border_radius=scaled_radius)
    elif behavior == 'in':
        surf = Surface((scaled_xy[0], scaled_xy[1]),
                       pygame.SRCALPHA)
        size: pygame.Rect = surf.get_rect().copy()
        pygame.draw.rect(surf, outline_color, size, border_radius=radius)
        size.size = (
            size.w - scaled_outline_2x,  # - (1 if scaled_xy[0] - size.w - scaled_outline_2x == 0 else 0),
            size.h - scaled_outline_2x)  # - (1 if scaled_xy[1] - size.h - scaled_outline_2x == 0 else 0) - change)
        size.topleft = (scaled_outline, scaled_outline)
        pygame.draw.rect(surf, color, size, border_radius=radius)
    if scale == 1:
        return surf
    return pygame.transform.scale(surf, (xy[0], xy[1]))


type RectTemplate = Callable[[Tuple[int, int]], pygame.Surface]


def rounded_rect_template(color=(255, 255, 255),
                          emulated_x: Optional[Callable] = default_emulated_x,
                          radius=0,
                          outline=0,
                          outline_color=(0, 0, 0),
                          emulate_outline=False,
                          emulate_radius=False,
                          double_bottom=False,
                          behavior: Literal['out'] | Literal['in'] = 'in') -> RectTemplate:
    return lambda xy: rounded_rect(xy, color, emulated_x(xy), radius, outline, outline_color, emulate_outline,
                                   emulate_radius, double_bottom, behavior=behavior)


def quick_template(color, radius=7, dark=False):
    return rounded_rect_template(
        color,
        emulated_x=default_emulated_x,
        radius=radius,
        outline=1,
        outline_color=(255, 255, 255) if dark else (0, 0, 0),
    )


# if a pos (x, y) is in a rect
def pos_in_rect(xy: (int, int), rect: pygame.Rect):
    return rect.left < xy[0] < rect.right and rect.top < xy[1] < rect.bottom


text_cache = {}
path = f'assets/fonts/{font_name}'


def get_main_font(size: int) -> pygame.font.Font:
    return text_cache.get(round(size * text_multiplier)) or pygame.font.Font(resource_path(path),
                                                                             round(size * text_multiplier))


def fix_color(color):
    if len(color) < 4:
        return (color[0], color[1], color[2], 255)
    else:
        return color


def lerp_colors(color1, color2, t) -> (int, int, int, int):
    color1 = fix_color(color1)
    color2 = fix_color(color2)
    r = round(color1[0] + (color2[0] - color1[0]) * t)
    g = round(color1[1] + (color2[1] - color1[1]) * t)
    b = round(color1[2] + (color2[2] - color1[2]) * t)
    a = round(color1[3] + (color2[3] - color1[3]) * t)
    return r, g, b, a


def clamp(num: float, lower: float, upper: float):
    return max(lower, min(num, upper))


def empty():
    pass


def comma_adder(amount: float | int):
    return f"{amount:,}"


units = ('K', 'M', 'B', 'T', 'Qd', 'Qt', 'Sx', 'Sp', 'Oc', 'Nt', 'Dc',)


def display_number(amount: float | int):
    return comma_adder(amount)
    # if amount < 1000:
    #     return str(amount)
    # unit_index = 0
    # while amount >= 1000 and unit_index < len(units) - 1:
    #     amount /= 1000
    #     unit_index += 1
    # if amount.is_integer():
    #     return f"{int(amount)}{units[unit_index]}"
    # else:
    #     return f"{amount:.1f}{units[unit_index]}"


type TupleColor = tuple[int, int, int] | tuple[int, int, int, int]


def rect_factory(pos: tuple[int, int], size: tuple[int, int], from_xy='left-top') -> pygame.Rect:
    left, top = relative_pos(dims, pos, from_xy=from_xy)
    return pygame.Rect(left, top, size[0], size[1])


def expand_rect_outline(r: pygame.Rect, outline: int = 0) -> pygame.Rect:
    a: pygame.Rect = r.copy()
    a.left -= outline
    a.top -= outline
    a.size = (a.width + outline * 2, a.height + outline * 2)
    return a


def rect_from_to(pos1: tuple[int, int], pos2: tuple[int, int]) -> pygame.Rect:
    size = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    return pygame.Rect(pos1[0], pos1[1], size[0], size[1])


ui_rect_template = rounded_rect_template(
    color=(0, 97, 183),  # (255, 162, 112),
    emulated_x=default_emulated_x,
    outline=1,
    double_bottom=True,
    radius=7
)


def mw_to_h(megawatts: int):
    return megawatts * 8760


def display_wh(mw_hours: int):
    if mw_hours < 1000:
        return f'{mw_hours:,.0f} MWh'
    else:
        rd = round(mw_hours / 1000, 2)
        return f'{display_number(rd)} GWh'


def get_distance_from_centre(outer_dims: tuple[int, int], pos: tuple[int, int]) -> tuple[int, int]:
    center_x = outer_dims[0] // 2
    center_y = outer_dims[1] // 2
    return pos[0] - center_x, pos[1] - center_y


def scale_vec2(vec2, v):
    return vec2[0] * v, vec2[1] * v


def percentage_chance(self, percent):
    random_number = uniform(0, 100)
    return random_number < percent
