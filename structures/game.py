from enum import Enum

import pygame

import utilities as u

pygame.init()

game_states = Enum("State", [
    ('home', 0),
    ('main', 1),
    ('shop', 2),
    ('dialogue', 3)
])


class Game:
    dims = (1280, 720)
    screen = pygame.display.set_mode(dims)
    clock = pygame.time.Clock()
    bg_tile_scaled = u.load_scale('assets/background.png', (64, 64))
    title = u.load_scale('assets/title.png', None, 3)
    country = u.load_scale('assets/country.png', None, 2 ** 3)
    country_detail = u.load_scale('assets/country_detail.png', None, 1)
    main_font = pygame.font.Font(u.resource_path('assets/fonts/main_reg.ttf'), 24)

    curr_state = game_states['home']

    def __init__(self):
        pygame.display.set_caption("Power Island")
        pygame.display.set_icon(u.load_image('assets/energy_icon.png'))
