import itertools
import random

from .graph import Graph


def complete(
    vertices: int = 5,
    vw_range: tuple[int, int] = (1, 1),
    el_range: tuple[int, int] = (1, 1),
) -> Graph[None, None]:
    graph = Graph[None, None]()
    for v in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
        for target in range(0, v):
            graph.make_edge(v, target, length=random.randint(*el_range))
    return graph


def random_undirected(
    vertices: int = 5, density: float = 0.5, vw_range: tuple[int, int] = (1, 1), el_range: tuple[int, int] = (1, 1)
) -> Graph[None, None]:
    graph = Graph[None, None]()
    for _ in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1) / 2)
    for source, target in random.sample([*itertools.combinations([*range(vertices)], 2)], edges):
        graph.make_edge(source, target, length=random.randint(*el_range), directed=False)
    return graph


def random_directed(
    vertices: int = 5,
    density: float = 0.5,
    vw_range: tuple[int, int] = (1, 1),
    el_range: tuple[int, int] = (1, 1),
) -> Graph[None, None]:
    graph = Graph[None, None]()
    for _ in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1))
    for source, target in random.sample([*itertools.permutations([*range(vertices)], 2)], edges):
        graph.make_edge(source, target, length=random.randint(*el_range), directed=True)
    return graph


def random_undirected_paired(
    vertices: int = 5,
    density: float = 0.5,
    cycle: bool = True,
    vw_range: tuple[int, int] = (1, 1),
    el_range: tuple[int, int] = (1, 1),
) -> Graph[None, None]:
    # paired means all vertices have even degree
    # unrepeated edges and full vertex coverage are not guaranteed
    graph = Graph[None, None]()
    for _ in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1) / 2)
    current = 0
    target = 0
    for _ in range(edges):
        target = random.randint(0, vertices - 1)
        graph.make_edge(current, target, length=random.randint(*el_range), directed=False)
        current = target
    if cycle and vertices > 0:
        graph.make_edge(current, 0, length=random.randint(*el_range), directed=False)
    return graph


def random_directed_paired(
    vertices: int = 5,
    density: float = 0.5,
    cycle: bool = True,
    vw_range: tuple[int, int] = (1, 1),
    el_range: tuple[int, int] = (1, 1),
) -> Graph[None, None]:
    # paired means all vertices have out_degree - in_degree = 0
    # unrepeated edges and full vertex coverage are not guaranteed
    graph = Graph[None, None]()
    for _ in range(vertices):
        graph.make_vertex(weight=random.randint(*vw_range))
    edges = round(min(max(0, density), 1) * vertices * (vertices - 1))
    current = 0
    target = 0
    for _ in range(edges):
        target = random.randint(0, vertices - 1)
        graph.make_edge(current, target, length=random.randint(*el_range), directed=True)
        current = target
    if cycle and vertices > 0:
        graph.make_edge(current, 0, length=random.randint(*el_range), directed=True)
    return graph


def random_dag(
    ranks_range: tuple[int, int] = (3, 5),
    vertices_range: tuple[int, int] = (1, 5),
    probability: float = 0.5,
    vw_range: tuple[int, int] = (1, 1),
    el_range: tuple[int, int] = (1, 1),
) -> Graph[None, None]:
    graph = Graph[None, None]()
    previous_vertices: list[int] = []
    ranks = random.randint(*ranks_range)
    for _ in range(ranks):
        rank_vertices_count = random.randint(*vertices_range)
        rank_vertices = [graph.make_vertex(random.randint(*vw_range)).id for _ in range(rank_vertices_count)]
        for previous_vertex in previous_vertices:
            for rank_vertex in rank_vertices:
                if random.random() < probability:
                    graph.make_edge(previous_vertex, rank_vertex, length=random.randint(*el_range), directed=True)
        previous_vertices.extend(rank_vertices)
    return graph


def random_flow(
    ranks_range: tuple[int, int] = (3, 5),
    vertices_range: tuple[int, int] = (1, 5),
    parent_probability: float = 0.9,
    sibling_probability: float = 0.2,
    ancestor_probability: float = 0.1,
    vw_range: tuple[int, int] = (1, 1),
    el_range: tuple[int, int] = (1, 1),
) -> tuple[Graph[None, None], int, int]:
    graph = Graph[None, None]()
    ranks_vertices: list[list[int]] = []
    ranks = random.randint(*ranks_range)
    for rank in range(ranks + 2):
        if rank == 0:
            ranks_vertices.append([graph.make_vertex(random.randint(*vw_range)).id])
            continue
        rank_vertices_count = random.randint(*vertices_range) if rank < ranks + 1 else 1
        rank_vertices = [graph.make_vertex().id for _ in range(rank_vertices_count)]
        for rank_vertex in rank_vertices:
            first = True
            # link with parents
            for previous_vertex in random.sample(ranks_vertices[-1], len(ranks_vertices[-1])):
                if first or random.random() < parent_probability:
                    graph.make_edge(previous_vertex, rank_vertex, length=random.randint(*el_range), directed=True)
                first = False
            # link with siblings
            for sibling_vertex in rank_vertices:
                if rank_vertex != sibling_vertex and random.random() < sibling_probability:
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
        print(vertex.id, end=" ")
    print()
    for edge in g.edges():
        print(f"{edge.source}>{edge.target}", end=" ")
    print()
    for vertex, *_ in g.traverse(0, "depth"):
        print(vertex.id, end=" ")
    print()
    for vertex, *_ in g.traverse(0, "breadth"):
        print(vertex.id, end=" ")
    print()
    for i in range(1, 11, 3):
        print("Complete graph:\n", complete(i))
        print("random undirected Graph:\n", random_undirected(i))
        print("random directed Graph:\n", random_directed(i))
        print("random undirected paired Graph:\n", random_undirected_paired(i))
        print("random directed paired Graph:\n", random_directed_paired(i))
        print("random directed Acyclic graph:\n", random_dag((i, i)))
        print("random flow graph:\n", random_flow((i, i))[0])


if __name__ == "__main__":
    test()
