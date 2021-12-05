from collections import Counter
from typing import Iterable

with open("challenges/day_3.txt") as file:
    lines = list(map(lambda s: s.strip(), file.readlines()))

# returns the most/least common symbol in list, n=0 for most common, n=-1 for least
common = lambda n, list_: (*Counter(list_).most_common()[n][0],)[0]
# returns the most common bits in one column as string
get_bits = lambda n, l: "".join((common(n, c) for c in l))
# transposes a list of strings
transpose = lambda l: [''.join(t) for t in zip(*l)]


def common_d(mode: int, column: Iterable, default):
    """
    :param column: the column
    :param default: the default returned by a tie
    :param mode: 0 for most common, -1 for least common
    :return:
    """
    most_common = Counter(column).most_common()
    return default if most_common[0][1] == most_common[1][1] else most_common[mode][0]


def task1(l):
    l = transpose(l)
    return int(get_bits(0, l), 2) * int(get_bits(-1, l), 2)


def filter_lines(filtered_lines, default: str, mode: int):
    """
    :param filtered_lines: the lines to be filtered
    :param default: the default value for a draw
    :param mode: 0 for most common element, -1 for least common
    :return: a single string
    """
    index = 0
    while len(filtered_lines) > 1:
        filter_bit = common_d(mode, transpose(filtered_lines)[index], default)
        filtered_lines = [line for line in filtered_lines if line[index] == filter_bit]
        index += 1
    return filtered_lines.pop()


def task2(l):
    o2 = int(filter_lines(l.copy(), "1", 0), 2)
    co2 = int(filter_lines(l.copy(), "0", -1), 2)
    return o2 * co2


if __name__ == '__main__':
    print(f'{task1(lines)=}')
    print(f'{task2(lines)=}')
