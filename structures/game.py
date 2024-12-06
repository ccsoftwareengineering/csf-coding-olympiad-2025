from enum import Enum

import pygame

import utilities as u
from structures.dialogue_handler import DialogueHandler

pygame.init()

game_states = Enum("State", [
    ('home', 0),
    ('main', 1),
    ('shop', 2),
    ('dialogue', 3)
])


class Game:
    dims = (1280, 720)
    tile_offset = 0
    screen = pygame.display.set_mode(dims)
    clock = pygame.time.Clock()
    bg_tile_scaled = u.load_scale('assets/background.png', (64, 64))
    title = u.load_scale('assets/title.png', None, 3)
    country = u.load_scale('assets/country.png', None, 2 ** 3)
    country_detail = u.load_scale('assets/country_detail.png', None, 1)
    main_font = pygame.font.Font(u.resource_path('assets/fonts/main_reg.ttf'), 24)

    curr_dialogue = None
    curr_state = game_states['home']

    on_press_start = {}
    on_press_end = {}

    def initiate_dialogue(self, id):
        self.curr_dialogue = DialogueHandler(id, speed=0.018)

    def __init__(self):
        pygame.display.set_caption("Power Island")
        pygame.display.set_icon(u.load_image('assets/energy_icon.png'))
