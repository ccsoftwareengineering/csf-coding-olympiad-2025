import pygame
from pygame import Surface

from modules import utilities as u
from structures.scene import Scene


class MainScene(Scene):
    factor = 1
    fs = factor * 8
    country_factor = factor * 1.5
    main_surface = Surface((fs * 50, fs * 50), pygame.SRCALPHA, 32)
    country_waves = u.load_scale('assets/country_waves.png', factor=country_factor)
    country_waves.set_alpha(70)
    zoom_factor = 4

    def define_game_variables(self):
        return {
            'country': u.rescale(self.game.country_detail, factor=self.country_factor)
        }

    def mouse_scroll(self, ev: pygame.event.Event):
        self.zoom_factor += ev.y * (self.zoom_factor < 0.1 and 0.1 or self.zoom_factor > 2 and 0.2 or 0.08)
        self.zoom_factor = round(u.clamp(self.zoom_factor, 0.46, 6), 2)
        self.game.telemetry_handler.set_value('zoom', self.zoom_factor)

    def draw(self):
        self.game.screen.fill((0, 132, 227))
        self.main_surface.fill((0, 132, 227))
        u.center_blit(self.main_surface, self.country_waves)
        u.center_blit(self.main_surface, self.g_vars['country'])
        scaled = u.rescale(self.main_surface, factor=self.zoom_factor)
        u.center_blit(self.game.screen, scaled)

    def init(self):
        self.game.input_handler.subscribe('mouse_wheel', self.mouse_scroll, 'main_zoom')

    def cleanup(self):
        self.game.input_handler.unsubscribe('mouse_wheel', 'main_zoom')
