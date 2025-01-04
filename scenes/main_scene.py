import pygame
from pygame import Surface

from modules import utilities as u
from modules.constants import default_emulated_x
from modules.more_utilities.enums import AnchorPoint, Direction, Side
from modules.utilities import display_number
from scenes.main_ui.money_display import MoneyDisplay
from structures.game import Game
from structures.hud.button import Button
from structures.hud.dynamic_button import DynamicButton
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
        self.ui_rect_template = u.rounded_rect_template(
            color=(0, 97, 183),  # (255, 162, 112),
            emulated_x=default_emulated_x,
            outline=1,
            double_bottom=True,
            radius=7
        )
        self.country = u.rescale(self.game.country_detail, factor=self.country_factor)

        self.tr_ui = ListLayout(
            self.game,
            anchor_point=AnchorPoint.TOP_RIGHT,
            direction=Direction.LEFT,
            gap=15,
            padding=13,
            position=u.relative_pos(self.game.screen.get_size(), (10, 10), from_xy='right-top'),
            rect_template=self.ui_rect_template
        )

        self.bl_ui = ListLayout(
            self.game,
            anchor_point=AnchorPoint.BOTTOM_LEFT,
            direction=Direction.UP,
            side=Side.RIGHT,
            gap=5,
            padding=20,
            position=u.relative_pos(self.game.screen.get_size(), (20, -30), from_xy='left-bottom'),
            rect_template=self.ui_rect_template,
            max_width=(350, 10_000)
        )

        apply_empty_space(self.bl_ui, amount=10)
        self.budget_display = Text(self.game, wrap=True, outline=1, size=15, parent=self.bl_ui)
        self.money_display = MoneyDisplay(game=self.game, parent=self.bl_ui, size=28)

        self.buttons = {
            'settings_button': Button(self.game, self.settings_icon, name="settings_button", parent=self.tr_ui),
            'info_button': Button(self.game, self.info_icon, name="info_button", parent=self.tr_ui),
            'add_button': DynamicButton(
                self.game,
                (120, 50),
                {"color": (0, 0, 0), "size": 18},
                box_template=u.rounded_rect_template(
                    color=(255, 255, 255),  # (255, 162, 112),
                    emulated_x=default_emulated_x,
                    outline=1,
                    radius=7
                ),
                text='ADD..',
                parent=self.tr_ui
            )
            # Button(self.game, self.add_icon, name="add_button", parent=self.tr_ui),
        }

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
        self.budget_display.text = f'Annual Budget Allocation: {display_number(self.game.player.budget_increase)}'
        self.bl_ui.draw()

    def draw(self):
        self.draw_map()
        self.draw_ui()

    def init(self):
        self.game.input_handler.subscribe('mouse_wheel', self.mouse_scroll, 'main_zoom')
        if not self.game.player.did_tutorial:
            self.game.modal_handler.show_modal(
                "Since you're new, let's give you a brief rundown of how to get started!",
                "Welcome!",
                lambda: self.game.initiate_dialogue("starting_tutorial"))

    def cleanup(self):
        self.game.input_handler.unsubscribe('mouse_wheel', 'main_zoom')
