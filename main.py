from enum import Enum
import pygame
from scenes.home import draw_home_factory
from scenes.dialogue import draw_dialogue_factory
from structures.game import *

game = Game()
running = True
draw_home = draw_home_factory(game)
draw_dialogue = draw_dialogue_factory(game)

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            game.on_press_start[event.key] = True
        else:
            game.on_press_start = {}

        if event.type == pygame.KEYUP:
            game.on_press_end[event.key] = True
        else:
            game.on_press_end = {}

        if event.type == pygame.QUIT:
            running = False

    if game.curr_state == game_states['home']:
        draw_home()

    if game.curr_state == game_states['dialogue']:
        draw_dialogue()

    if game.curr_state == game_states['main']:
        game.screen.fill((129, 135, 240))
        game.screen.blit(game.main_font.render("In-Game", False, (22, 33, 240)), (10, 10))

    pygame.display.flip()
    game.clock.tick(60)
pygame.quit()
