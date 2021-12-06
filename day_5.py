from __future__ import annotations
from dataclasses import dataclass
from collections import Counter

# types
from typing import Iterable, Callable, TypeVar

# helper functions
T = TypeVar("T")
fst: Callable[[Iterable[T], ], T]
fst = lambda t: t[0]
snd: Callable[[Iterable[T], ], T]
snd = lambda t: t[1]
lst: Callable[[Iterable[T], ], T]
lst = lambda t: t[-1]
flatten: Callable[[list[list[T]], ], list[T]]
flatten = lambda list_: [item for sublist in list_ for item in sublist]


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int

    def __getitem__(self, item):
        match item:
            case 0 | -2:
                return self.x
            case 1 | -1:
                return self.y
            case _:
                raise IndexError(f'Index out of bound for {item}')


@dataclass(frozen=True, eq=True)
class Line:
    points: tuple[Point]

    def is_horizontal(self) -> bool:
        return fst(self.points).y == lst(self.points).y

    def is_vertical(self) -> bool:
        return fst(self.points).x == lst(self.points).x

    def is_square(self) -> bool:
        return self.is_vertical() or self.is_horizontal()

    def interpolated(self) -> Line:
        assert len(self.points) == 2, "Only a line with two points can be interpolated!"

        if self.is_vertical():
            x = fst(self.points).x
            a, b = fst(self.points).y, lst(self.points).y
            start, stop = min(a, b), max(a, b) + 1
            points = [Point(x, y) for y in range(start, stop)]
        elif self.is_horizontal():
            y = fst(self.points).y
            a, b = fst(self.points).x, lst(self.points).x
            start, stop = min(a, b), max(a, b) + 1
            points = [Point(x, y) for x in range(start, stop)]
        else:
            p1, p2 = fst(self.points), lst(self.points)
            start_x, stop_x = min(p1.x, p2.x), max(p1.x, p2.x) + 1
            start_y, stop_y = min(p1.y, p2.y), max(p1.y, p2.y) + 1
            x_range = range(start_x, stop_x)
            y_range = range(start_y, stop_y)
            x_range = reversed(x_range) if p1.x > p2.x else x_range
            y_range = reversed(y_range) if p1.y > p2.y else y_range
            points = [Point(x, y) for x, y in zip(x_range, y_range)]

        return Line((*points,))

    def __iter__(self):
        return iter(self.points)


with open("challenges/day_5.txt") as file:
    lines = [line.strip().split(" -> ") for line in file.readlines()]
    lines: list[Line] = [Line((*(Point(*map(int, point.split(","))) for point in line),)) for line in lines]

no_points_above_2: Callable[[list[Point], ], int]
no_points_above_2 = lambda l: len((*filter(lambda i: snd(i) >= 2, Counter(l).most_common()),))


def task1():
    horizontal_lines = [line for line in lines if line.is_square()]
    interpolated_horizontal_lines = map(lambda l: l.interpolated(), horizontal_lines)
    # print_points(flatten(interpolated_horizontal_lines))
    no_above_2 = no_points_above_2(flatten(interpolated_horizontal_lines))
    print(f'{no_above_2=}')


def print_points(points: list[Point]):
    max_x = max(map(fst, points))
    max_y = max(map(snd, points))
    counts = Counter(points).most_common()
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            point = list(filter(lambda t: fst(t).x == x and fst(t).y == y, counts))
            if not point:
                print(".", end="")
            else:
                print(point.pop()[1], end="")
        print()


if __name__ == '__main__':
    interpolated_lines = list(map(lambda l: l.interpolated(), lines))
    #print_points(flatten(interpolated_lines))
    no_above_2 = no_points_above_2(flatten(interpolated_lines))
    print(f'{no_above_2=}')  # 12 != 15
