import pygame
from pygame import Surface

from modules import utilities as u
from modules.constants import default_emulated_x, dims, ui_color_light, red, white, green
from modules.info.info import info_map
from modules.more_utilities.enums import AnchorPoint, Direction, HorizontalAlignment
from modules.utilities import display_number
from scenes.main_ui.money_display import MoneyDisplay
from scenes.main_ui.selector_prompt import SelectorPrompt
from structures.game import Game
from structures.hud.button import Button
from structures.hud.dropdown import Dropdown
from structures.hud.dynamic_button import DynamicButton
from structures.hud.dynamic_text_box import DynamicTextBox
from structures.hud.hud_object import HudObject
from structures.hud.list_layout import ListLayout
from structures.hud.text import Text
from structures.scene import Scene


def apply_empty_space(list_layout: ListLayout, size: tuple[int, int] = (0, 0), amount=0):
    if amount != 0:
        if list_layout.vertical:
            size = (size[0], amount)
        else:
            size = (size[1], amount)
    HudObject(list_layout.game, Surface(size, pygame.SRCALPHA), parent=list_layout)


class MainScene(Scene):
    factor = 1
    fs = factor * 8
    country_factor = factor * 1.5
    main_surface = Surface((fs * 50, fs * 50), pygame.SRCALPHA, 32)
    country_waves = u.load_scale('assets/country_waves.png', factor=country_factor)
    country_waves.set_alpha(70)
    zoom_factor = 4

    settings_icon = u.load_scale('assets/ui/icons/settings.png', factor=1.5)
    info_icon = u.load_scale('assets/ui/icons/info.png', factor=1.5)
    add_icon = u.load_scale('assets/ui/icons/add.png', factor=1.5)

    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.country = u.rescale(self.game.country_detail, factor=self.country_factor)

        self.tr_ui = ListLayout(
            self.game,
            anchor_point=AnchorPoint.TOP_RIGHT,
            direction=Direction.LEFT,
            gap=15,
            padding=13,
            side=HorizontalAlignment.LEFT,
            position=u.relative_pos(self.game.screen.get_size(), (10, 10), from_xy='right-top'),
            rect_template=u.ui_rect_template
        )

        self.tc_ui = DynamicTextBox(
            self.game,
            (300, 150),
            {"color": (255, 255, 255), "size": 32, "outline": 2, "outline_color": (0, 0, 0), "xy": (None, 20)},
            rect_template=u.ui_rect_template,
            text=f'YEAR X',
        )
        self.tc_ui.rect.midtop = u.relative_pos(dims, (0, 10), from_xy='center-top')

        self.advance = DynamicButton(
            game,
            (250, 50),
            select_cursor='NEXT',
            rect_template=u.rounded_rect_template(
                outline=1,
                emulated_x=default_emulated_x,
                color=ui_color_light,
                radius=7
            ),
            text_options={"size": 20},
            text="ADVANCE YEAR",
            parent=self.tc_ui
        )
        self.advance.rect.midbottom = u.relative_pos(self.tc_ui.size, (0, 20), from_xy='center-bottom')

        self.bl_ui = ListLayout(
            self.game,
            anchor_point=AnchorPoint.BOTTOM_LEFT,
            direction=Direction.UP,
            side=HorizontalAlignment.RIGHT,
            gap=5,
            padding=20,
            position=u.relative_pos(self.game.screen.get_size(), (20, 20), from_xy='left-bottom'),
            rect_template=u.ui_rect_template,
            max_size=(300, 10_000),
        )

        self.budget_display = Text(self.game, wrap=True, outline=1, size=15, parent=self.bl_ui, max_width=300)
        self.money_display = MoneyDisplay(game=self.game, parent=self.bl_ui, size=28)

        white_template = u.rounded_rect_template(
            color=(255, 255, 255),  # (255, 162, 112),
            emulated_x=default_emulated_x,
            outline=1,
            radius=20,
        )
        self.tr_buttons = {
            'settings_button': Button(self.game, self.settings_icon, object_id="settings_button", parent=self.tr_ui),
            'info_button': Button(self.game, self.info_icon, object_id="info_button", parent=self.tr_ui),
            'add_button': DynamicButton(
                self.game,
                (150, 50),
                {"color": (0, 0, 0), "size": 18},
                rect_template=white_template,
                text='CREATE...',
                select_cursor='ADD',
                parent=self.tr_ui,
                object_id="create_button"
            )
            # Button(self.game, self.add_icon, object_id="add_button", parent=self.tr_ui),
        }

        self.add_dropdown = Dropdown(
            game,
            (300, 300),
            button=self.tr_buttons['add_button'],
            # rect_template=self.ui_rect_template
        )

        button_dropdown_space = 10
        dbl = ListLayout(
            game,
            anchor_point=AnchorPoint.TOP_LEFT,
            direction=Direction.DOWN,
            parent=self.add_dropdown,
            side=HorizontalAlignment.RIGHT,
            position=(0, 0),
            rect_template=u.ui_rect_template,
            max_size=(300, 300),
            gap=10,
            padding=button_dropdown_space
        )
        manufacture_button = lambda text, mtype: DynamicButton(
            game,
            (300 - button_dropdown_space * 2, 38),
            text_options={"size": 18, "color": (0, 0, 0)},
            rect_template=white_template,
            text=text,
            object_id=text.lower().replace(' ', '_'),
            parent=dbl,
            attributes={"type": mtype}
        )
        self.add_dropdown_button_list = (dbl, (
            manufacture_button('Plant', 'plant'),
            # 'campaign': manufacture_button('Campaign'),
            manufacture_button('Infrastructure', 'infra'),
        ))

        for btn in self.add_dropdown_button_list[1]:
            btn.on('on_press_end', lambda b: self.create_selector_prompt(b.attributes.get('type')))

        self.selector_prompts = None

        manufacture_placement_template = lambda outline_color: u.rounded_rect_template(
            white, outline=2,
            emulate_outline=True,
            outline_color=outline_color,
            emulated_x=lambda xy: xy[0] * 4,
            behavior='in')

        self.placement_color = green
        self.placement_color = red

        # To make introduction dialogue see it
        self.tr_ui.predraw()
        self.bl_ui.predraw()
        self.tc_ui.predraw()

    def create_selector_prompt(self, which):
        self.add_dropdown.selected = False
        self.game.modal_handler.show_custom_modal(self.selector_prompts[which])

    def define_game_variables(self):
        return {}

    def mouse_scroll(self, ev: pygame.event.Event):
        self.zoom_factor += ev.y * (self.zoom_factor < 0.1 and 0.1 or self.zoom_factor > 2 and 0.2 or 0.08)
        self.zoom_factor = round(u.clamp(self.zoom_factor, 0.46, 6), 2)
        self.game.telemetry_handler.set_value('zoom', self.zoom_factor)

    def draw_map(self):
        self.game.screen.fill((0, 132, 227))
        self.main_surface.fill((0, 132, 227))
        u.center_blit(self.main_surface, self.country_waves)
        u.center_blit(self.main_surface, self.country)
        scaled = u.rescale(self.main_surface, factor=self.zoom_factor)
        u.center_blit(self.game.screen, scaled)

    def draw_ui(self):
        self.tr_ui.draw()
        self.add_dropdown.draw()
        self.bl_ui.draw()
        self.tc_ui.draw()

    def draw(self):
        if self.game.input_handler.key_on_down.get(pygame.K_ESCAPE):
            self.game.placement_info = None

        if self.game.input_handler.mouse_on_down.get(1) and self.game.placement_info is not None:
            print(f'handle placement of {
            self.game.placement_info['type'].value[0]}')
            # handle suffering here
        self.draw_map()
        if self.game.placement_info is not None:
            size = info_map[self.game.placement_info['category']][self.game.placement_info['type']]['size']
            place_surf = pygame.transform.scale_by(Surface(size, pygame.SRCALPHA), self.zoom_factor / 2)
            place_surf.fill(green)
            place_surf.set_alpha(155)
            rect = place_surf.get_rect()
            rect.center = pygame.mouse.get_pos()
            self.game.screen.blit(place_surf, rect)
        self.draw_ui()

    def init(self):
        self.game.input_handler.on('mouse_wheel', self.mouse_scroll, 'main_zoom')
        self.tc_ui.text_object.text = f'YEAR {self.game.player.year}'
        self.budget_display.text = f'Annual Budget Allocation: ${display_number(self.game.player.budget_increase)}'
        if not self.game.player.did_tutorial:
            self.game.modal_handler.show_simple_modal(
                "Since you're new, let's give you a brief rundown of how to get started!",
                "Welcome!",
                lambda: self.game.initiate_dialogue("starting_tutorial"))
        self.selector_prompts = {
            'plant': SelectorPrompt(self.game, 'plant'),
            # 'campaign': SelectorPrompt(self.game, 'campaign'),
            'infra': SelectorPrompt(self.game, 'infra'),
        }

    def cleanup(self):
        self.game.input_handler.off('mouse_wheel', 'main_zoom')
