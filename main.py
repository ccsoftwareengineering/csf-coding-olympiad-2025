from enum import Enum
import pygame
from scenes.home import draw_home_factory
from structures.game import *

game = Game()
running = True
draw_home = draw_home_factory(game)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game.curr_state == game_states['home']:
        draw_home()

    if game.curr_state == game_states['main']:
        game.screen.fill((129, 135, 240))
        game.screen.blit(game.main_font.render("In-Game", False, (22, 33, 240)), (10, 10))

    pygame.display.flip()
    game.clock.tick(60)
pygame.quit()
