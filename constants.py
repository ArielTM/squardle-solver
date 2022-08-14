from enum import Enum
import json
import itertools

POSSIBLE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'


class SmallLettersType(Enum):
    SQUARE_DIV = 0
    COVER_DIV = 1
    IS_FADED = 2
    CLUE_SRC = 3
    CSS_DIV = 4
    GUESSED_LETTER = 5


with open(r"wordlist2.json", "r") as f:
    WORDLIST = json.load(f)

WORDLIST_3 = ['.'.join(x) for x in itertools.product(POSSIBLE_LETTERS, repeat=3)]
