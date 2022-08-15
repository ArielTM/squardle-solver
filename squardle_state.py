import json

from constants import WORDLIST, WORDLIST_3, SmallLettersType, POSSIBLE_LETTERS
from tabulate import tabulate


class SquardleState:
    def __init__(self, small_squares, is_three_words=True):
        self.is_daily = is_three_words

        self.passed_squares = [[1, 1], [3, 1], [1, 3], [3, 3]] if self.is_daily else []

        middle_wordlist = WORDLIST_3 if self.is_daily else WORDLIST
        middle_letters = ["."] if self.is_daily else POSSIBLE_LETTERS
        self.possible_words_vertical = [
            WORDLIST,
            middle_wordlist,
            WORDLIST,
            middle_wordlist,
            WORDLIST,
        ]
        self.possible_words_horizontal = [
            WORDLIST,
            middle_wordlist,
            WORDLIST,
            middle_wordlist,
            WORDLIST,
        ]
        self.letters_matrix = [
            [
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
            ],
            [
                POSSIBLE_LETTERS,
                middle_letters,
                POSSIBLE_LETTERS,
                middle_letters,
                POSSIBLE_LETTERS,
            ],
            [
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
            ],
            [
                POSSIBLE_LETTERS,
                middle_letters,
                POSSIBLE_LETTERS,
                middle_letters,
                POSSIBLE_LETTERS,
            ],
            [
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
                POSSIBLE_LETTERS,
            ],
        ]

        self.do_analysis(small_squares)

    def do_analysis(self, small_squares):
        self.parse_small_squares(small_squares)

        prev_wordlist_sum = 0
        while self.all_possible_words() != prev_wordlist_sum:
            prev_wordlist_sum = self.all_possible_words()
            print(prev_wordlist_sum)
            self.apply_letter_analysis()

    def all_possible_words(self):
        wordlist_sum = 0
        for i in range(5):
            wordlist_sum += len(self.possible_words_horizontal[i]) + len(
                self.possible_words_vertical[i]
            )
        return wordlist_sum

    def parse_small_squares(self, small_squares):
        for x in range(5):
            for y in range(5):
                if [x, y] in self.passed_squares:
                    continue
                for i in range(16):
                    self.parse_small_square(x, y, small_squares[x][y][i])

    def parse_small_square(self, x, y, small_square):

        if small_square[SmallLettersType.SQUARE_DIV.value] is False:
            return

        current_letter = small_square[SmallLettersType.GUESSED_LETTER.value]
        current_image = small_square[SmallLettersType.CLUE_SRC.value]

        if current_image.startswith("greener"):
            self.set_green_horizontal(x, y, current_letter)
            self.set_green_vertical(x, y, current_letter)
        elif current_image.startswith("redder"):
            self.set_black_horizontal(x, y, current_letter, False)
            self.set_yellow_vertical(x, y, current_letter)
        elif current_image.startswith("yellower"):
            self.set_yellow_horizontal(x, y, current_letter)
            self.set_black_vertical(x, y, current_letter, False)
        elif current_image.startswith("oranger"):
            self.set_yellow_horizontal(x, y, current_letter, False)
            self.set_yellow_vertical(x, y, current_letter, False)
        elif current_image.startswith("whiter"):
            self.set_black_horizontal(x, y, current_letter)
            self.set_black_vertical(x, y, current_letter)
        elif current_image.startswith("blacker"):
            self.set_global_black(current_letter)
        else:
            raise Exception("No matching letter class")

    def set_green_horizontal(self, x, y, letter):
        self.possible_words_horizontal[y] = self.apply_green_letter_to_wordlist(
            self.possible_words_horizontal[y], letter, x
        )

    def set_green_vertical(self, x, y, letter):
        self.possible_words_vertical[x] = self.apply_green_letter_to_wordlist(
            self.possible_words_vertical[x], letter, y
        )

    def set_black_horizontal(self, x, y, letter, realblack=True):
        self.possible_words_horizontal[y] = self.apply_black_letter_to_wordlist(
            self.possible_words_horizontal[y], letter
        )
        if realblack:
            for i in range(len(self.possible_words_horizontal)):
                self.possible_words_horizontal[
                    i
                ] = self.apply_positional_black_letter_to_wordlist(
                    self.possible_words_horizontal[i], letter, x
                )

    def set_black_vertical(self, x, y, letter, realblack=True):
        self.possible_words_vertical[x] = self.apply_black_letter_to_wordlist(
            self.possible_words_vertical[x], letter
        )

        if realblack:
            for i in range(len(self.possible_words_vertical)):
                self.possible_words_vertical[
                    i
                ] = self.apply_positional_black_letter_to_wordlist(
                    self.possible_words_vertical[i], letter, y
                )

    def set_yellow_horizontal(self, x, y, letter, realyellow=True):
        self.possible_words_horizontal[y] = self.apply_yellow_letter_to_wordlist(
            self.possible_words_horizontal[y], letter, x
        )

        if realyellow:
            for i in range(len(self.possible_words_horizontal)):
                if i == y:
                    continue
                self.possible_words_horizontal[
                    i
                ] = self.apply_positional_black_letter_to_wordlist(
                    self.possible_words_horizontal[i], letter, x
                )

    def set_yellow_vertical(self, x, y, letter, realyellow=True):
        self.possible_words_vertical[x] = self.apply_yellow_letter_to_wordlist(
            self.possible_words_vertical[x], letter, y
        )

        if realyellow:
            for i in range(len(self.possible_words_vertical)):
                if i == x:
                    continue
                self.possible_words_vertical[
                    i
                ] = self.apply_positional_black_letter_to_wordlist(
                    self.possible_words_vertical[i], letter, y
                )

    def set_global_black(self, letter):
        for i in range(len(self.possible_words_horizontal)):
            self.possible_words_horizontal[i] = self.apply_black_letter_to_wordlist(
                self.possible_words_horizontal[i], letter
            )
        for i in range(len(self.possible_words_vertical)):
            self.possible_words_vertical[i] = self.apply_black_letter_to_wordlist(
                self.possible_words_vertical[i], letter
            )

    @staticmethod
    def apply_black_letter_to_wordlist(wordlist, letter):
        if wordlist == []:
            return []
        new_wordlist = [word for word in wordlist if letter not in word]
        return new_wordlist

    @staticmethod
    def apply_yellow_letter_to_wordlist(wordlist, letter, pos):
        if wordlist == []:
            return []
        new_wordlist = [
            word for word in wordlist if letter in word and word[pos] != letter
        ]
        return new_wordlist

    @staticmethod
    def apply_green_letter_to_wordlist(wordlist, letter, pos):
        if wordlist == []:
            return []
        new_wordlist = [word for word in wordlist if word[pos] == letter]
        return new_wordlist

    @staticmethod
    def apply_positional_black_letter_to_wordlist(wordlist, letter, pos):
        if wordlist == []:
            return []
        new_wordlist = [word for word in wordlist if word[pos] != letter]
        return new_wordlist

    def apply_letter_analysis(self):
        self.letter_analysis()
        self.apply_letter_matrix_on_wordlists()

    def letter_analysis(self):
        letters_matrix = self.letters_matrix

        for y, wordlist in enumerate(self.possible_words_horizontal):
            # if IS_DAILY and y in [1, 3]:
            #     continue

            letters = [set([word[i] for word in wordlist]) for i in range(5)]

            for x in range(5):
                letters_matrix[x][y] = list(set(letters_matrix[x][y]) & letters[x])

        for x, wordlist in enumerate(self.possible_words_vertical):
            # if IS_DAILY and x in [1, 3]:
            #     continue

            letters = [set([word[i] for word in wordlist]) for i in range(5)]

            for y in range(5):
                letters_matrix[x][y] = list(set(letters_matrix[x][y]) & letters[y])

        self.letters_matrix = letters_matrix

    def apply_letter_matrix_on_wordlists(self):
        for y, wordlist in enumerate(self.possible_words_horizontal):
            # if IS_DAILY and y in [1, 3]:
            #     continue
            self.possible_words_horizontal[y] = self.apply_letters_list_on_wordlist(
                wordlist, [self.letters_matrix[i][y] for i in range(5)]
            )

        for x, wordlist in enumerate(self.possible_words_vertical):
            # if IS_DAILY and x in [1, 3]:
            #     continue
            self.possible_words_vertical[x] = self.apply_letters_list_on_wordlist(
                wordlist, self.letters_matrix[x]
            )

    @staticmethod
    def apply_letters_list_on_wordlist(wordlist, letters_list):
        for i in range(5):
            wordlist = [word for word in wordlist if word[i] in letters_list[i]]

        return wordlist

    def __str__(self):
        data = ""
        data += "Horizontal:\n"
        for words in self.possible_words_horizontal:
            if not words:
                continue
            wordlist = ", ".join(words[:30])
            data += f"\t({len(words)}) {wordlist}\n"

        data += "Vertical:\n"
        for words in self.possible_words_vertical:
            if not words:
                continue
            wordlist = ", ".join(words[:30])
            data += f"\t({len(words)}) {wordlist}\n"

        return data

    def get_letter_matrix(self):
        letters_data = self.letters_matrix
        letters_data = list(map(list, zip(*letters_data)))
        return tabulate(letters_data)
