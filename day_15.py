import sys
from heapq import heappush, heappop

from func import neighbors_sq, position, height, width

Matrix = list[list[int]]
Path = list[tuple[int, int]]

with open("challenges/day_15.txt") as file:
    matrix = [[int(x) for x in line.strip()] for line in file.readlines()]


def dijkstra(matrix_: Matrix, start_index: tuple[int, int], end_index: tuple[int, int]) -> int:
    distances = {start_index: 0}
    visited = set()
    heap = []
    heappush(heap, (distances[start_index], start_index))

    while heap and end_index not in distances:
        (dist, pos) = heappop(heap)
        visited.add(pos)
        for neighbor_pos in neighbors_sq(matrix_, *pos):
            distance = position(matrix_, *neighbor_pos)
            if neighbor_pos not in visited:
                new_cost = distances[pos] + distance
                if new_cost < distances.get(neighbor_pos, sys.maxsize):
                    heappush(heap, (new_cost, neighbor_pos))
                    distances[neighbor_pos] = new_cost

    return distances[end_index]


def expand_matrix(matrix_: Matrix, factor=5) -> Matrix:
    h, w = height(matrix_), width(matrix_)

    incr_ = lambda i: i + 1 if i < 9 else 1

    # new matrix
    new = [[0 for _ in range(w * factor)] for _ in range(h * factor)]

    # copy old
    for y in range(h):
        for x in range(w):
            new[y][x] = position(matrix_, x, y)

    # fill first "row"
    for y in range(h):
        for x in range(w, w * factor):
            new[y][x] = incr_(position(new, x - w, y))

    # fill rest
    for y in range(h, h * factor):
        for x in range(w * factor):
            new[y][x] = incr_(position(new, x, y - h))

    return new


if __name__ == '__main__':
    start = (0, 0)
    end = (width(matrix) - 1, height(matrix) - 1)

    task1 = dijkstra(matrix, start, end)
    print(f'{task1=}')

    expanded_matrix = expand_matrix(matrix)
    end = (width(expanded_matrix) - 1, height(expanded_matrix) - 1)
    task2 = dijkstra(expanded_matrix, start, end)
    print(f'{task2=}')
