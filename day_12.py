from collections import defaultdict
from typing import Iterable

Graph = dict[str, list]

with open("challenges/day_12.txt") as file:
    lines = map(str.strip, file.readlines())


def create_graph(lines_: Iterable[str]) -> Graph:
    graph: Graph = defaultdict(list)
    for a, b in {tuple(line.split("-")) for line in lines_}:
        graph[a].append(b)
        graph[b].append(a)
    return graph


def walk(current: str, graph: Graph) -> list[list[str]]:
    if current == "end":
        return [[current]]
    else:
        # remove current node (only once) if it is a small cave
        graph: Graph = (
            {
                node: [n for n in adjacent if current != n] + [current] * (adjacent.count(current) - 1)
                for node, adjacent in graph.items()
            }
            if current.islower() else graph
        )
        return [[current] + route for pos in graph[current] for route in walk(pos, graph)]


if __name__ == '__main__':
    graph = create_graph(lines)

    no_routes_1 = len(walk("start", graph))
    print(f'{no_routes_1=}')

    # for every small cave (except start/end):
    # create a version of the graph where this cave occurs double, so it can be visited two times
    graphs = (
        # create modified version of graph
        {
            node_: adjacent + [node2x] if node2x in adjacent else adjacent
            for node_, adjacent in graph.items()
        }
        # get every small cave for to double it
        for node2x in {node for node in graph if node.islower()} - {"start", "end"}
    )

    # walk every modified graph and remove duplicate paths at the end
    no_routes_2 = len(set(tuple(path) for g in graphs for path in walk("start", g)))
    print(f'{no_routes_2=}')

    assert no_routes_1 == 5874
    assert no_routes_2 == 153592
