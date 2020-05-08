from ..disjoint_set import DisjointSet
from .graph import Graph


def connected(graph):
    visited = [False] * len(graph)
    groups = [None] * len(graph)
    if len(graph) == 0:
        return groups
    group = 0
    for vertex in range(len(graph)):
        if visited[vertex]:
            continue
        for vertex, previous, *_ in graph.traverse(vertex, visited=visited):
            groups[vertex] = group
        group += 1
    return group, groups


def test():
    for i in range(10):
        g = Graph.random(20, 0.1)
        print(g)
        print(connected(g))
        print('\n')


if __name__ == '__main__':
    test()
