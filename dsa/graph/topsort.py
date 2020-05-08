from .graph import Graph


def topsort(graph: Graph):
    order = []
    visited = [False] * len(graph)
    for vertex in range(len(graph)):
        if visited[vertex]:
            continue
        for traverse_vertex, previous, *_ in graph.traverse(vertex, visited=visited, before=False):
            order.append(traverse_vertex)
    order.reverse()
    return order


def test():
    for i in range(10):
        g = Graph.random_dag()
        print(g)
        print(topsort(g))
        print('\n')


if __name__ == '__main__':
    test()
