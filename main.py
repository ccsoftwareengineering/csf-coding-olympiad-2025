from scenes.dialogue_scene import DialogueScene
from scenes.home_scene import HomeScene
from scenes.main_scene import MainScene
from structures.game import *
from structures.player import Player

game = Game(show_fps=False)
game.set_scenes({
    GameState.HOME: HomeScene(game),
    GameState.DIALOGUE: DialogueScene(game),
    GameState.MAIN: MainScene(game),
})
game.set_state(GameState.HOME)

# developer_player = Player(game, "<Developer>")
# game.player = developer_player

while game.running:
    game.update()
pygame.quit()
