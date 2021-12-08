from typing import TypeVar, Callable, Iterable

NumberOfSegments = int
Number = int

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

with open("challenges/day_8.txt") as file:
    lines = map(lambda l: l.strip().split(" | "), file.readlines())


def task1():
    easy_code: dict[NumberOfSegments, Number] = {
        2: 1,
        4: 4,
        3: 7,
        7: 8
    }
    output_values = flatten(map(lambda s: s.split(), map(snd, lines)))
    output_values = filter(lambda s: len(s) in easy_code, output_values)
    output_values = map(lambda s: easy_code[len(s)], output_values)
    print(len(list(output_values)))


filter_num = lambda n, l: list(filter(lambda s: len(s) == n, l))[0]


def task2():
    result = []

    for line in lines:
        input_line, output_line = line[0].split(), line[1].split()
        input_line = list(map(frozenset, input_line))
        output_line = list(map(frozenset, output_line))

        # the two is the only number where the 'f'-position is missing.
        temp = (list(filter(lambda s: c not in s, input_line)) for c in "abcdfeg")
        num2 = list(filter(lambda l: len(l) == 1, temp))[0][0]
        input_line.remove(num2)

        # get all easy numbers
        num1 = filter_num(2, input_line)
        input_line.remove(num1)
        num4 = filter_num(4, input_line)
        input_line.remove(num4)
        num7 = filter_num(3, input_line)
        input_line.remove(num7)
        num8 = filter_num(7, input_line)
        input_line.remove(num8)

        # get not so easy number by seeing how the numbers overlap
        num9 = [num for num in input_line if num != num8 and set(num4) <= set(num)][0]
        input_line.remove(num9)

        num0 = [num for num in input_line if not (num8 - num <= num1) and len(num) == 6][0]
        input_line.remove(num0)

        num6 = filter_num(6, input_line)
        input_line.remove(num6)

        num3 = [num for num in input_line if num1 <= num][0]
        input_line.remove(num3)

        # at last the five is the only number left
        num5 = input_line[0]

        # print(f'{num0=} {num1=} {num2=} {num3=} {num4=} {num5=} {num6=} {num7=} {num8=} {num9=}')

        pattern = {
            num0: 0,
            num1: 1,
            num2: 2,
            num3: 3,
            num4: 4,
            num5: 5,
            num6: 6,
            num7: 7,
            num8: 8,
            num9: 9,
        }

        result.append(int("".join(map(str, map(lambda d: pattern.get(d), output_line)))))

    print(f'{sum(result)=}')


if __name__ == '__main__':
    task2()
