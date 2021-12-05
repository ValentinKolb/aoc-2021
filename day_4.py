import re

# types
from typing import Callable

Row = list[tuple[int, bool]]
Board = list[Row]

# helper functions
fst = lambda t: t[0]
snd = lambda t: t[1]
transpose: Callable[[Board], Board]
transpose = lambda l: Board(zip(*l))

with open("challenges/day_4.txt") as file:
    numbers = [int(num) for num in file.readline().split(",")]  # all numbers drawn

    boards: list[Board] = [
        [
            [(int(n), False) for n in re.split(r"\s+", row.strip())]
            for row in board
        ] for board in (
            board.split("\n") for board in file.read().strip().split("\n\n")
        )
    ]

sum_unmarked: Callable[[Board], int]
sum_unmarked = lambda b: sum(
    sum(
        map(fst, filter(lambda t: not snd(t), row))
    ) for row in b
)

any_row_full: Callable[[Board], bool]
any_row_full = lambda b: any(all(map(snd, row)) for row in b)

check_row: Callable[[Board], int]
check_row = lambda b: sum_unmarked(b) if any_row_full(b) else 0

check_col: Callable[[Board], int]
check_col = lambda b: check_row(transpose(b))


def print_board(b: Board) -> None:
    for row in b:
        print(" ".join(str(fst(n)).rjust(2)
                       if not snd(n) else
                       f'\x1b[7m{str(fst(n)).rjust(2)}\x1b[27m'
                       for n in row))


def set_num(n: int, b: Board) -> Board:
    """
    marks the number on the board
    :param n: the number to marked
    :param b: the board
    :return: the changed board
    """
    return [
        [(fst(t), True) if fst(t) == n else t for t in row]
        for row in b
    ]


def task_1():
    global boards
    for number in numbers:
        boards = Board(map(lambda b: set_num(number, b), boards))

        rows = list(map(check_row, boards))
        if any(rows):
            result = fst(list(filter(bool, rows)))
            print(f'{result*number=}')
            break

        cols = list(map(check_col, boards))
        if any(cols):
            result = fst(list(filter(bool, cols)))
            print(f'{result*number=}')
            break


def task_2():
    global boards
    for number in numbers:
        boards = Board(map(lambda b: set_num(number, b), boards))

        if len(boards) == 1 and (last_board := fst(boards)):
            if check_row(last_board) or check_col(last_board):
                if result := sum_unmarked(last_board):
                    print(f'{result*number=}')
                elif result := sum_unmarked(last_board):
                    print(f'{result*number=}')
                break

        else:
            boards = [board for board in boards if not check_row(board)]
            boards = [board for board in boards if not check_col(board)]


if __name__ == '__main__':
    task_2()
