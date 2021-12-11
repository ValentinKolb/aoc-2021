from func import *
from itertools import count

with open("challenges/day_11.txt") as file:
    octopuses = [[int(octopus) for octopus in line.strip()] for line in file.readlines()]

inc_m = lambda m: map(pmap(inc), m)
unmap = lambda m: list(map(list, m))
inc_if = lambda m: map(pmap(lambda i: i if not i else inc(i)), m)


def task1():
    global octopuses
    flashes = 0
    for i in range(100):
        octopuses = unmap(inc_m(octopuses))
        while any(map(gt_n(9), flatten(octopuses))):
            flashes += 1
            x, y = octopus = indexm(octopuses, gt_n(9))
            octopuses[y][x] = 0
            for (x, y) in neighbors(octopuses, *octopus):
                val = position(octopuses, x, y)
                octopuses[y][x] = inc(val) if val else val

    print(f'{flashes=}')


def task2():
    global octopuses
    for i in count():

        if all(map(eq_n(0), flatten(octopuses))):
            print(f'{i=}')
            break

        octopuses = unmap(inc_m(octopuses))
        while any(map(gt_n(9), flatten(octopuses))):
            x, y = octopus = indexm(octopuses, gt_n(9))
            octopuses[y][x] = 0
            for (x, y) in neighbors(octopuses, *octopus):
                val = position(octopuses, x, y)
                octopuses[y][x] = inc(val) if val else val


if __name__ == '__main__':
    task2()
