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


class Direction(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3


class Side(Enum):
    LEFT = 0
    RIGHT = 1,


class PlantType(Enum):
    FOSSIL_FUEL = 'fossil fuel power station',
    SOLAR = 'solar power plant',
    WIND = 'wind farm',
    GEOTHERMAL = 'geothermal power plant',
    HYDROPOWER = 'hydroelectric power plant',
    NUCLEAR = 'nuclear power plant',

