from .graph import Graph


def topological_sort(graph):
    order = []
    visited = [False] * len(graph)
    for source in range(len(graph)):
        if visited[source]:
            continue
        for traverse_vertex, previous, *_ in graph.traverse(source, visited=visited, before=False):
            order.append(traverse_vertex)
    order.reverse()
    return order


def test():
    for i in range(10):
        g = Graph.random_dag()
        print(g)
        print(topological_sort(g))
        print('\n')


if __name__ == '__main__':
    test()
