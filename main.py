from enum import Enum
import pygame
from scenes.home import draw_home
from structures.game import Game

game = Game()
running = True

game_states = Enum("State", [
    ('home', 0),
    ('main', 1),
    ('shop', 2),
    ('dialogue', 3)
])

curr_state = game_states['home']

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if curr_state == game_states['home']:
        draw_home(game)

    pygame.display.flip()
    game.clock.tick(60)
pygame.quit()
