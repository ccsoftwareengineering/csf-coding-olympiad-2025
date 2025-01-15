from math import log2, inf
from typing import TYPE_CHECKING, Optional

from modules.more_utilities.enums import GameState
from structures.handlers.placeable_handler import PlaceableManager
from structures.placeables.placeable import Placeable

if TYPE_CHECKING:
    from structures.game import Game

import modules.utilities as u


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
        self.initial_requirements = 600
        self.energy_requirements = self.initial_requirements
        self.pollution_multipliers = (
            (100, 600, inf),
            ((200, 255, 200), (255, 255, 200), (255, 200, 200)),
            (0.4, 0, -0.4)
        )
        self.island_name = ""
        self.introduced = False
        self.natural_disaster_chance = 1
        self.did_tutorial = False
        self.super_popular_count = 0
        self.super_unpopular_count = 0
        self.fail_count = 0

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

        self.approval += self.pollution_multipliers[2][self.placeable_manager.pollution_level]

        if self.energy_requirements > (u.mw_to_h(self.placeable_manager.total_output) / 1000):
            self.fail_count += 1
            self.approval -= (0.5 * self.fail_count)
        else:
            self.approval += 0.2

        self.approval = u.clamp(round(self.approval, 2), 0, 5)

        if round(self.approval) >= 4:
            self.super_popular_count += 1
        if self.super_popular_count > 3:
            self.super_popular_count = 0
            self.budget_increase_multiplier *= 1.2
            self.budget_increase_multiplier = round(self.budget_increase_multiplier, 2)
            self.budget_increase *= self.budget_increase_multiplier
        if round(self.approval) == 0:
            self.super_unpopular_count += 1
        else:
            self.super_unpopular_count = 0

        if self.super_unpopular_count == 3:
            self.game.modal_handler.show_simple_multi_modal((
                {
                    "title": "Approval Low!",
                    "body": "You've had low approval for 3 years straight. Two more years and you'll be [REPLACED]!"
                },
                {
                "title": "Approval Low!",
                "body": "P.S... [REPLACEMENT] is sort-of like a game over. To fix your approval, you should try to "
                    "ensure you meet the energy requirements and be more environmentally conscious!"
                }
            ))

        if self.super_unpopular_count == 4:
            self.game.modal_handler.show_simple_multi_modal((
                {
                    "title": "Approval LOW!",
                    "body": "You've had low approval for FOUR years straight. In a year if this doesn't change "
                    "you'll be [REPLACED]!"
                },
                {
                    "title": "Approval LOW!",
                    "body": "REMEMBER! [REPLACEMENT] is sort-of like a game over. You must meet energy demands and"
                            " monitor your pollution levels!"
                }
            ))

        if self.super_unpopular_count == 5:
            self.game.loading_handler.transition_to(GameState.REPLACED)

        print(log2(self.year * 0.4))
        self.energy_requirements *= (1 + 0.05)
        self.energy_requirements = round(self.energy_requirements)
        self.budget = int(self.budget)
        self.natural_disaster_chance *= 2
        for plant in self.placeable_manager.plants.values:
            self.budget -= plant.data['upkeep'] * plant.upkeep_multiplier
