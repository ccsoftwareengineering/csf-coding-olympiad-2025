from scenes.home_scene import draw_home_factory
from scenes.main_scene import draw_main_factory
from scenes.dialogue_scene import draw_dialogue_factory
from structures.game import *

game = Game()
running = True
draw_home = draw_home_factory(game)
draw_dialogue = draw_dialogue_factory(game)
draw_main = draw_main_factory(game)

while running:
    game.pre_loop()
    for event in pygame.event.get():
        game.handle_event(event)
        if event.type == pygame.QUIT:
            running = False

    if game.curr_state == game_states['home']:
        draw_home()

    if game.curr_state == game_states['dialogue']:
        draw_dialogue()

    if game.curr_state == game_states['main']:
        draw_main()

    game.post_loop()
    pygame.display.flip()
    game.clock.tick(60)
pygame.quit()
