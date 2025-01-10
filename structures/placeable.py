from pygame import Surface

import modules.utilities as u
from modules.info.infra import InfraType
from modules.info.plants import PlantType
from structures.handlers.placeable_handler import PlaceableType
from structures.hud.button import Button

image_cache = {}
rescale_cache = {}


def differenciate_type(t):
    if isinstance(t, PlantType):
        return PlaceableType.PLANT
    if isinstance(t, InfraType):
        return PlaceableType.INFRA


class Placeable:
    def __init__(self, game, name, data, placeable_type: PlantType, pos):
        self.type = placeable_type
        self.p_type = differenciate_type(placeable_type)
        self.data = data
        self.name = name
        self.pos = pos
        cache_get = image_cache.get(placeable_type) or (None, None)
        string = 'plants' if isinstance(placeable_type, PlantType) else 'infra'
        self.image = cache_get[0] or u.load_image(f'assets/{string}/{data.get('asset_id') or 'missing'}.png')
        self.ratio = cache_get[1] or data['size'][0] / self.image.get_width() * 0.5
        image_cache[placeable_type] = (self.image, self.ratio)
        self.object = Button(game, self.image, (0, 0), select_cursor='POINTER_CONFIG')

    def update_pos(self, zf):
        a = rescale_cache.get((self.type, zf)) or u.rescale(self.image, factor=self.ratio * zf)
        rescale_cache[(self.type, zf)] = a
        self.object.surface = a
        self.object.darker_surface = a
        # rescale_cache[(self.type, zf)] = self.object.surface
        self.object.rect.size = self.object.surface.get_size()

    @staticmethod
    def draw_all(plants, zoom_factor, surf: Surface, zf_better):
        for plant in plants:
            plant.update_pos(zoom_factor)
            plant.object.rect.center = u.relative_pos(surf.get_size(),
                                                      (plant.pos[0] * zf_better, plant.pos[1] * zf_better),
                                                      from_xy="center-center")
            plant.object.draw(draw_surface=surf)
