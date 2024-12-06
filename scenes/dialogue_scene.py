import pygame.key
from pygame import K_RETURN

import modules.utilities as u
from structures.game import Game
from structures.hud.button import Button
from structures.hud.hud_object import HudObject
from structures.hud.text import Text

info_icon = u.load_scale('assets/info_icon_32_new.png', factor=2)
modal = u.load_scale('assets/modal.png', factor=4)


def draw_dialogue_factory(game: Game):
    dialogue_box = HudObject(game, modal, name="DialogueBox")
    dialogue_box.rect.topleft = u.cbp(game.screen, dialogue_box.surface)

    # info_box = HudObject(game, info_icon, parent=dialogue_box, pos=(40, 40), name="InfoBox")
    text = Text(game, "", 32, (20, 80), parent=dialogue_box, color=(33, 0, 43))
    text.end_padding = 20
    text.wrap = True

    okay_surface = u.load_scale('assets/okay_button.png', factor=2)
    okay = Button(game, okay_surface, (0, 0), scale=0.6)
    okay.rect.center = dialogue_box.rect.midbottom

    def draw_dialogue():
        nonlocal text
        u.draw_tiles(game, game.screen, game.bg_tile_scaled, game.tile_offset)
        game.tile_offset += 0.5
        if game.tile_offset == 64:
            game.tile_offset = 0

        text.text = game.curr_dialogue.get_text()
        dialogue_box.draw()
        okay.draw()
        if not game.curr_dialogue.is_last_block_char or okay.on_press_end or game.on_press_start.get(K_RETURN):
            game.curr_dialogue.update()

    return draw_dialogue
