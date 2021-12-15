from toolz.curried import *

with open("challenges/day_14_test.txt") as file:
    start, _ = file.readline().strip(), file.readline()
    rules = map(str.strip, file.readlines())

    rules = {rule.split(" -> ")[0]: rule.split(" -> ")[1] for rule in rules}


def naive():
    rules_ = {key: key[0] + val + key[1] for key, val in rules.items()}
    string = start

    for i in range(10):
        new = string[0]
        for c1, c2 in sliding_window(2, string):
            new += rules_[c1 + c2][1:]
        string = new

    occurrences = list((times, char) for char, times in frequencies(string).items())
    print(first(max(occurrences)) - first(min(occurrences)))


if __name__ == '__main__':
    ...
