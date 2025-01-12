from math import log2, inf
from typing import TYPE_CHECKING, Optional

from modules.info.plants import PlantType
from structures.handlers.placeable_handler import PlaceableManager
from structures.placeable import Placeable

if TYPE_CHECKING:
    from structures.game import Game


class Player:
    def __init__(self, game: 'Game', name: str, options: Optional[dict[str, any]] = None):
        self.game = game
        self.name = name
        self.budget = 0
        self.budget_increase = 1_000_000
        self.budget_increase_multiplier = 1
        self.approval = 3
        self.emissions = 0
        self.year = 1
        self.plants: dict[str, Placeable] = {}
        self.plants_construction_pending = {}
        self.placeable_manager = PlaceableManager(self.game)
        self.energy_requirements = 400
        self.pollution_multipliers = (
            (100, 600, inf),
            ((200, 255, 200), (255, 255, 200), (255, 200, 200)),
        )
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
        if self.approval == 5:
            self.super_popular_count += 1
        if self.super_popular_count > 3:
            self.super_popular_count = 0
            self.budget_increase_multiplier *= 1.2
            self.budget_increase_multiplier = round(self.budget_increase_multiplier, 2)
            self.budget_increase *= self.budget_increase_multiplier
        self.energy_requirements += 400 * log2(self.year)
        self.energy_requirements = round(self.energy_requirements)
        self.natural_disaster_chance *= 2
