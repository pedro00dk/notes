import itertools
import random

from .graph import Graph


def complete(vertices=5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    for vertex in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
        for target in range(0, vertex):
            graph.make_edge(vertex, target, length=random.randint(*el_range))
    return graph


def random_undirected(vertices=5, density=0.5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    for vertex in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1) / 2)
    for source, target in random.sample([*itertools.combinations(range(vertices), 2)], edges):
        graph.make_edge(source, target, length=random.randint(*el_range), directed=False)
    return graph


def random_directed(vertices=5, density=0.5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    for vertex in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1))
    for source, target in random.sample([*itertools.permutations(range(vertices), 2)], edges):
        graph.make_edge(source, target, length=random.randint(*el_range), directed=True)
    return graph


def random_dag(ranks_range=(3, 5), vertices_range=(1, 5), probability=0.5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    ranks = random.randint(*ranks_range)
    previous_vertices = 0
    for rank in range(ranks):
        vertices = random.randint(*vertices_range)
        for vertice in range(previous_vertices, vertices + previous_vertices):
            graph.make_vertex(weight=random.randint(*vw_range))
        for previous in range(previous_vertices):
            for vertice in range(previous_vertices, vertices + previous_vertices):
                if random.random() < probability:
                    graph.make_edge(previous, vertice, length=random.randint(*el_range), directed=True)
        previous_vertices += vertices
    return graph


def test():
    g = complete(5)
    print(g)
    for vertex in g.vertices():
        print(vertex._id, end=' ')
    print()
    for edge in g.edges():
        print(f'{edge._source}>{edge._target}', end=' ')
    print()
    for vertex, parent, edge, depth in g.traverse(0, 'dfs'):
        print(vertex._id, end=' ')
    print()
    for vertex, parent, edge, depth in g.traverse(0, 'bfs'):
        print(vertex._id, end=' ')
    print()
    for i in range(10):
        print('Complete graph:\n', complete(i))
        print('Random undirected Graph:\n', random_undirected(i))
        print('Random directed Graph:\n', random_directed(i))
        print('Random directed Acyclic graph:\n', random_dag((i, i)))


if __name__ == '__main__':
    test()
