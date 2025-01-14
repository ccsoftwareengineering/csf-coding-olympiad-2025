from enum import Enum


class AnchorPoint(Enum):
    TOP_LEFT = 0
    TOP_CENTER = 1
    TOP_RIGHT = 2
    MID_LEFT = 3
    MID_CENTER = 4
    MID_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_CENTER = 7
    BOTTOM_RIGHT = 8


anchor_map: list[str] = [
    'topleft',
    'midtop',
    'topright',
    'midleft',
    'center',
    'midright',
    'bottomleft',
    'midbottom',
    'bottomright',
]


class GameState(Enum):
    HOME = 0
    MAIN = 1
    SHOP = 2
    DIALOGUE = 3
    SKIPPING = 4
    NONE = 5


class ActionState(Enum):
    NONE = 0,
    PLACING = 1,
    DESTROYING = 2,
    UPGRADING = 3,


class Direction(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3


class VerticalAlignment(Enum):
    TOP = 0,
    CENTER = 1,
    BOTTOM = 2


class HorizontalAlignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2,
