from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from structures.game import Game


class DelayHandler:
    def __init__(self, game: 'Game'):
        self.game = game
        self.delays = {}

    def delay_run(self, delay, func):
        time = datetime.now()
        self.delays[time] = (time, delay, func)

    def run_all(self):
        now = datetime.now()
        for key, val in tuple(self.delays.items()):
            if (now - val[0]).microseconds > val[1]:
                val[2]()
                del self.delays[key]