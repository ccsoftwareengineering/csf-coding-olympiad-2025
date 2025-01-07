from typing import TYPE_CHECKING

import modules.utilities as u
from structures.hud.button import Button
from structures.hud.dynamic_hud_object import DynamicHudObject

if TYPE_CHECKING:
    from structures.game import Game


class Dropdown(DynamicHudObject):
    def __init__(
            self,
            game: 'Game',
            size: tuple[int, int],
            button: Button,
            gap: int = 20,
            rect_template: u.RectTemplate = None,
            pos: (int, int) = (0, 0),
            scale: float = 1,
            parent=None,
            object_id=None,
            children_enabled=True,
            **kwargs
    ):
        self.gap = gap
        self.button = button
        self.button.on('on_press_end', self.on_button_press)
        self._selected = False
        super().__init__(game, size, rect_template, pos, scale, parent, object_id, children_enabled)
        self.visible = False

    @property
    def selected(self):
        return self._selected

    def on_button_press(self, button):
        self.selected = self.button.enabled

    @selected.setter
    def selected(self, selected: bool):
        if self._selected == selected:
            return
        self._selected = selected
        if selected:
            self.game.input_handler.on("mouse_on_up", self.on_mouse_up, "dropdown_selection")
            self.visible = True
        else:
            self.visible = False
            self.game.input_handler.off("mouse_on_up", "dropdown_selection")
            pass

    def on_mouse_up(self, event):
        if event.button != 1:
            return
        self.selected = self.hovering and self.enabled

    def predraw(self):
        self.game.telemetry_handler.set_value('add button', (self.button.hovering, self.button.on_hover_start,
                                              self.button.on_hover_end, self.button.on_press_start,
                                              self.button.on_press_end))
        # if self.button.on_press_end and self.button.enabled:
        #     self.selected = True
        self.rect.midtop = (self.button.absolute_rect.centerx, self.button.absolute_rect.bottom + self.gap)
        super().predraw()
