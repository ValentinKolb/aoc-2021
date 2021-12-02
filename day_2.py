import re

DOWN, UP, FORWARD = int, int, int

regex_down = r'^down (?P<num>[0-9]+)'
regex_up = r'^up (?P<num>[0-9]+)'
regex_forward = r'^forward (?P<num>[0-9]+)'

pos_x = 0
pos_y = 0
aim = 0

with open("challenges/day_2.txt") as file:
    challenge = file.readlines()


def get_measurements(line: str) -> (UP, DOWN, FORWARD):
    num = lambda m: int(m.group("num"))
    if match := re.match(regex_down, line):
        return 0, num(match), 0
    elif match := re.match(regex_up, line):
        return num(match), 0, 0
    elif match := re.match(regex_forward, line):
        return 0, 0, num(match)
    return 0, 0, 0


if __name__ == '__main__':

    for line in challenge:
        up, down, forward = get_measurements(line)

        # pos_y += down
        # pos_y -= up
        pos_x += forward

        aim += down
        aim -= up
        pos_y += aim * forward

    print(pos_x * pos_y)
