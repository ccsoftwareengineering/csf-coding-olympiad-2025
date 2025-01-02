import pygame
from pygame import Surface

from modules import utilities as u
from modules.more_utilities.enums import AnchorPoint, Direction
from structures.hud.button import Button
from structures.hud.list_layout import ListLayout
from structures.scene import Scene


class MainScene(Scene):
    factor = 1
    fs = factor * 8
    country_factor = factor * 1.5
    main_surface = Surface((fs * 50, fs * 50), pygame.SRCALPHA, 32)
    country_waves = u.load_scale('assets/country_waves.png', factor=country_factor)
    country_waves.set_alpha(70)
    zoom_factor = 4

    settings_icon = u.load_scale('assets/ui/icons/settings.png', factor=2)
    info_icon = u.load_scale('assets/ui/icons/info.png', factor=2)

    def define_game_variables(self):
        tr_ui = ListLayout(
            self.game,
            anchor_point=AnchorPoint.TOP_RIGHT,
            direction=Direction.LEFT,
            position=u.relative_pos(self.game.screen.get_size(), (20, 20), from_xy='right-top')
        )

        return {
            'country': u.rescale(self.game.country_detail, factor=self.country_factor),
            'top_right_ui': tr_ui,
            'settings_button': Button(self.game, self.settings_icon, name="settings_button", parent=tr_ui),
            'info_button': Button(self.game, self.info_icon, name="info_button", parent=tr_ui),
        }

    def mouse_scroll(self, ev: pygame.event.Event):
        self.zoom_factor += ev.y * (self.zoom_factor < 0.1 and 0.1 or self.zoom_factor > 2 and 0.2 or 0.08)
        self.zoom_factor = round(u.clamp(self.zoom_factor, 0.46, 6), 2)
        self.game.telemetry_handler.set_value('zoom', self.zoom_factor)

    def draw_map(self):
        self.game.screen.fill((0, 132, 227))
        self.main_surface.fill((0, 132, 227))
        u.center_blit(self.main_surface, self.country_waves)
        u.center_blit(self.main_surface, self.g_vars['country'])
        scaled = u.rescale(self.main_surface, factor=self.zoom_factor)
        u.center_blit(self.game.screen, scaled)

    def draw_ui(self):
        top_right_ui: ListLayout = self.g_vars['top_right_ui']
        top_right_ui.draw()
        self.game.telemetry_handler.set_values({
            'tr-ui pos': top_right_ui.rect.topright,
            'tr-ui children amount': len(top_right_ui.children),
            'tr-ui settings pos': top_right_ui.children_list[0].rect.topright,
        })

    def draw(self):
        self.draw_map()
        self.draw_ui()

    def init(self):
        self.game.input_handler.subscribe('mouse_wheel', self.mouse_scroll, 'main_zoom')

    def cleanup(self):
        self.game.input_handler.unsubscribe('mouse_wheel', 'main_zoom')
