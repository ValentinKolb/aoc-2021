from toolz.curried import *
from func import print_matrix

Matrix = list[list[bool]]
print_matrix = curry(print_matrix)(transform=lambda c: '#' if c else ".", space=" ")

with open("challenges/day_13.txt") as file:
    coordinates, instructions = file.read().split("\n\n")
    coordinates = [tuple(int(i) for i in row.split(",")) for row in coordinates.split("\n")]
    instructions = instructions.split("\n")

    width = max(map(first, coordinates)) + 1
    height = max(map(second, coordinates)) + 1

    matrix = [[True if (x, y) in coordinates else False
               for x in range(width)]
              for y in range(height)]

combine = lambda m_a, m_b: [[a or b for a, b in zip(row_a, row_b)]
                            for row_a, row_b in zip(m_a, m_b)]


def fold_y(matrix_: Matrix, y_: int):
    upper_m, lower_m = (matrix[:y_]), reversed(matrix_[y_ + 1:])
    return combine(upper_m, lower_m)


def fold_x(matrix_: Matrix, x_: int):
    left_m, right_m = (reversed(row[x_ + 1:]) for row in matrix_), ((row[:x_]) for row in matrix_)
    return combine(left_m, right_m)


count = compose(len, list, filter(bool), concat)

if __name__ == '__main__':
    for instruction in instructions:
        if "x" in instruction:
            _, x = instruction.split("=")
            print(f"folding along {x=}")
            matrix = fold_x(matrix, int(x))
        else:
            _, y = instruction.split("=")
            print(f'folding along {y=}')
            matrix = fold_y(matrix, int(y))

        print_matrix(matrix)
        print()

