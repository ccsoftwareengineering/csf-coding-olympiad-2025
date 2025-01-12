from typing import Optional

import modules.utilities as u
from modules.more_utilities.enums import AnchorPoint
from structures.hud.hud_object import HudObject


class Tooltip:
    def __init__(
            self,
            text_size,
            text: Optional[str] = "",
            size: Optional[tuple[int, int]] = None,
            width: Optional[int] = None,
            padding: Optional[int] = 20,
            distance: Optional[int] = 5,
            rect_template: Optional[u.RectTemplate] = u.ui_rect_template,
            target: Optional[HudObject] = None,
            anchor_point: Optional[AnchorPoint] = AnchorPoint.TOP_LEFT
    ):
        self.text_size = text_size
        self.size = size if size else (width, None)
        self.width = width
        self.padding = padding
        self.distance = distance
        self.rect_template = rect_template
        self.target = target
