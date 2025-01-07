from typing import TYPE_CHECKING

from modules.constants import white, black, ui_color_light
from modules.info.infra import infra
from modules.info.plants import plants
from modules.more_utilities.enums import Direction, AnchorPoint
from structures.hud.dynamic_button import DynamicButton
from structures.hud.dynamic_hud_object import DynamicHudObject
from structures.hud.dynamic_text_box import DynamicTextBox
from structures.hud.list_layout import ListLayout

if TYPE_CHECKING:
    from structures.game import Game

import modules.utilities as u

info_map = {
    'plant': plants,
    'infra': infra,
    # 'campaign': {}
}


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
        bottom_button_size = (200, 50)
        super().__init__(game, size=modal_dims, rect_template=u.ui_rect_template, **kwargs)
        self.which = which
        self.list = list(info_map[which].items())
        self.rect.topleft = u.center_blit_pos(game.screen, self.surface)
        self.selected_index = 0
        pad = 20
        m_height = modal_dims[1] - pad * 3 - bottom_button_size[1]
        self.type_list = ListLayout(
            game,
            size=(300, m_height),
            position=(pad, pad),
            direction=Direction.DOWN,
            anchor_point=AnchorPoint.TOP_LEFT,
            gap=20,
            parent=self
        )
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

        red_template = u.quick_template((207, 58, 48))

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
        self.change_afford_view()

    def change_afford_view(self):
        can_afford = self.can_afford_selected
        self.select_button.visible = can_afford
        self.cannot_afford.visible = not can_afford

    @property
    def can_afford_selected(self):
        return self.list[self.selected_index][1]['cost'] <= self.game.player.budget

    def predraw(self):
        self.change_afford_view()
