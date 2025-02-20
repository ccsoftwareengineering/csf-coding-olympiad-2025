from typing import TYPE_CHECKING
from modules.dialogues.introduction import introduction
from modules.dialogues.starting_tutorial import starting_tutorial

if TYPE_CHECKING:
    from structures.game import Game


def dialogues(game: 'Game'):
    return {
        'introduction': introduction(game),
        'starting_tutorial': starting_tutorial(game),
    }
