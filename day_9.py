from func import *
from heapq import nlargest
from functools import reduce
from operator import mul

with open("challenges/day_9.txt") as file:
    matrix = [[int(char) for char in line.strip()] for line in file.readlines()]

# returns the coordinates of all neighbors
neighbors = lambda m, x, y: filter(not_None,
                                   ((x_, y_) if 0 <= x_ < len(m[0]) and 0 <= y_ < len(m) else None
                                    for x_, y_ in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1))))

# returns the values of all neighbors
neighbors_vals = lambda m, x, y: map(lambda cord: point(matrix, fst(cord), snd(cord)), neighbors(m, x, y))

# returns the coordinates of all low_points
low_points = lambda m: filter(not_None, (
    (x, y) if all(map(lambda n: n > point(m, x, y), neighbors_vals(m, x, y))) else None
    for y in range(len(m)) for x in range(len(m[0]))
))

point = lambda m, x, y: m[y][x]

point_vals = lambda cords: map(lambda cord: matrix[fst(cord)][snd(cord)], cords)


def task1():
    res1 = sum(map(lambda cord: 1 + point(matrix, fst(cord), snd(cord)), low_points(matrix)))
    print(f'{res1=}')


# returns all coordinates that are higher than the points(x,y)
get_higher = lambda m, x, y: set(filter(not_None, (neighbor
                                                   if 9 > point(m, fst(neighbor), snd(neighbor)) > point(m, x, y)
                                                   else None for neighbor in neighbors(m, x, y))))


def get_all_higher_points(point):
    res = {*get_higher(matrix, *point)}
    return {i for p in res for i in get_all_higher_points(p)} | res


def task2():
    basins = map(len, (get_all_higher_points(p) | {p} for p in low_points(matrix)))
    res2 = reduce(mul, nlargest(3, basins))
    print(f'{res2=}')


if __name__ == '__main__':
    task1()  # 468
    task2()  # 1280496
