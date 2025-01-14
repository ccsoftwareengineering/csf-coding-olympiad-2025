# import datetime
# import random
# import string
from enum import Enum
from typing import cast

import pygame
from pygame import Surface

from modules import utilities as u
from modules.constants import default_emulated_x, dims, ui_color_light, red, green, center_dims
from modules.info.info import info_map
from modules.info.infra import InfraType
from modules.info.plants import PlantType
from modules.more_utilities.enums import AnchorPoint, Direction, HorizontalAlignment, ActionState
from modules.utilities import display_number
from scenes.main_ui.icon_value import IconValue
from scenes.main_ui.money_display import MoneyDisplay
from scenes.main_ui.selector_prompt import SelectorPrompt
from structures.game import Game
from structures.handlers.placeable_handler import PlaceableManager
from structures.hud.button import Button
from structures.hud.dropdown import Dropdown
from structures.hud.dynamic_button import DynamicButton
from structures.hud.dynamic_text_box import DynamicTextBox
from structures.hud.hud_object import HudObject
from structures.hud.list_layout import ListLayout
from structures.hud.text import Text
from structures.placeable import Placeable, differenciate_type
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
    initial_zoom_factor = 4
    zoom_factor = initial_zoom_factor

    settings_icon = u.load_scale('assets/ui/icons/settings.png', factor=1.5)
    info_icon = u.load_scale('assets/ui/icons/info.png', factor=1.5)
    add_icon = u.load_scale('assets/ui/icons/add.png', factor=1.5)

    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.country = u.rescale(self.game.country_detail, factor=self.country_factor)

        self.cr_ui = ListLayout(
            self.game,
            anchor_point=AnchorPoint.TOP_LEFT,
            direction=Direction.DOWN,
            gap=15,
            padding=13,
            side=HorizontalAlignment.RIGHT,
            position=u.relative_pos(self.game.screen.get_size(), (10, 10), from_xy='right-top'),
            rect_template=u.ui_rect_template
        )

        self.tc_ui = DynamicTextBox(
            self.game,
            (300, 140),
            {"color": (255, 255, 255), "size": 32, "outline": 0, "outline_color": (0, 0, 0), "xy": (None, 20)},
            rect_template=u.ui_rect_template,
            text=f'YEAR X',
        )
        self.tc_ui.rect.topright = u.relative_pos(dims, (10, 10), from_xy='right-top')

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

        self.tl_ui = ListLayout(
            self.game,
            anchor_point=AnchorPoint.TOP_LEFT,
            direction=Direction.DOWN,
            side=HorizontalAlignment.RIGHT,
            gap=5,
            padding=20,
            position=u.relative_pos(dims, (20, 20), from_xy='left-top'),
            rect_template=u.ui_rect_template,
            min_size=(300, 140),
            max_size=(10_000, 140)
        )

        self.money_display = MoneyDisplay(game=self.game, parent=self.tl_ui, size=28)
        self.budget_display = Text(self.game, wrap=True, outline=0, size=15, parent=self.tl_ui, max_width=300)

        white_template = u.rounded_rect_template(
            color=(255, 255, 255),  # (255, 162, 112),
            emulated_x=default_emulated_x,
            outline=1,
            radius=20,
        )
        manufacture_icon_button = lambda icon, object_id=None: Button(
            self.game,
            game.asset_handler(1.8, 'assets/ui/icons/')[icon + '.png'],
            object_id=object_id or f'{icon}_button',
            parent=self.cr_ui
        )

        # DynamicButton(
        #     self.game,
        #     (150, 50),
        #     {"color": (0, 0, 0), "size": 18},
        #     rect_template=white_template,
        #     text='CREATE...',
        #     select_cursor='ADD',
        #     parent=self.cr_ui,
        #     object_id="create_button"
        # )

        self.cr_buttons = {
            'add_button': manufacture_icon_button('add'),
            'trash_button': manufacture_icon_button('trash'),
            'wrench_button': manufacture_icon_button('wrench'),
            'info_button': manufacture_icon_button('info'),
            'settings_button': manufacture_icon_button('settings'),
            # Button(self.game, self.add_icon, object_id="add_button", parent=self.cr_ui),
        }

        self.add_dropdown = Dropdown(
            game,
            (300, 108),
            button=self.cr_buttons['add_button'],
            direction=Direction.LEFT
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

        dbl.predraw()
        dbl.rect.midright = u.relative_pos(self.add_dropdown.size, (0, 0), from_xy='right-center')

        self.br_ui = ListLayout(
            game,
            direction=Direction.RIGHT,
            x_padding=20,
            y_padding=30,
            anchor_point=AnchorPoint.TOP_LEFT,
            position=(0, 0),
            rect_template=u.ui_rect_template,
            gap=50,
        )

        game.globals['approval_icons'] = game.asset_handler(1, 'assets/opinion/').load((
            '1.png',
            '2.png',
            '3.png',
            '4.png',
            '5.png'
        ))
        br_scale = 1.8
        self.approval_upsized = tuple(u.rescale(surf, factor=br_scale) for surf in game.globals['approval_icons'])
        self.br_icons = game.asset_handler(br_scale, 'assets/').load((
            'bulb_small.png',
            'energy.png',
            'earth_small.png'
        ))
        manufacture_metric = lambda i: IconValue(game, {"size": 20}, i, parent=self.br_ui)

        self.br_ui_elements = {
            'demand': manufacture_metric(self.br_icons[0]),
            'output': manufacture_metric(self.br_icons[1]),
            'approval': manufacture_metric(self.approval_upsized[2]),
            'pollution': manufacture_metric(self.br_icons[2]),
        }

        for btn in self.add_dropdown_button_list[1]:
            btn.on('on_press_end', lambda b: self.create_selector_prompt(b.attributes.get('type')))

        self.selector_prompts = None

        # manufacture_placement_template = lambda outline_color: u.rounded_rect_template(
        #     white, outline=2,
        #     emulate_outline=True,
        #     outline_color=outline_color,
        #     emulated_x=lambda xy: xy[0] * 4,
        #     behavior='in')

        self.placement_color = green
        self.can_place_color = green
        self.cant_place_color = red
        self.can_place = True
        self.placement_data: None | tuple[Enum, dict[str, any]] = None

        # To make introduction dialogue see it

        self.cr_ui.predraw()
        self.cr_ui.rect.midright = u.relative_pos(dims, (20, 0), from_xy='right-center')
        self.tl_ui.predraw()
        self.tc_ui.predraw()
        self.br_ui.predraw()

        self.game.globals['br'] = u.relative_pos(dims, (20, 20), from_xy='right-bottom')

        # this for random generation of thingy to test placement :)
        # self.gap = 0.1
        # self.og = datetime.datetime.now()
        self.map_cache = {}
        self.country_mask = {
            "mask": pygame.mask.from_surface(self.country),
            "rect": self.country.get_rect(center=center_dims)
        }

        self.game.observable_handler['action_state'].on('change', self.action_state_change, 'main_watch')

    def action_state_change(self, new: ActionState, old: ActionState):
        if old == ActionState.PLACING:
            self.game.input_handler.off('mouse_on_up', 'main_click')
        if new == ActionState.PLACING:
            self.game.input_handler.on('mouse_on_up', self.placement_click, 'main_click')

    @property
    def pm(self) -> 'PlaceableManager':
        return self.game.player.placeable_manager

    def draw(self):
        if pygame.K_o in self.game.input_handler.key_down:
            self.update_zoom_factor(0.5)
        elif pygame.K_i in self.game.input_handler.key_down:
            self.update_zoom_factor(-0.5)
        # if self.game.placement_info is not None:
        #     self.game.input_handler.on('mouse_on_up', self.placement_click, 'main_click')
        # else:
        #     self.game.input_handler.off('mouse_on_up', 'main_click')
        if self.game.input_handler.key_on_down.get(pygame.K_ESCAPE):
            self.game.observable_handler['action_state'] = ActionState.NONE
            # self.game.player.plants
        self.draw_map()
        self.draw_placement()
        self.draw_ui()

    def create_selector_prompt(self, which):
        self.add_dropdown.selected = False
        self.game.modal_handler.show_custom_modal(self.selector_prompts[which])

    def define_game_variables(self):
        return {}

    @property
    def fixed_zoom_factor(self):
        return self.zoom_factor / self.initial_zoom_factor

    def update_zoom_factor(self, multiplier):
        self.zoom_factor += multiplier * (self.zoom_factor < 0.1 and 0.1 or self.zoom_factor > 2 and 0.2 or 0.08)
        self.zoom_factor = round(u.clamp(self.zoom_factor, 0.46, 8), 2)
        self.game.telemetry_handler.set_value('zoom', self.zoom_factor)
        self.game.telemetry_handler.set_value('fixed zoom', self.fixed_zoom_factor)
        self.game.telemetry_handler.set_value('inverted fixed zoom', round(1 / self.fixed_zoom_factor, 2))

    def mouse_scroll(self, ev: pygame.event.Event):
        self.update_zoom_factor(ev.y)

    def draw_map(self):
        cached = self.map_cache.get(self.zoom_factor)
        if not cached:
            self.game.screen.fill((0, 132, 227))
            self.main_surface.fill((0, 132, 227))
            u.center_blit(self.main_surface, self.country_waves)
            u.center_blit(self.main_surface, self.country)
            scaled = u.rescale(self.main_surface, factor=self.zoom_factor)
            u.center_blit(self.game.screen, scaled)
            self.map_cache[self.zoom_factor] = self.game.screen.copy()
        else:
            self.game.screen.blit(cached, (0, 0))
        self.pm.draw_all(self.zoom_factor, self.game.screen, self.fixed_zoom_factor)

    def draw_ui(self):
        self.br_ui_elements['demand'].text_object.text = f'{
        u.display_number(self.game.player.energy_requirements)} GWh'
        self.br_ui_elements['output'].text_object.text = f'{u.display_wh(u.mw_to_h(self.pm.total_output))}'
        self.br_ui_elements['output'].text_object.color = (200, 255, 200) if u.mw_to_h(
            self.pm.total_output) / 1000 >= self.game.player.energy_requirements else (255, 200, 200)
        self.br_ui_elements['pollution'].text_object.color = self.game.player.pollution_multipliers[1][
            self.pm.pollution_level
        ]
        self.br_ui_elements[
            'pollution'].text_object.text = f'{u.display_number(self.pm.total_pollution)} tCO2e'
        self.br_ui_elements['approval'].text_object.text = f'{round(self.game.player.approval * 20)}%'
        self.br_ui_elements['approval'].text_object.color = u.lerp_colors(
            (255, 150, 150),
            (150, 255, 150),
            self.game.player.approval / 5
        )
        self.br_ui.rect.midbottom = u.relative_pos(dims, (0, 20), from_xy='center-bottom')
        self.br_ui.draw()
        self.cr_ui.draw()
        self.add_dropdown.draw()
        self.tl_ui.draw()
        self.tc_ui.draw()

    def create(self, name, pos: tuple[int, int]):
        placeable = Placeable(
            self.game,
            name,
            self.placement_data[1],
            cast(PlantType | InfraType, self.placement_data[0]),
            pos
        )
        print(self.placement_data[0])
        added = self.pm.add_placeable(placeable)
        if not added:
            self.game.modal_handler.show_simple_modal('A plant with that name already exists! '
                                                      'Please rename the pre-existing one or choose another name.')
            self.game.player.budget += self.placement_data[1]['cost']
            return
        # self.game.player.plants[name] = Placeable(self.game, name, self.placement_data[1],
        #                                           cast(PlantType, self.placement_data[0]),
        #                                           position)
        print(f'Creating {name} of type {self.placement_data[0].value[0]}')

    def placement_click(self, event: pygame.event.Event):
        if event.button != 1 or not self.can_place:
            return
        t_pos = u.div_vec2(u.get_distance_from_centre(dims, pygame.mouse.get_pos()), self.fixed_zoom_factor)
        if self.game.placement_info is not None:
            # if self.game.placement_info['type'] != InfraType.TRANSMISSION_LINE
            self.placement_data = (self.game.placement_info['type'],
                                   info_map[self.game.placement_info['category']][self.game.placement_info['type']])
            self.game.placement_info = None
            self.game.observable_handler['action_state'] = ActionState.NONE
            self.game.player.budget -= self.placement_data[1]['cost']
            print('showing placement modal')
            self.game.modal_handler.show_simple_modal(
                'What do you want to name it?',
                f'Creation',
                on_close=lambda: self.create(self.game.modal_handler.input_box.data, t_pos),
                input_visible=True)

    def draw_placement(self):
        if self.game.observable_handler['action_state'].value == ActionState.PLACING:
            which = self.country_waves if self.game.placement_info['type'] == PlantType.WIND else self.country
            rescaled_country = u.rescale(which, factor=self.zoom_factor)
            self.country_mask = {
                "mask": pygame.mask.from_surface(rescaled_country),
                "rect": rescaled_country.get_rect(center=center_dims)
            }
            size = info_map[self.game.placement_info['category']][self.game.placement_info['type']]['size']
            place_surf = pygame.transform.scale_by(Surface(size, pygame.SRCALPHA), self.zoom_factor / 2)
            rect = place_surf.get_rect()
            rect.center = pygame.mouse.get_pos()
            # if rect
            self.can_place = not self.pm.is_colliding(
                rect,
                self.game.placement_info['type'],
                differenciate_type(self.game.placement_info['type'])
            ) and PlaceableManager.in_country(
                self.country_mask['mask'],
                self.country_mask['rect'],
                rect
            )
            self.placement_color = self.can_place_color if self.can_place else self.cant_place_color
            place_surf.fill(self.placement_color)
            place_surf.set_alpha(155)
            self.game.screen.blit(place_surf, rect)

    def init(self):
        self.game.input_handler.on('mouse_wheel', self.mouse_scroll, 'main_zoom')

        self.cr_buttons['info_button'].on('on_press_end', lambda _: self.game.modal_handler.show_simple_modal(
            f'Player Name: {self.game.player.name}\n'
            f'Island Name: {self.game.player.island_name}\n'
            f'No. of Plants: {self.pm.plants.size}\n'
            f'No. of Infra: 0\n'
            'v0.0.0-alpha',
            title="Info"
        ))

        def on_advance(_):
            self.game.player.replenish()
            self.tc_ui.text_object.text = f'YEAR {self.game.player.year}'

        self.advance.on('on_press_end', on_advance, 'replenish')
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
        self.game.input_handler.off('mouse_on_up', 'main_click')
