from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from structures.game import Game


class Player:
    def __init__(self, game: 'Game', name: str, options: Optional[dict[str, any]] = None):
        self.game = game
        self.name = name
        self.money = 0
        self.popularity = 0
        self.emissions = 0
        self.plants = 0
        self.island_name = ""
        self.introduced = False

        if options:
            for option, value in options.items():
                setattr(self, option, value)
