import pygame
from pygame import Surface

from structures.hud.hud_object import HudObject
import modules.utilities as u
from structures.hud.text import Text


class MoneyDisplay(HudObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, surface=Surface((0, 0), pygame.SRCALPHA))
        self.size = kwargs.get("size")
        scaled_money = round(self.size * 1.8)
        self.money = u.load_scale('assets/ui/icons/money.png', size=(scaled_money, scaled_money))
        self.money_size = (scaled_money, scaled_money)
        self.half_money = scaled_money // 2
        self.distance = self.size // 3.5
        self.text = Text(self.game, size=kwargs.get('size'), wrap=False, color=(255, 255, 255), outline=2)

    def predraw(self):
        self.text.text = u.display_number(self.game.player.budget)
        self.text.predraw()
        text_size = self.text.current_surface.get_size()
        x_size = text_size[0] + self.distance + self.money_size[0]
        self.surface = Surface((x_size, self.money_size[1]),
                               pygame.SRCALPHA)
        self.text.rect.midleft = (self.money_size[0] + self.distance, self.half_money - 4)
        self.surface.blit(self.text.current_surface, self.text.rect)
        self.surface.blit(self.money, (0, 0))