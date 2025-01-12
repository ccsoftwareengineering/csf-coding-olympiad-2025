from typing import TypedDict, NotRequired

from modules import utilities as u


class TextOptions(TypedDict):
    color: NotRequired[u.TupleColor]
    outline: NotRequired[int]
    outline_color: NotRequired[u.TupleColor]
    size: int
    offsets: NotRequired[tuple[int | None, int | None]]
    xy: NotRequired[tuple[int | None, int | None]]
    max_width: NotRequired[int]


class TextDefaults(TypedDict):
    color: NotRequired[u.TupleColor]
    outline: NotRequired[int]
    outline_color: NotRequired[u.TupleColor]
    offsets: NotRequired[tuple[int | None, int | None]]
    xy: NotRequired[tuple[int | None, int | None]]
    max_width: NotRequired[int]


class IconOptions(TypedDict):
    path: str
    size: NotRequired[tuple[int, int]]
    factor: NotRequired[float]
