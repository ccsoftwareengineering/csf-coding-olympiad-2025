from enum import Enum
import pygame
from scenes.home import draw_home_factory
from scenes.main_scene import draw_main_factory
from structures.game import *

game = Game()
running = True
draw_home = draw_home_factory(game)
draw_main = draw_main_factory(game)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game.curr_state == game_states['home']:
        draw_home()

    if game.curr_state == game_states['main']:
        draw_main()

    pygame.display.flip()
    game.clock.tick(60)
pygame.quit()
