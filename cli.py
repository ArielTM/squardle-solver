from squardle_state import SquardleState
from json import loads


def input_multiline(prompt=''):
    if prompt:
        print(prompt)

    multiline_text = ""
    text = input()
    while text != "":
        multiline_text += text + '\n'
        text = input()
    return multiline_text


if __name__ == "__main__":
    board_size = int(input("Board size [3/5]: "))
    if board_size not in [3, 5]:
        print("Illegal board size")
        exit()

    is_three_words = board_size == 3

    while True:
        small_squares_text = input_multiline("Enter 'smallSquares': ")
        small_squares = loads(small_squares_text)
        s = SquardleState(small_squares, is_three_words)
        print(s)
        print(s.get_letter_matrix())
