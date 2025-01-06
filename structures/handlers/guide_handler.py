from typing import TYPE_CHECKING, Callable

import pygame
from pygame import Surface, K_RETURN

import modules.utilities as u
from modules.constants import default_emulated_x
from modules.more_utilities.enums import Direction, VerticalAlignment, HorizontalAlignment
from modules.more_utilities.guide_helpers import get_curr_guide_info, GuideInfo
from structures.hud.dynamic_button import DynamicButton
from structures.hud.hud_object import HudObject
from structures.hud.text import Text

if TYPE_CHECKING:
    from structures.game import Game


class GuideHandler:
    def __init__(self, game: 'Game', text_gap=25, button_gap=10):
        self.game = game
        self.text_gap = text_gap
        self.button_gap = button_gap
        self.rect_template = u.rounded_rect_template((255, 255, 255), emulated_x=default_emulated_x, radius=8)
        self.dark_surface = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        self.dark_surface.set_colorkey((255, 255, 255))
        self.dark_surface.set_alpha(255 // 2)
        self.text_hud = HudObject(game, Surface((400, 300), pygame.SRCALPHA), pos=(0, 0))
        self.text = Text(game, 14, pos=(0, 0), color=(255, 255, 255), parent=self.text_hud)
        self.ok_button = DynamicButton(
            game,
            (100, 30),
            text_options={'size': 10, 'color': (255, 255, 255)},
            rect_template=u.rounded_rect_template(
                color=(0, 0, 0, 0),
                emulated_x=default_emulated_x,
                radius=4, outline=1,
                outline_color=(255, 255, 255)
            ),
            text="OKAY!",
            object_id="ok_guide_button"
        )
        self.button_height = self.ok_button.surface.get_height()

        self.text_placement_strategies: dict[
            Direction, dict[VerticalAlignment, Callable[[pygame.Rect, tuple[int, int]], None]]] = {
            Direction.LEFT: {
                VerticalAlignment.TOP: lambda rect, offset: self.set_text_rect_pos_to(
                    'topright',
                    (rect.topleft[0] - self.text_gap + offset[0],
                     rect.top + offset[1])
                ),

                VerticalAlignment.CENTER: lambda rect, offset: self.set_text_rect_pos_to(
                    'midright',
                    (rect.midleft[0] - self.text_gap + offset[0], rect.midleft[1] - self.button_visible_offset // 2)
                ),

                VerticalAlignment.BOTTOM: lambda rect, offset: self.set_text_rect_pos_to(
                    'bottomright',
                    (rect.bottomleft[0] - self.text_gap + offset[0], rect.bottom - self.button_visible_offset)
                )
            },
            Direction.RIGHT: {
                VerticalAlignment.TOP: lambda rect, offset: self.set_text_rect_pos_to(
                    'topleft',
                    (rect.topright[0] + self.text_gap + offset[0],
                     rect.top + offset[1])
                ),

                VerticalAlignment.CENTER: lambda rect, offset: self.set_text_rect_pos_to(
                    'midleft',
                    (rect.midright[0] + self.text_gap + offset[0], rect.midright[1] - self.button_visible_offset // 2)
                ),

                VerticalAlignment.BOTTOM: lambda rect, offset: self.set_text_rect_pos_to(
                    'bottomleft',
                    (rect.bottomright[0] + self.text_gap + offset[0], rect.bottom - self.button_visible_offset)
                )
            },
            Direction.UP: {
                VerticalAlignment.TOP: lambda rect, offset: self.set_text_rect_pos_to(
                    'bottomleft',
                    (rect.left, rect.top - self.text_gap - self.button_visible_offset + offset[0])
                ),

                VerticalAlignment.CENTER: lambda rect, offset: self.set_text_rect_pos_to(
                    'midbottom',
                    (rect.midtop[0], rect.midtop[1] - self.text_gap - self.button_visible_offset + offset[0])
                ),

                VerticalAlignment.BOTTOM: lambda rect, offset: self.set_text_rect_pos_to(
                    'bottomright',
                    (rect.right, rect.topright[1] - self.text_gap - self.button_visible_offset + offset[0])
                )
            },
            Direction.DOWN: {
                VerticalAlignment.TOP: lambda rect, offset: self.set_text_rect_pos_to(
                    'topleft',
                    (rect.left, rect.bottom + self.text_gap + offset[0])
                ),

                VerticalAlignment.CENTER: lambda rect, offset: self.set_text_rect_pos_to(
                    'midtop',
                    (rect.midtop[0], rect.midbottom[1] + self.text_gap + offset[0])
                ),

                VerticalAlignment.BOTTOM: lambda rect, offset: self.set_text_rect_pos_to(
                    'topright',
                    (rect.right, rect.bottomright[1] + self.text_gap + offset[0])
                )
            },
        }

        self.button_placement_strategies = {
            HorizontalAlignment.LEFT: lambda: self.set_button_rect_pos_to('topleft', (
                self.text_hud.rect.left,
                self.text_hud.rect.bottom + self.button_gap
            )),
            HorizontalAlignment.CENTER: lambda: self.set_button_rect_pos_to('midtop', (
                self.text_hud.rect.centerx,
                self.text_hud.rect.midbottom[1] + self.button_gap
            )),
            HorizontalAlignment.RIGHT: lambda: self.set_button_rect_pos_to('topright', (
                self.text_hud.rect.right,
                self.text_hud.rect.bottomright[1] + self.button_gap
            ))
        }

    def set_button_rect_pos_to(self, which: str, v: tuple[int, int]):
        setattr(self.ok_button.rect, which, v)

    def set_text_rect_pos_to(self, which: str, v: tuple[int, int]):
        setattr(self.text_hud.rect, which, v)

    @property
    def button_visible_offset(self):
        return self.button_height + self.button_gap  # if self.ok_button.visible else 0

    def update_text_hud_and_button(self, cgi: GuideInfo):
        rect = cgi['rect']
        direction = cgi['text_placement']
        offset = cgi['text_offset']
        self.text.text = self.game.curr_dialogue.subtext
        self.text.align = cgi['text_alignment']
        self.text.predraw()
        self.text_hud.rect.size = self.text.rect.size
        self.text_placement_strategies[direction][cgi['text_box_alignment']](rect, offset)
        self.button_placement_strategies[cgi['button_alignment']]()

    def draw(self):
        curr_guide_info = get_curr_guide_info(self.game)
        self.dark_surface.fill((0, 0, 0))
        if self.game.loading_handler.is_transitioning:
            self.game.screen.blit(self.dark_surface, (0, 0))
            return
        self.dark_surface.blit(self.rect_template(curr_guide_info['rect'].size), curr_guide_info['rect'].topleft)
        self.game.screen.blit(self.dark_surface, (0, 0))

        self.update_text_hud_and_button(curr_guide_info)
        self.text_hud.draw()
        self.ok_button.draw()

        if self.game.curr_dialogue.is_last_block_char:
            self.ok_button.visible = True
            if self.ok_button.on_press_end or self.game.input_handler.key_on_down.get(pygame.K_RETURN):
                # if self.curr_input:
                #     game.curr_dialogue.curr_input = self.curr_input.data
                #     data, error = game.curr_dialogue.parse_data()
                #     if error:
                #         self.curr_input.error = error
                #         return
                self.ok_button.predraw()
                self.game.curr_dialogue.update()
                self.ok_button.visible = False
        else:
            # if self.curr_input:
            #     self.curr_input.destroy()
            # self.curr_input = None
            if self.ok_button.on_press_end or self.game.input_handler.key_on_down.get(K_RETURN):
                self.game.curr_dialogue.skip_to_end_of_block()
            self.ok_button.visible = False
            self.game.curr_dialogue.update()
