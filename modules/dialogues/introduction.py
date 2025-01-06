from modules.more_utilities.enums import GameState
from structures.hud.input_box import input_data
from structures.player import Player


def island_name_comment(name: str):
    if name.lower() == 'jamaica':
        return 'A developer favourite'
    else:
        return 'Lovely'


def developer_name_comment(name: str):
    if name.lower() in ("tori", "matthew", "tjon", "amari"):
        return f"A developer doppelganger I see! ;)"
    else:
        return "That's a neat object_id."


introduction = lambda game: ([
                    ("Welcome to Power Island!", {}),
                    ("In this game, you are tasked with managing a country's energy resources.", {}),
                    ("Before you start playing, we want to know a few things...", {}),
                    ("What is your object_id? ", {
                        "input": input_data("object_id", placeholder="Write your object_id here",
                                            options={"min_length": 3}),
                        "input_submit": lambda data: setattr(game, 'player', Player(game, data)),
                    }),
                    (
                        lambda: f"{game.player.id}? {
                        developer_name_comment(game.player.id)} Now what for the object_id of your island?",
                        {
                            "input": input_data("island_name", placeholder="Write your island object_id here",
                                                options={"min_length": 3}),
                            "input_submit": lambda data: setattr(game.player, 'island_name', data),
                        }),
                    (
                        lambda: f"You've chosen {
                        game.player.island_name}... {
                        island_name_comment(game.player.island_name)}! Press OKAY to jump into the action!",
                        {})
                ], {
                    "after": lambda: game.loading_handler.transition_to(GameState.MAIN)
                })
