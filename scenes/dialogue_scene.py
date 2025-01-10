from typing import Optional

from pygame import K_RETURN

import modules.utilities as u
from modules.constants import white
from structures.hud.button import Button
from structures.hud.hud_object import HudObject
from structures.hud.input_box import InputBox
from structures.hud.text import Text
from structures.scene import Scene


class DialogueScene(Scene):
    curr_input: Optional[InputBox] = None
    # info_icon = u.load_scale('assets/info_icon_32_new.png', factor=2)

    def define_game_variables(self):
        dialogue_box = HudObject(self.game, self.game.modal, object_id="DialogueBox")
        dialogue_box.rect.topleft = u.cbp(self.game.screen, dialogue_box.surface)

        # info_box = HudObject(game, info_icon, parent=dialogue_box, pos=(40, 40), object_id="InfoBox")
        text = Text(self.game, 20, pos=(20, 80), parent=dialogue_box, color=(33, 0, 43))
        text.end_padding = 20
        text.wrap = True

        okay = Button(self.game, self.game.okay_surface, (0, 0), scale=0.6, select_cursor='NEXT')
        okay.rect.center = dialogue_box.rect.midbottom

        return {
            'box_w': dialogue_box.rect.width - 40,
            'text': text,
            'dialogue_box': dialogue_box,
            'okay': okay,
        }

    def draw(self):

        game, text, dialogue_box, okay, box_w = (
            self.game, self.g_vars['text'], self.g_vars['dialogue_box'], self.g_vars['okay'], self.g_vars['box_w'])
        u.draw_tiles(game.screen, game.bg_tile_scaled, game.tile_offset)
        game.tile_offset += game.tile_increase
        if game.tile_offset == 64:
            game.tile_offset = 0

        if game.loading_handler.is_transitioning:
            game.screen.blit(dialogue_box.surface, dialogue_box.rect)
            okay.draw()
            return

        text.text = game.curr_dialogue.subtext
        dialogue_box.draw()
        okay.draw()
        if game.curr_dialogue.is_last_block_char:
            if not self.curr_input and (curr_input_data := game.curr_dialogue.curr_input_data):
                dimensions = curr_input_data['options'].get('size') or (None, None)
                self.curr_input = InputBox(
                    game,
                    size=(dimensions[0] or box_w, dimensions[1] or 50),
                    parent=dialogue_box,
                    pos=(20, text.rect.top + text.surface.get_height() + 20),
                    object_id=curr_input_data["object_id"],
                    data=curr_input_data,
                    color=(255, 255, 255, 100)
                )

            if okay.on_press_end or game.input_handler.key_on_down.get(K_RETURN):
                if self.curr_input:
                    game.curr_dialogue.curr_input = self.curr_input.data
                    data, error = game.curr_dialogue.parse_data()
                    if error:
                        self.curr_input.error = error
                        return
                game.curr_dialogue.update()
        else:
            if self.curr_input:
                self.curr_input.destroy()
            self.curr_input = None
            if okay.on_press_end or game.input_handler.key_on_down.get(K_RETURN):
                game.curr_dialogue.skip_to_end_of_block()
            game.curr_dialogue.update()
