from typing import TYPE_CHECKING

from modules.info.infra import InfraType
from modules.more_utilities.enums import PlaceableType
from structures.placeables.placeable import Placeable

if TYPE_CHECKING:
    from structures.game import Game

import modules.utilities as u


class Plant(Placeable):
    def __init__(
            self,
            game: 'Game',
            name: str,
            data: dict[str, any],
            placeable_type: InfraType,
            pos: tuple[int, int]
    ):
        super().__init__(game, name, data, placeable_type, pos, PlaceableType.PLANT)

    def get_info(self):
        addition = f' (-{
        round(max(1 - self.upkeep_multiplier, 0) * 100)}% reduction)' if self.upkeep_multiplier != 1 else ''
        return (
                super().get_info() +
                f"\nOutput: {self.data['output_mw']} MW"
                f"\nYearly Output: {u.display_wh(u.mw_to_h(self.data['output_mw']))}"
                f"\nPollution: {u.display_number(self.data['pollution_tco2e'] * self.data['output_mw'])} tCO2e"
                f"\nUpkeep: ${u.display_number(int(self.data['upkeep'] * max(self.upkeep_multiplier, 0)))}{addition}"
        )