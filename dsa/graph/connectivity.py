from ..disjoint_set import DisjointSet
from .factory import *


def connected(graph: Graph):
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    visited = [False] * len(graph)
    groups = []
    for source in graph.vertices():
        if visited[source._id]:
            continue
        groups.append([vertex for vertex, *_ in graph.traverse(source._id, visited=visited)])
    return groups


def test():
    for i in range(10):
        g = random_undirected(20, 0.1)
        print(g)
        print([[vertex._id for vertex in group] for group in connected(g)])
        print('\n')


if __name__ == '__main__':
    test()
