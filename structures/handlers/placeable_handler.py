from enum import Enum
from typing import TYPE_CHECKING

import pygame
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
        self.total_pollution = 0
        self.pollution_level = 0

        self.add_method = {
            PlaceableType.INFRA: self.add_infra,
            PlaceableType.PLANT: self.add_plant,
        }

        self.plants_events.on('on_press_end', self.plant_clicked)
        self.gap = 20

    def plant_clicked(self, plant: 'Placeable'):
        if plant.p_type == PlaceableType.PLANT:
            self.game.modal_handler.show_simple_modal(
                f"Output: {plant.data['output_mw']} MW\nYearly Output: {u.display_wh(u.mw_to_h(plant.data['output_mw']))}"
                f"\nPollution: {u.display_number(plant.data['pollution_tco2e'] * plant.data['output_mw'])} tCO2e",
                title=f'{plant.name}: Info'
            )

    def update_output(self):
        self.total_output = sum([plant.data['output_mw'] for plant in self.plants.values])

    def update_pollution(self):
        self.total_pollution = sum(
            [plant.data['pollution_tco2e'] * plant.data['output_mw'] for plant in self.plants.values])

    def add_plant(self, p: 'Placeable'):
        if p.name in self.plants:
            p.object.destroy()
            return False
        self.plants[p.name] = p
        p.object.on('on_press_end', lambda e: self.plants_events.emit('on_press_end', p))
        self.update_output()
        self.update_pollution()
        for i in range(len(self.game.player.pollution_multipliers[0])):
            if (self.total_pollution <
                    self.game.player.energy_requirements * self.game.player.pollution_multipliers[0][i]):
                self.pollution_level = i
                break
        if not self.game.globals['first_plant']:
            self.game.globals['first_plant'] = True
            self.game.delay_handler.delay_run(
                0,
                lambda: self.game.modal_handler.show_simple_multi_modal((
                    {
                        'title': 'FIRST PLANT!',
                        'body': "Congratulations on placing your"
                                " first plant! Remember, in a year your total output should be "
                                "EQUAL OR EXCEED the energy demand. This ensures the nation is well powered.",
                    },
                    {
                        'title': 'FIRST PLANT!',
                        'body': "Also, ensure your pollution is in the green."
                                " Following both of these keeps your approval high.",
                    }
                )))

            print('Skibidi')
        return True

    def add_infra(self, p: 'Placeable'):
        if p.name in self.infra:
            p.object.destroy()
            return False
        self.infra[p.name] = p
        p.object.on('on_press_end', lambda e: self.infra_events.emit('on_press_end', p))
        return True

    def add_placeable(self, p: 'Placeable') -> bool:
        return self.add_method[p.p_type](p)  # noqa

    def draw_all(self, zoom_factor, surf: Surface, normalized_zoom_factor):
        for plant in self.plants.main_dict.values():
            plant.update_pos(zoom_factor)
            plant.object.rect.center = u.relative_pos(
                surf.get_size(),
                (plant.pos[0] * normalized_zoom_factor, plant.pos[1] * normalized_zoom_factor),
                from_xy="center-center")
            plant.object.draw(draw_surface=surf)

    def is_colliding(self, rect: pygame.Rect):
        return rect.collidelist(
            [u.expand_rect_outline(plant.object.rect, self.gap) for plant in self.plants.values]) == 0

    @staticmethod
    def in_country(country_mask: pygame.Mask, country_rect: pygame.Rect, placement_rect: pygame.Rect):
        corners = (
            placement_rect.topleft,
            placement_rect.topright,
            placement_rect.bottomleft,
            placement_rect.bottomright
        )
        for corner in corners:
            relative = corner[0] - country_rect.topleft[0], corner[1] - country_rect.topleft[1]
            try:
                if not country_mask.get_at(relative):
                    return False
            except IndexError:
                return False
        return True
        # offset = (placement_rect.x - country_rect.x, placement_rect.y - country_rect.y)
        # return country_mask.overlap(pygame.mask.Mask(placement_rect.size, fill=True), offset)
