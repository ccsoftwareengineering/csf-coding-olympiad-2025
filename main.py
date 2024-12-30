from scenes.dialogue_scene import draw_dialogue_factory
from scenes.home_scene import draw_home_factory
from scenes.main_scene import draw_main_factory
from structures.game import *

game = Game()
update = game.update_factory({
    'home': draw_home_factory(game),
    'dialogue': draw_dialogue_factory(game),
    'main': draw_main_factory(game)
})

while game.running:
    update()
pygame.quit()
