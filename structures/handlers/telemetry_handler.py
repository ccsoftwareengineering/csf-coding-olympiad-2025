import pygame

import modules.utilities as u
import typing

if typing.TYPE_CHECKING:
    from structures.game import Game
    from structures.handlers.input_handler import InputHandler
from structures.hud.hud_object import HudObject
from structures.hud.text import Text


class TelemetryHandler:
    def __init__(self, game: 'Game', use_telemetry=False, text_size=18, enabled=False):
        self.enabled = enabled
        self.game = game
        self.use_telemetry = use_telemetry
        if use_telemetry:
            self.keys = {}
            self.window = HudObject(game, u.load_scale('assets/terminal.png', factor=3))
            self.window.rect.bottomleft = u.relative_pos(game.dims, (20, 20), from_xy="left-bottom")
            self.window_text = Text(game, text_size, parent=self.window, pos=(20, 20), color=(255, 255, 255))

    def set_value(self, key, value):
        if not self.use_telemetry:
            return
        self.keys[key] = value

    def draw_terminal(self):
        if not self.use_telemetry or not self.enabled:
            return
        text = '== DEVELOPER CONSOLE ==\n'
        for key, value in self.keys.items():
            text += f'{key}: {value}\n'
        self.window_text.text = text
        self.window.draw()

    def inject_telemetry_events(self, input_handler: 'InputHandler'):
        if not self.use_telemetry:
            return

        def on_o_press(key: int):
            nonlocal input_handler
            if key == pygame.K_o and input_handler.is_key_down(pygame.K_LCTRL):
                self.enabled = not self.enabled

        input_handler.subscribe('key_on_down', on_o_press, 'telemetry_window_enable')
