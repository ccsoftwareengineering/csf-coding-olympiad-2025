from typing import TYPE_CHECKING, cast

import pygame
from pygame import Surface

from modules.constants import dims
from modules.info.info import info_map
from modules.info.infra import InfraType
from modules.info.plants import PlantType
from modules.more_utilities.enums import PlaceableType, ActionState
from structures.event_emitter import EventEmitter
from structures.placeables.infra import Infra
from structures.placeables.plant import Plant
from structures.store import Store

if TYPE_CHECKING:
    from structures.game import Game
    from structures.placeables.placeable import Placeable

import modules.utilities as u


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

        self.on('on_press_end', self.placeable_click)
        self.on('add_infra', self.maintenance_added, 'update_internals')
        self.gap = 20

    def placeable_click(self, p: 'Placeable'):
        # deleting placeable
        if self.game.observable_handler['action_state'].value == ActionState.DESTROYING:
            if p.p_type == PlaceableType.INFRA:
                if p.type == InfraType.MAINTENANCE_CENTER:
                    self.mass_remove_effector(p)
                self.infra.remove(p.name)
            if p.p_type == PlaceableType.PLANT:
                self.plants.remove(p.name)
            self.game.player.budget += round(p.data['cost'] / 1000 * 0.75) * 1000
            del p
            self.update_output()
            self.update_pollution()
        else:
            self.game.modal_handler.show_simple_modal(
                body=p.get_info(),
                title=p.name + ': Info'
            )

    # there's a more elegant way to do this...
    # make the maintenance center store the plants and infra that it affects,
    # so everything doesn't have to be updated

    # also side note, all of this code is riddled with side effects
    #
    def mass_remove_effector(self, effector):
        for plant in self.plants.values:
            plant.remove_effector(effector)
        for infra in self.infra.values:
            infra.remove_effector(effector)

    def maintenance_added(self, infra: 'Infra'):
        for plant in cast(list['Plant'], self.plants.values):
            within = u.rect_circle_collision(pygame.Rect(plant.pos, plant.data['size']), infra.pos,
                                             infra.data['radius'])
            if within:
                plant.add_effector(infra)

        for _infra in cast(list['Infra'], self.plants.values):
            if _infra.type == InfraType.MAINTENANCE_CENTER:
                continue
            within = u.rect_circle_collision(pygame.Rect(_infra.pos, _infra.data['size']), infra.pos,
                                             infra.data['radius'])
            if within:
                _infra.add_effector(infra)

    def update_output(self):
        self.total_output = sum([plant.data['output_mw'] for plant in self.plants.values])

    def update_pollution(self):
        self.total_pollution = sum(
            [plant.data['pollution_tco2e'] * plant.data['output_mw'] for plant in self.plants.values])

    def add_plant(self, plant: 'Plant'):
        if plant.name in self.plants:
            plant.object.destroy()
            return False
        self.plants[plant.name] = plant
        plant.object.on('on_press_end', lambda e: self.plants_events.emit('on_press_end', plant))
        self.update_output()
        self.update_pollution()
        for i in range(len(self.game.player.pollution_multipliers[0])):
            if (self.total_pollution <
                    self.game.player.energy_requirements * self.game.player.pollution_multipliers[0][i]):
                self.pollution_level = i
                break
        self.first_plant_added()
        self.emit('add_plant', plant)
        for infra in self.infra.values:
            if infra.type == InfraType.MAINTENANCE_CENTER:
                within = u.rect_circle_collision(pygame.Rect(plant.pos, plant.data['size']), infra.pos,
                                                 infra.data['radius'])
                if within:
                    plant.add_effector(infra)
        return True

    def first_plant_added(self):
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

    def add_infra(self, infra: 'Infra'):
        if infra.name in self.infra:
            infra.object.destroy()
            return False
        self.infra[infra.name] = infra
        self.emit('add_infra', infra)
        if infra.type == InfraType.MAINTENANCE_CENTER:
            self.maintenance_added(infra)
        else:
            for _infra in self.infra:
                if _infra.type == InfraType.MAINTENANCE_CENTER:
                    within = u.rect_circle_collision(pygame.Rect(infra.pos, infra.data['size']), _infra.pos,
                                                     _infra.data['radius'])
                    if within:
                        infra.add_effector(infra)
        infra.object.on('on_press_end', lambda e: self.infra_events.emit('on_press_end', infra))
        return True

    def add_placeable(self, p: 'Placeable') -> bool:
        a = self.add_method[p.p_type](p)  # noqa
        if a:
            self.emit('add_placeable', p)
        p.object.on('on_press_end', lambda e: self.emit('on_press_end', p))
        return a

    def draw_all(self, zoom_factor, surf: Surface, normalized_zoom_factor):
        for infra in self.infra.values:
            infra.draw(zoom_factor, surf, normalized_zoom_factor)
        for plant in list(self.plants.values):
            plant.draw(zoom_factor, surf, normalized_zoom_factor)

    def is_colliding(self, rect: pygame.Rect, s_type: InfraType | PlantType, p_type: PlaceableType):
        a = rect.collidelist(
            [u.expand_rect_outline(plant.object.rect, plant.object.rect.w // 2) for plant in self.plants.values]) == 0
        b = rect.collidelist(
            [u.expand_rect_outline(infra.object.rect, infra.object.rect.w // 4) for infra in
             self.plants.values]) == 0
        if p_type == PlaceableType.PLANT:
            return a and b

        status = False
        if s_type == InfraType.MAINTENANCE_CENTER:
            pos = u.get_distance_from_centre(dims, rect.center)
            radius: int = info_map['infra'][InfraType.MAINTENANCE_CENTER]['radius']
            for infra in self.infra.values:
                if infra.type == InfraType.MAINTENANCE_CENTER:
                    status = status and not u.circles_collision(radius, pos, radius * 0.7, infra.pos)
                else:
                    status = status and rect.colliderect(infra.object.rect) == 0
            return status
        else:
            return a and b

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
