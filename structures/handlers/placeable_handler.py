from enum import Enum
from typing import TYPE_CHECKING

from pygame import Surface

from structures.event_emitter import EventEmitter
from structures.store import Store

if TYPE_CHECKING:
    from structures.game import Game
    from structures.placeable import Placeable

import modules.utilities as u


class PlaceableType(Enum):
    PLANT = 0
    INFRA = 1


class PlaceableManager(EventEmitter):
    def __init__(self, game: 'Game'):
        super().__init__()
        self.game = game
        self.plants = Store()
        self.infra = Store()

        self.plants_events = EventEmitter()
        self.infra_events = EventEmitter()

        self.total_output = 0

        self.add_method = {
            PlaceableType.INFRA: self.add_infra,
            PlaceableType.PLANT: self.add_plant,
        }

        self.plants_events.on('on_press_end', self.plant_clicked)

    def plant_clicked(self, plant: 'Placeable'):
        if plant.p_type == PlaceableType.PLANT:
            self.game.modal_handler.show_simple_modal(
                f"Output: {plant.data['output_mw']}",
                title=f'{plant.name}: Info'
            )

    def update_output(self):
        self.total_output = sum([plant.data['output_mw'] for plant in self.plants.main_dict.values()])

    def add_plant(self, p: 'Placeable'):
        if p.name in self.plants:
            p.object.destroy()
            return False
        self.plants[p.name] = p
        p.object.on('on_press_end', lambda e: self.plants_events.emit('on_press_end', p))
        self.update_output()
        return True

    def add_infra(self, p: 'Placeable'):
        if p.name in self.infra:
            p.object.destroy()
            return False
        self.infra[p.name] = p
        p.object.on('on_press_end', lambda e: self.infra_events.emit('on_press_end', p))
        return True

    def add_placeable(self, p: 'Placeable') -> bool:
        return self.add_method[p.p_type](p) # noqa

    def draw_all(self, zoom_factor, surf: Surface, normalized_zoom_factor):
        for plant in self.plants.main_dict.values():
            plant.update_pos(zoom_factor)
            plant.object.rect.center = u.relative_pos(
                surf.get_size(),
                (plant.pos[0] * normalized_zoom_factor, plant.pos[1] * normalized_zoom_factor),
                from_xy="center-center")
            plant.object.draw(draw_surface=surf)
