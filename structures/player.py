from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from structures.game import Game


class Player:
    def __init__(self, game: 'Game', name: str, options: Optional[dict[str, any]] = None):
        self.game = game
        self.name = name
        self.budget = 0
        self.budget_increase = 1_000_000
        self.popularity = 0
        self.emissions = 0
        self.plants = {}
        self.plants_construction_pending = {}
        self.island_name = ""
        self.introduced = False
        self.natural_disaster_chance = 0
        self.did_tutorial = False

        if options:
            for option, value in options.items():
                setattr(self, option, value)

        self.replenish()

    def get_plants_from_type(self):
        pass

    def replenish(self):
        self.budget += self.budget_increase
