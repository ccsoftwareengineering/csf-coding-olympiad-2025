from typing import TYPE_CHECKING

import pygame

from modules.constants import white, black, ui_color_light, ui_color_dark, red
from modules.info.info import info_map
from modules.more_utilities.enums import Direction, AnchorPoint
from structures.hud.dynamic_button import DynamicButton
from structures.hud.dynamic_hud_object import DynamicHudObject
from structures.hud.dynamic_text_box import DynamicTextBox
from structures.hud.list_layout import ListLayout
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game

import modules.utilities as u


class SelectorPrompt(DynamicHudObject):
    def __init__(
            self,
            game: 'Game',
            which: str,
            # size: tuple[int, int],
            # rect_template: u.RectTemplate = None,
            # position: (int, int) = (0, 0),
            # scale: float = 1,
            # parent=None,
            # object_id=None,
            # children_enabled=True,
            **kwargs
    ):
        modal_dims = (800, 600)
        bottom_button_size = (230, 50)
        super().__init__(game, size=modal_dims, rect_template=u.ui_rect_template, **kwargs)
        self.which = which
        self.list = list(info_map[which].items())
        self.rect.topleft = u.center_blit_pos(game.screen, self.surface)
        self.selected_index = 0
        pad = 20
        m_height = modal_dims[1] - pad * 3 - bottom_button_size[1]
        self.type_list = ListLayout(
            game,
            size=(350, m_height),
            position=(pad, pad),
            direction=Direction.DOWN,
            anchor_point=AnchorPoint.TOP_LEFT,
            gap=20,
            parent=self
        )

        self.selected_template = u.rounded_rect_template(outline=0, color=ui_color_light, radius=7)
        self.unselected_template = u.rounded_rect_template(outline=0, color=(0, 0, 0, 0), radius=7)

        self.buttons = [DynamicButton(
            game,
            size=(self.type_list.min_size[0], 50),
            text_options={"size": 15, "color": ui_color_dark if self.selected_index == i else ui_color_light,
                          "xy": (pad, None)},
            rect_template=self.selected_template if self.selected_index == i else self.unselected_template,
            parent=self.type_list,
            text=f"{v[0].value[0].upper()}",
            attributes={"index": i},
            wrap=True,
            max_text_width=self.type_list.min_size[0] - pad * 2
        )
                        .on('on_press_end', self.update_selection)
                        for i, v in enumerate(self.list)]
        br_to = {"size": 18, "color": black}
        pos = u.relative_pos(modal_dims, (pad, pad), from_xy='right-bottom')
        self.select_button = DynamicButton(
            game,
            bottom_button_size,
            rect_template=u.quick_template(white),
            text_options=br_to,
            parent=self,
            text="SELECT!"
        )

        red_template = u.quick_template(red)

        self.cannot_afford = DynamicTextBox(
            game,
            bottom_button_size,
            rect_template=red_template,
            text_options=br_to,
            parent=self,
            text="CANNOT AFFORD"
        )

        self.cancel_button = DynamicButton(
            game,
            bottom_button_size,
            rect_template=red_template,
            text_options=br_to,
            parent=self,
            text="CANCEL"
        )

        self.cancel_button.on('on_press_end', lambda _: game.modal_handler.cancel_modal())
        self.cancel_button.rect.bottomleft = u.relative_pos(modal_dims, (pad, pad), from_xy='left-bottom')

        self.info_box = DynamicHudObject(
            game,
            (modal_dims[0] - self.type_list.min_size[0] - pad * 3, m_height),
            rect_template=u.quick_template(ui_color_light),
            parent=self
        )
        self.info_box.rect.topright = u.relative_pos(modal_dims, (pad, pad), from_xy='right-top')

        self.select_button.rect.bottomright = self.cannot_afford.rect.bottomright = pos

        self.description_text = Text(game, 20, None, (pad, pad), pad, self.info_box, black)

        self.change_afford_view()

    def update_selection(self, button: DynamicButton):
        self.selected_index = button.attributes.get('index')

    def change_afford_view(self):
        can_afford = self.can_afford_selected
        self.select_button.visible = can_afford
        self.cannot_afford.visible = not can_afford

    def update_type_list_look(self):
        for i in range(len(self.list)):
            button = self.buttons[i]
            selected = self.selected_index == i
            if selected:
                button.box_template = self.selected_template
                button.text_object.color = ui_color_dark
            else:
                button.box_template = self.unselected_template
                button.text_object.color = ui_color_light

    def can_afford(self, idx):
        return self.list[idx][1]['cost'] <= self.game.player.budget

    @property
    def can_afford_selected(self):
        return self.can_afford(self.selected_index)

    @property
    def selected(self):
        return self.list[self.selected_index]

    def predraw(self):
        if self.select_button.on_press_end:
            self.game.placement_info = {"category": self.which, "type": self.selected[0]}
            self.game.modal_handler.cancel_modal()
        if self.game.input_handler.key_on_down.get(pygame.K_DOWN):
            self.selected_index += 1
        elif self.game.input_handler.key_on_down.get(pygame.K_UP):
            self.selected_index -= 1
        self.selected_index = u.clamp(self.selected_index, 0, len(self.list) - 1)
        self.change_afford_view()
        self.update_type_list_look()
        selected = self.selected
        self.description_text.text = f'{
        selected[1]['description']}\n \n\nCost: ${u.display_number(selected[1]["cost"])}'
        if self.which == 'plant':
            output = selected[1]['output_mw']
            self.description_text.text += f'\nOutput: {
            u.display_number(output)} MW\nYearly Output: {u.display_wh(u.mw_to_h(output))}'
