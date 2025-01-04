import datetime
from typing import TYPE_CHECKING

from modules.more_utilities.input_parse import input_parse

if TYPE_CHECKING:
    from structures.game import Game


# trying to make it so that you can access the input from the respective dialogue
# create the input box there and handle it
# but the dialogue handler would have methods to check if the data reconciles
# todo: implement function to add input data and store it in dialgoue handler
# dialogue handler will then use the input parser functions to ensure everything's legit

class DialogueHandler:
    def __init__(self, game: 'Game', dialogue_id: str, speed=0.05):
        self.game = game
        self.dialogue = game.dialogues[dialogue_id][0]
        self.options: dict = game.dialogues[dialogue_id][1]
        self.speed = speed
        self.is_last_block_char = False
        self.done = False
        self.curr_block_index = 0
        self.curr_char = 0
        self.prev_time = datetime.datetime.now()
        self.curr_text = self.get_text()
        self.curr_input = None
        self.parsed_data = None

    @property
    def curr_block(self):
        return self.dialogue[self.curr_block_index]

    @property
    def curr_input_data(self):
        return self.curr_block[1].get('input')

    @property
    def curr_block_data(self):
        return self.curr_block[1]

    def parse_data(self):
        data, error = input_parse(self.curr_input, self.curr_input_data)
        self.parsed_data = data
        return data, error

    def get_text(self):
        text_ish = self.curr_block[0]
        if type(text_ish) is str:
            return text_ish
        else:
            return text_ish()

    @property
    def subtext(self):
        return self.curr_text[0:self.curr_char + 1]

    @property
    def is_guide(self):
        return "guide" in self.options

    def skip_to_end_of_block(self):
        self.curr_char = len(self.curr_text) - 2

    def next_block(self):
        self.is_last_block_char = False
        if self.curr_block_index == len(self.dialogue) - 1:
            self.done = True
            after_fn = self.options.get('after')
            if after_fn:
                after_fn()
            self.game.cursor_handler.cursor = 'NORMAL'
            self.game.curr_dialogue = None
            self.game.in_dialogue = False
            self.game.in_guide = False
        else:
            # right here is where I do the input checking stuff
            input_submit_fn = self.curr_block[1].get('input_submit')
            if input_submit_fn:
                input_submit_fn(self.parsed_data)
            self.curr_block_index += 1
            self.curr_char = 0
            self.curr_text = self.get_text()
            self.curr_input = self.curr_input_data and "" or None

    def update(self):
        diff = (datetime.datetime.now() - self.prev_time)
        sec = diff.microseconds / 1_000_000
        if sec > self.speed:
            block_len = len(self.curr_text)
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
