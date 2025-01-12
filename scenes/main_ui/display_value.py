from pygame import Surface

from structures.hud.dynamic_button import create_text_from_options
from modules.more_utilities.text import TextOptions
from structures.hud.hud_object import HudObject


class DisplayValue(HudObject):
    def __init__(self, label_options: TextOptions, value_options: TextOptions, max_width=None, gap=20, **kwargs):
        super().__init__(**kwargs)
        self.max_width = max_width
        self.label = create_text_from_options(self.game, label_options)
        self.value = create_text_from_options(self.game, value_options)
        self.gap = gap

    def predraw(self):
        self.label.predraw()
        self.value.predraw()
        surf = Surface((
            self.label.surface.get_width() + self.gap + self.value.surface.get_width(),
            max(self.label.surface.get_height(), self.value.surface.get_height())
        ))
        surf.blit(self.label.surface, (0, 0))

