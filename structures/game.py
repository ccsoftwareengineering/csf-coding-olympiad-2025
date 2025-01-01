from enum import Enum

import pygame

from modules import utilities as u
from modules.dialogue import dialogues
from structures.global_store import GlobalStore
from structures.handlers.cursor_handler import CursorHandler
from structures.handlers.dialogue_handler import DialogueHandler
from structures.handlers.input_handler import InputHandler
from structures.handlers.loading_handler import LoadingHandler
from structures.handlers.modal_handler import ModalHandler
from structures.handlers.telemetry_handler import TelemetryHandler

pygame.init()

game_states = Enum("State", [
    ('home', 0),
    ('main', 1),
    ('shop', 2),
    ('dialogue', 3),
    ('skipping', 4)
])


class Game:
    dims = (1280, 720)
    tile_offset = 0
    screen = pygame.display.set_mode(dims)
    clock = pygame.time.Clock()
    sea_tile = u.load_scale('assets/background.png', (16, 16))
    bg_tile_scaled = u.load_scale('assets/background.png', (64, 64))
    title = u.load_scale('assets/title.png', None, 3)
    country = u.load_scale('assets/country.png', None, 2 ** 3)
    country_detail = u.load_scale('assets/country_detail.png', None, 1)
    main_font = pygame.font.Font(u.resource_path('assets/fonts/main_reg.ttf'), 16)
    panels = u.load_scale('assets/panels.png')
    globals = GlobalStore()

    curr_dialogue = None

    curr_state = None
    curr_state_draw_function = None

    on_press_start = {}
    on_press_end = {}

    running = True
    player = None

    def __init__(self, show_fps=False, default_state="home"):
        pygame.display.set_caption("Power Island")
        pygame.display.set_icon(u.load_image('assets/energy_icon.png'))
        self.show_fps = show_fps
        self.dialogues = dialogues(self)
        self.input_handler = InputHandler(self)
        self.telemetry_handler = TelemetryHandler(self, use_telemetry=True)
        self.cursor_handler = CursorHandler(self)
        self.loading_handler = LoadingHandler(self)
        self.modal_handler = ModalHandler(self)
        self.telemetry_handler.inject_telemetry_events(self.input_handler)

        self.set_state(default_state)

        pygame.mouse.set_visible(False)

    def set_state(self, state):
        self.cursor_handler.cursor = 'NORMAL'
        self.curr_state = state
        self.curr_state_draw_function = state

    white = (255, 255, 255)
    black = (0, 0, 0)

    def update_factory(self, draw_functions):
        def update():
            self.pre_loop()
            for event in pygame.event.get():
                self.handle_event(event)
            draw_functions[self.curr_state]()
            self.modal_handler.draw()
            self.loading_handler.draw()
            self.post_loop()
            pygame.display.flip()
            self.clock.tick(60)

        return update

    def initiate_dialogue(self, dialogue_id):
        self.curr_dialogue = DialogueHandler(self, dialogue_id, speed=0.018)

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
