from statistics import mean

with open("challenges/day_1.txt") as file:
    challenge = file.readlines()
challenge = [int(line) for line in challenge]


def count_inc(l: list):
    return sum(1 for prev, next_ in zip(l, l[1:]) if prev < next_)


def window_means(l: list, window_size=3):
    return [mean(l[i:i + window_size]) for i in range(len(l) - (window_size - 1))]


if __name__ == '__main__':
    print(count_inc(window_means(challenge)))
