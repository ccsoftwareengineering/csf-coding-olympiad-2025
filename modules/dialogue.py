import typing

from structures.hud.input_box import input_data
from structures.player import Player

if typing.TYPE_CHECKING:
    from structures.game import Game


def dialogues(game: 'Game'):
    def create_player(name):
        game.player = Player(name)

    return {
        'introduction': ([
            ("Welcome to Power Island!", {}),
            ("In this game, you are tasked with managing a country's energy resources.", {}),
            ("Before you start playing, we want to know a few things...", {}),
            ("What is your name? ", {
                "input": input_data("name", placeholder="Write your name here"),
                "input_submit": lambda data: create_player(data),
            }),
            (lambda: f"{game.player.name}? That's a neat name. Here's how you can get started.", {}),
        ], {})
    }
