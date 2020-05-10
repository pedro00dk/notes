from .factory import *


def topological_sort(graph: Graph):
    if not graph.is_directed():
        raise Exception('topological sort only works with directed acyclic graphs')
    order = []
    visited = [False] * graph.vertices_length()
    for source in graph.vertices():
        if visited[source._id]:
            continue
        for vertex, *_ in graph.traverse(source._id, visited=visited, yield_after=True):
            order.append(vertex)
    order.reverse()
    return order


def test():
    for i in range(10):
        g = random_dag()
        print(g)
        print([vertex._id for vertex in topological_sort(g)])
        print('\n')


if __name__ == '__main__':
    test()
