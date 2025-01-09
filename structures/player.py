from typing import TYPE_CHECKING, Optional

from modules.info.plants import PlantType
from structures.plant import Plant

if TYPE_CHECKING:
    from structures.game import Game


class Player:
    def __init__(self, game: 'Game', name: str, options: Optional[dict[str, any]] = None):
        self.game = game
        self.name = name
        self.budget = 0
        self.budget_increase = 1_000_000
        self.budget_increase_multiplier = 1
        self.popularity = 3
        self.emissions = 0
        self.year = 1
        self.plants: dict[str, Plant] = {}
        self.plants_construction_pending = {}
        self.island_name = ""
        self.introduced = False
        self.natural_disaster_chance = 1
        self.did_tutorial = False
        self.super_popular_count = 0

        if options:
            for option, value in options.items():
                setattr(self, option, value)

        self.initial_replenish()

    def get_plants_from_type(self):
        pass

    def initial_replenish(self):
        self.budget += self.budget_increase

    def replenish(self):
        self.initial_replenish()
        self.year += 1
        if self.popularity == 5:
            self.super_popular_count += 1
        if self.super_popular_count > 3:
            self.super_popular_count = 0
            self.budget_increase_multiplier *= 1.2
            self.budget_increase_multiplier = round(self.budget_increase_multiplier, 2)
            self.budget_increase *= self.budget_increase_multiplier
        self.natural_disaster_chance *= 2
