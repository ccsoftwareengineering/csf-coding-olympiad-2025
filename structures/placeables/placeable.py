import modules.utilities as u
from modules.info.infra import InfraType
from modules.info.plants import PlantType
from structures.hud.button import Button
from structures.store import Store

image_cache = {}
rescale_cache = {}


class Placeable:
    def __init__(self, game, name, data, placeable_type: PlantType | InfraType, pos, p_type):
        self.game = game
        self.type = placeable_type
        self.p_type = p_type
        self.data = data
        self.name = name
        self.pos = pos
        cache_get = image_cache.get(placeable_type) or (None, None)
        string = 'plants' if isinstance(placeable_type, PlantType) else 'infra'
        self.image = cache_get[0] or u.load_image(f'assets/{string}/{data.get('asset_id') or 'missing'}.png')
        self.ratio = cache_get[1] or data['size'][0] / self.image.get_width() * 0.5
        image_cache[placeable_type] = (self.image, self.ratio)
        self.object = Button(game, self.image, (0, 0), select_cursor='POINTER_CONFIG')
        self.predraw_surf = None
        self.attributes = Store()

        self.effectors = set()
        self.upkeep_multiplier = 1.0

    def update_pos(self, zf):
        a = rescale_cache.get((self.type, zf)) or u.rescale(self.image, factor=self.ratio * zf)
        rescale_cache[(self.type, zf)] = a
        self.object.surface = a
        self.object.darker_surface = a
        # rescale_cache[(self.type, zf)] = self.object.surface
        self.object.rect.size = self.object.surface.get_size()

    def get_info(self):
        return f'Type: {self.type.value[0].title()}'

    def add_effector(self, placeable: 'Placeable'):
        self.effectors.add(placeable)
        self.update_values()

    def remove_effector(self, placeable: 'Placeable'):
        self.effectors.discard(placeable)
        self.update_values()

    def update_values(self):
        ukm = 1
        for effector in self.effectors:
            if effector.type == InfraType.MAINTENANCE_CENTER:
                ukm -= effector.data['upkeep_reduction']
        self.upkeep_multiplier = ukm
        print(self.upkeep_multiplier)
