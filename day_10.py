from func import *
from functools import reduce

with open("challenges/day_10.txt") as file:
    lines = map(strip, file.readlines())

syntax_checker_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

autocomplete_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

brackets = {
    "(": ")",
    "{": "}",
    "[": "]",
    "<": ">"
}


def solution():
    invalid = []
    missing = []
    for line in lines:
        symbols = []
        for symbol in line:
            # case closing bracket missing
            if symbol not in brackets:
                if symbol != brackets[symbols[-1]]:
                    invalid.append(symbol)
                    break
                else:
                    symbols.pop(-1)
            else:
                symbols.append(symbol)
        else:
            # case incomplete
            missing.append([brackets.get(symbol) for symbol in reversed(symbols)])

    score_task_1 = sum(map(lambda s: syntax_checker_scores[s], invalid))

    scores_task_2 = sorted(
        reduce(lambda x, y: x * 5 + y, (autocomplete_scores[s] for s in line), 0) for line in missing)
    score_task_2 = scores_task_2[len(scores_task_2) // 2]

    print(f'{score_task_1=}')
    print(f'{score_task_2=}')

    assert score_task_1 == 271245
    assert score_task_2 == 1685293086


if __name__ == '__main__':
    solution()
