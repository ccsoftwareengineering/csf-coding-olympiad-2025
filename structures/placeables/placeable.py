import pygame

import modules.utilities as u
from modules.info.infra import InfraType
from modules.info.plants import PlantType
from modules.more_utilities.enums import ActionState
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
        self.object = Button(game, self.image, (0, 0), select_cursor='POINTER_CONFIG', attributes={
            'type': 'placeable'
        })
        self.predraw_surf = None
        self.attributes = Store()

        self.effectors = set()
        self.upkeep_multiplier = 1.0

        self.object.on('on_hover_start', self.start_hover, 'destroy')
        self.object.on('on_hover_end', self.stop_hover, 'destroy')

    def start_hover(self, _):
        print('h')
        if self.game.observable_handler['action_state'].value == ActionState.DESTROYING:
            self.game.cursor_handler.text = f'Delete "{self.name}"'

    def stop_hover(self, _):
        if self.game.observable_handler['action_state'].value == ActionState.DESTROYING:
            self.game.cursor_handler.text = ''

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

    def draw(self, zoom_factor, surf, normalized_zoom_factor):
        destroying = self.game.observable_handler['action_state'].value == ActionState.DESTROYING
        if self.object.hovering and destroying:
            self.game.cursor_handler.text = f'Delete "{self.name}"'
        else:
            self.game.cursor_handler.text = ''
        print(self.object.hovering)
        self.update_pos(zoom_factor)
        self.object.rect.center = u.relative_pos(
            surf.get_size(),
            (self.pos[0] * normalized_zoom_factor, self.pos[1] * normalized_zoom_factor),
            from_xy="center-center")
        if self.predraw_surf:
            rescaled = pygame.transform.scale_by(self.predraw_surf, normalized_zoom_factor)
            surf.blit(rescaled, rescaled.get_rect(center=self.object.rect.center))
        self.object.draw(draw_surface=surf)
