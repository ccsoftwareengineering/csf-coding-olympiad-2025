import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from structures.game import Game


class DialogueHandler:
    def __init__(self, game: 'Game', dialogue_id: str, speed=0.05):
        self.game = game
        self.dialogue = game.dialogues[dialogue_id][0]
        self.options: dict = game.dialogues[dialogue_id][1]
        self.speed = speed
        self.is_last_block_char = False
        self.done = False
        self.curr_block = 0
        self.curr_char = 0
        self.prev_time = datetime.datetime.now()
        self.curr_text = self.get_text()

    def get_text(self):
        text_ish = self.dialogue[self.curr_block][0]
        if type(text_ish) is str:
            return text_ish
        else:
            return text_ish()

    def get_subtext(self):
        return self.curr_text[0:self.curr_char + 1]

    def skip_to_end_of_block(self):
        self.curr_char = len(self.dialogue[self.curr_block][0]) - 1
        self.is_last_block_char = True

    def next_block(self):
        self.is_last_block_char = False
        if self.curr_block == len(self.dialogue) - 1:
            self.done = True
        else:
            # right here is where I do the input checking stuff
            self.curr_block += 1
            self.curr_char = 0
            self.curr_text = self.get_text()

    def update(self):
        diff = (datetime.datetime.now() - self.prev_time)
        sec = diff.microseconds / 1_000_000
        if sec > self.speed:
            block_len = len(self.dialogue[self.curr_block][0])
            if self.curr_char == block_len - 1:
                # MOVE TO NEXT BLOCK
                self.next_block()
            else:
                self.curr_char += 1
                if self.curr_char == block_len - 1:
                    # HAS MOVED TO THE LAST ONE
                    self.is_last_block_char = True
            self.prev_time = datetime.datetime.now()
            return True
        else:
            return False
