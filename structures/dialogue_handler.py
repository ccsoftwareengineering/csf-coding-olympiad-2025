import datetime

import dialogue


class DialogueHandler:
    def __init__(self, dialogue_id: str, speed=0.05):
        self.dialogue: list[str] = dialogue.dialogues[dialogue_id]
        self.speed = speed
        self.is_last_block_char = False
        self.done = False
        self.curr_block = 0
        self.curr_char = 0
        self.prev_time = datetime.datetime.now()

    def get_text(self):
        return self.dialogue[self.curr_block][0:self.curr_char + 1]

    def skip_to_end_of_block(self):
        self.curr_char = len(self.dialogue[self.curr_block]) - 1
        self.is_last_block_char = True

    def update(self):
        diff = (datetime.datetime.now() - self.prev_time)
        sec = diff.microseconds / 1_000_000
        if sec > self.speed:
            block_len = len(self.dialogue[self.curr_block])
            if self.curr_char == block_len - 1:
                self.is_last_block_char = False
                if self.curr_block == len(self.dialogue) - 1:
                    self.done = True
                else:
                    self.curr_block += 1
                    self.curr_char = 0
            else:
                self.curr_char += 1
                if self.curr_char == block_len - 1:
                    self.is_last_block_char = True
            self.prev_time = datetime.datetime.now()
            return True
        else:
            return False
