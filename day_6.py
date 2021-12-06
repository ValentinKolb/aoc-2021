from collections import Counter
from typing import Callable, TypeVar, Iterable

# types
FishList = list[int]
T = TypeVar("T")

# helper
fst: Callable[[Iterable[T], ], T]
fst = lambda t: t[0]
snd: Callable[[Iterable[T], ], T]
snd = lambda t: t[1]
lst: Callable[[Iterable[T], ], T]
lst = lambda t: t[-1]
flatten: Callable[[list[list[T]], ], list[T]]
flatten = lambda list_: [item for sublist in list_ for item in sublist]

with open("challenges/day_6.txt") as file:
    lanternfish = map(int, file.read().split(","))

reproduce: Callable[[FishList], FishList]
reproduce = lambda fish: flatten([[f - 1] if f != 0 else [6, 8] for f in fish])


def task1(fish_list):
    for i in range(80):
        fish_list = reproduce(fish_list)
    print(f'{len(fish_list)=}')


def task2(fish_list):
    fish_list = Counter(fish_list).most_common()
    for i in range(9):
        if i not in map(fst, fish_list):
            fish_list.append((i, 0))
    fish_list = sorted(fish_list)

    for i in range(256):
        count_fish_0 = snd(fst(fish_list))
        fish_list = [(fish, count) for (fish, _), (_, count) in zip(fish_list, fish_list[1:])] + [(8, count_fish_0)]
        fish_list[6] = (6, snd(fish_list[6]) + count_fish_0)

    no_of_fish = sum(map(snd, fish_list))
    print(f'{no_of_fish=}')


if __name__ == '__main__':
    task2(lanternfish)
