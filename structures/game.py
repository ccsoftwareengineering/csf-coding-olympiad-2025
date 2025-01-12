from enum import Enum
from typing import Optional

import pygame
import pygame._sdl2 as pg_sdl2

from modules import utilities as u
from modules.constants import dims
from modules.dialogue import dialogues
from modules.more_utilities.enums import GameState
from structures.handlers.asset_handler import AssetHandler
from structures.handlers.cursor_handler import CursorHandler
from structures.handlers.delay_handler import DelayHandler
from structures.handlers.dialogue_handler import DialogueHandler
from structures.handlers.guide_handler import GuideHandler
from structures.handlers.input_handler import InputHandler
from structures.handlers.loading_handler import LoadingHandler
from structures.handlers.modal_handler import ModalHandler
from structures.handlers.placeable_handler import PlaceableManager
from structures.handlers.telemetry_handler import TelemetryHandler
from structures.player import Player
from structures.scene import Scene
from structures.store import Store

pygame.init()


class Game:
    tile_offset = 0
    screen = pygame.display.set_mode(dims, pygame.RESIZABLE | pygame.SCALED)
    clock = pygame.time.Clock()
    sea_tile = u.load_scale('assets/background.png', (16, 16))
    bg_tile_scaled = u.load_scale('assets/background.png', (64, 64))
    title = u.load_scale('assets/title.png', None, 3)
    country = u.load_scale('assets/country.png', None, 2 ** 3)
    country_detail = u.load_scale('assets/country_detail.png', None, 1)
    main_font = u.get_main_font(16)
    panels = u.load_scale('assets/panels.png')
    window = pg_sdl2.Window.from_display_module()

    modal = u.load_scale('assets/modal.png', factor=4)
    title_modal = u.load_scale('assets/title_modal.png', factor=4)
    okay_surface = u.load_scale('assets/okay_button.png', factor=2)

    globals = Store()
    hud_object_store = Store()

    curr_dialogue = None
    in_guide = False

    curr_state = None

    on_press_start = {}
    on_press_end = {}

    running = True

    ideal_fps = 60
    tile_increase = round(0.5 / round(ideal_fps / 60), 2)

    player: Player = None
    placement_info: Optional[dict[str, any]] = None

    def __init__(self, show_fps=False):
        pygame.display.set_caption("Power Island")
        pygame.display.set_icon(u.load_image('assets/energy_icon.png'))
        self.screen.fill((0, 0, 0))
        u.center_blit(self.screen, self.title)
        self.input_handler = InputHandler(self)

        def fullscreen_keybinding(ev: pygame.event.Event):
            if ev.key == pygame.K_ESCAPE:
                self.window.set_windowed()
            elif ev.key == pygame.K_F11:
                self.screen = pygame.display.set_mode(dims, pygame.SCALED | pygame.FULLSCREEN)

        self.input_handler.on('key_on_down', fullscreen_keybinding, 'fullscreen')
        self.in_dialogue = False
        self.in_guide = False
        self.dialogues = None
        self.just_ended_modal = False
        self.delay_handler = DelayHandler(self)
        self.asset_handler = AssetHandler(self)
        self.loading_handler = LoadingHandler(self)
        self.cursor_handler = CursorHandler(self)
        self.guide_handler = GuideHandler(self)
        self.show_fps = show_fps
        self.telemetry_handler = TelemetryHandler(self, use_telemetry=True)
        self.modal_handler = ModalHandler(self)
        self.telemetry_handler.inject_telemetry_events(self.input_handler)
        self.scenes: dict[Enum, Scene] = {}
        pygame.mouse.set_visible(False)

    def set_state(self, state: Enum):
        self.cursor_handler.cursor = 'NORMAL'
        if self.curr_state:
            self.scenes[self.curr_state].cleanup()
        self.curr_state = state
        self.scenes[self.curr_state].init()

    white = (255, 255, 255)
    black = (0, 0, 0)

    def set_scenes(self, fns: dict[Enum, Scene]):
        class EmptyScene(Scene):
            def draw(self):
                pass

        self.scenes = fns
        self.scenes[GameState.NONE] = EmptyScene(self)
        self.dialogues = dialogues(self)

    def update(self):
        self.pre_loop()
        self.delay_handler.run_all()
        for event in pygame.event.get():
            self.handle_event(event)
        self.telemetry_handler.set_value('Mouse Pos', pygame.mouse.get_pos())
        self.scenes[self.curr_state].draw()
        self.modal_handler.draw()
        if self.in_guide and not self.just_ended_modal:
            self.guide_handler.draw()
        else:
            self.just_ended_modal = False
        self.loading_handler.draw()
        self.post_loop()
        pygame.display.flip()
        self.clock.tick(self.ideal_fps)

    def initiate_dialogue(self, dialogue_id):
        self.curr_dialogue = DialogueHandler(self, dialogue_id, speed=0.018)
        self.in_dialogue = True
        if self.curr_dialogue.options.get('guide'):
            self.in_guide = True

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False
        else:
            self.input_handler.handle_event(event)

    def pre_loop(self):
        pass

    def post_loop(self):
        self.telemetry_handler.draw_terminal()
        self.input_handler.update()
        if self.show_fps:
            self.screen.blit(
                self.main_font.render(f'{self.clock.get_fps():.0f} FPS', False, self.white, self.black),
                (0, 0))
        if self.input_handler.mouse_focused:
            self.cursor_handler.draw()
