from scenes.dialogue_scene import draw_dialogue_factory
from scenes.home_scene import draw_home_factory
from scenes.main_scene import draw_main_factory
from scenes.skipping_scene import draw_skipping_factory
from structures.game import *
from structures.player import Player

game = Game(show_fps=True)
update = game.update_factory({
    'home': draw_home_factory(game),
    'dialogue': draw_dialogue_factory(game),
    'main': draw_main_factory(game),
    'skipping': draw_skipping_factory(game, 1.5)
})

# developer_player = Player(game, "<Developer>")
# game.player = developer_player

while game.running:
    update()
pygame.quit()
