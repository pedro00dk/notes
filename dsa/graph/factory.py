import itertools
import random

from .graph import Graph


def complete(vertices=5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    for v in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
        for target in range(0, v):
            graph.make_edge(v, target, length=random.randint(*el_range))
    return graph


def random_undirected(vertices=5, density=0.5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    for v in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1) / 2)
    for source, target in random.sample([*itertools.combinations([*range(vertices)], 2)], edges):
        graph.make_edge(source, target, length=random.randint(*el_range), directed=False)
    return graph


def random_directed(vertices=5, density=0.5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    for v in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1))
    for source, target in random.sample([*itertools.permutations([*range(vertices)], 2)], edges):
        graph.make_edge(source, target, length=random.randint(*el_range), directed=True)
    return graph


def random_undirected_paired(vertices=5, density=0.5, cycle=True, vw_range=(1, 1), el_range=(1, 1)):
    # paired means all vertices have even degree
    # unrepeated edges and full vertex coverage are not guaranteed
    graph = Graph()
    for v in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1) / 2)
    current = 0
    target = 0
    for i in range(edges):
        target = random.randint(0, vertices - 1)
        graph.make_edge(current, target, length=random.randint(*el_range), directed=False)
        current = target
    if cycle and vertices > 0:
        graph.make_edge(current, 0, length=random.randint(*el_range), directed=False)
    return graph


def random_directed_paired(vertices=5, density=0.5, cycle=True, vw_range=(1, 1), el_range=(1, 1)):
    # paired means all vertices have out_degree - in_degree = 0
    # unrepeated edges and full vertex coverage are not guaranteed
    graph = Graph()
    for v in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1))
    current = 0
    target = 0
    for i in range(edges):
        target = random.randint(0, vertices - 1)
        graph.make_edge(current, target, length=random.randint(*el_range), directed=True)
        current = target
    if cycle and vertices > 0:
        graph.make_edge(current, 0, length=random.randint(*el_range), directed=True)
    return graph


def random_dag(ranks_range=(3, 5), vertices_range=(1, 5), probability=0.5, vw_range=(1, 1), el_range=(1, 1)):
    graph = Graph()
    previous_vertices = []
    ranks = random.randint(*ranks_range)
    for rank in range(ranks):
        rank_vertices_count = random.randint(*vertices_range)
        rank_vertices = [graph.make_vertex()._id for _ in range(rank_vertices_count)]
        for previous_vertex in previous_vertices:
            for rank_vertex in rank_vertices:
                if random.random() < probability:
                    graph.make_edge(previous_vertex, rank_vertex, length=random.randint(*el_range), directed=True)
        previous_vertices.extend(rank_vertices)
    return graph


def random_flow(ranks_range=(3, 5), vertices_range=(1, 5), parent_probability=0.9, sibling_probability=0.2, ancestor_probability=0.1, el_range=(1, 1)):
    graph = Graph()
    ranks_vertices = []
    ranks = random.randint(*ranks_range)
    for rank in range(ranks + 2):
        if rank == 0:
            ranks_vertices.append([graph.make_vertex()._id])
            continue
        rank_vertices_count = random.randint(*vertices_range) if rank < ranks + 1 else 1
        rank_vertices = [graph.make_vertex()._id for _ in range(rank_vertices_count)]
        for rank_vertex in rank_vertices:
            first = True
            # link with parents
            for previous_vertex in random.sample(ranks_vertices[-1], len(ranks_vertices[-1])):
                if first or random.random() < parent_probability:
                    graph.make_edge(previous_vertex, rank_vertex, length=random.randint(*el_range), directed=True)
                first = False
            # link with siblings
            for sibling_vertex in rank_vertices:
                if rank_vertex != sibling_vertex and random.random() < parent_probability:
                    graph.make_edge(sibling_vertex, rank_vertex, length=random.randint(*el_range), directed=True)
            # link with ancestors
            for previous_rank_vertices in ranks_vertices[1:-1]:
                for ancestor_vertex in previous_rank_vertices:
                    if random.random() < ancestor_probability:
                        graph.make_edge(ancestor_vertex, rank_vertex, length=random.randint(*el_range), directed=True)
        ranks_vertices.append(rank_vertices)
    return graph, 0, graph.vertices_count() - 1


def test():
    g = complete(5)
    print(g)
    for vertex in g.vertices():
        print(vertex._id, end=' ')
    print()
    for edge in g.edges():
        print(f'{edge._source}>{edge._target}', end=' ')
    print()
    for vertex, *_ in g.traverse(0, 'dfs'):
        print(vertex._id, end=' ')
    print()
    for vertex, *_ in g.traverse(0, 'bfs'):
        print(vertex._id, end=' ')
    print()
    for i in range(10):
        print('Complete graph:\n', complete(i))
        print('Random undirected Graph:\n', random_undirected(i))
        print('Random directed Graph:\n', random_directed(i))
        print('Random directed Acyclic graph:\n', random_dag((i, i)))


if __name__ == '__main__':
    test()
