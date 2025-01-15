from typing import TYPE_CHECKING

import pygame
from pygame import Surface

from modules.info.infra import InfraType
from modules.more_utilities.enums import PlaceableType
from structures.placeables.placeable import Placeable

if TYPE_CHECKING:
    from structures.game import Game


class Infra(Placeable):
    def __init__(
            self,
            game: 'Game',
            name: str,
            data: dict[str, any],
            placeable_type: InfraType,
            pos: tuple[int, int]
    ):
        super().__init__(game, name, data, placeable_type, pos, PlaceableType.INFRA)
        if placeable_type == InfraType.MAINTENANCE_CENTER:
            rad = data['radius']
            scale = 32
            circ_surf = Surface((scale, scale), pygame.SRCALPHA)
            pygame.draw.circle(circ_surf, (255, 0, 0), (scale // 2, scale // 2), scale // 2)
            circ_surf = pygame.transform.scale(circ_surf, (rad * 2, rad * 2))
            circ_surf.set_alpha(70)
            self.predraw_surf = circ_surf

    def get_info(self):
        if self.type == InfraType.MAINTENANCE_CENTER:
            return (super().get_info() +
                    f'\nUpkeep Reduction: {round(self.data['upkeep_reduction'] * 100)}%')
