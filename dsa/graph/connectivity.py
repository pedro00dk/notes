from ..disjoint_set import DisjointSet
from .factory import *


def connected(graph: Graph):
    if graph.is_directed():
        raise Exception('connected algorithm does not work with directed graphs')
    visited = [False] * len(graph)
    groups = [None] * len(graph)
    if graph.vertices_length() == 0:
        return groups
    group = 0
    for source in graph.vertices():
        if visited[source._id]:
            continue
        for vertex, *_ in graph.traverse(source._id, visited=visited):
            groups[vertex._id] = group
        group += 1
    return group, groups


def test():
    for i in range(10):
        g = random_undirected(20, 0.1)
        print(g)
        print(connected(g))
        print('\n')


if __name__ == '__main__':
    test()
