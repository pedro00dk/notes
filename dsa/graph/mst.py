import heapq

from ..dset import DisjointSet
from .graph import Graph


def mst_prim(graph: Graph):
    """
    Prim minimum spanning tree algorithm.

    > complexity:
    - time: `O(e*log(e)) ~> O(e*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find tree

    > `return: (int | float, (int, int, int | float)[])`: tree cost and edges (source, target, length), or `None` if the
        graph contains more than one connected component
    """
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    cost = 0
    edges = []
    visited = [False] * graph.vertices_count()
    heap = []
    for edge in graph.edges(0) if graph.vertices_count() > 0 else ():
        heapq.heappush(heap, (edge.length, float('nan'), edge))  # exploit heapq impl with NaN, stopping comparisons
    if graph.vertices_count() > 0:
        visited[0] = True
    while len(heap) > 0 and len(edges) < graph.vertices_count() - 1:
        _, _, edge = heapq.heappop(heap)
        if visited[edge._target]:
            continue
        visited[edge._target] = True
        cost += edge.length
        edges.append(edge)
        for edge in graph.edges(edge._target):
            if not visited[edge._target]:
                heapq.heappush(heap, (edge.length, float('nan'), edge))
    return (cost, (*((edge._source, edge._target, edge.length) for edge in edges),)) \
        if len(edges) == graph.vertices_count() - 1 else None


def mst_kruskal(graph: Graph):
    """
    Kruskal minimum spanning tree algorithm.

    > complexity:
    - time: `O(e*log(e)) ~> O(e*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find tree

    > `return: (int | float, (int, int, int | float)[])`: tree cost and edges (source, target, length), or `None` if the
        graph contains more than one connected component
    """
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    if graph.vertices_count() < 2:
        return None, ()
    cost = 0
    edges = []
    sorted_edges = [*graph.edges()]
    sorted_edges.sort(key=lambda edge: edge.length)
    disjoint_set = DisjointSet(graph.vertices_count())
    for edge in sorted_edges:
        if len(edges) == graph.vertices_count() - 1:
            break
        if disjoint_set.connected(edge._source, edge._target):
            continue
        cost += edge.length
        edges.append(edge)
        disjoint_set.union(edge._source, edge._target)
    return (cost, (*((edge._source, edge._target, edge.length) for edge in edges),)) \
        if len(edges) == graph.vertices_count() - 1 else None


def mst_boruvka(graph: Graph):
    """
    Boruvka minimum spanning tree algorithm.

    > complexity:
    - time: `O((v + e)*log(v)) ~> O(e*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find tree

    > `return: (int | float, (int, int, int | float)[])`: tree cost and edges (source, target, length), or `None` if the
        graph contains more than one connected component
    """
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    if graph.vertices_count() < 2:
        return None, ()
    cost = 0
    edges = []
    disjoint_set = DisjointSet(graph.vertices_count())
    shortest_edges = [None] * graph.vertices_count()
    while disjoint_set.sets() > 1:
        for edge in graph.edges():
            if disjoint_set.connected(edge._source, edge._target):
                continue
            source_set = disjoint_set.find(edge._source)
            target_set = disjoint_set.find(edge._target)
            if shortest_edges[source_set] is None or edge.length < shortest_edges[source_set].length:
                shortest_edges[source_set] = edge
            if shortest_edges[target_set] is None or edge.length < shortest_edges[target_set].length:
                shortest_edges[target_set] = edge
        for v in range(graph.vertices_count()):
            shortest_edge = shortest_edges[v]
            if shortest_edge is None or disjoint_set.connected(shortest_edge._source, shortest_edge._target):
                continue
            edges.append(shortest_edge)
            cost += shortest_edge.length
            disjoint_set.union(shortest_edge._source, shortest_edge._target)
        shortest_edges = [None] * graph.vertices_count()
    return (cost, (*((edge._source, edge._target, edge.length) for edge in edges),)) \
        if len(edges) == graph.vertices_count() - 1 else None


def test():
    from ..test import benchmark
    from .factory import complete
    benchmark(
        [
            ('   mst prim', mst_prim),
            ('mst kruskal', mst_kruskal),
            ('mst boruvka', mst_boruvka)
        ],
        test_input_iter=(complete(i, el_range=(0, 100)) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100, 1000),
        bench_input=(lambda s, r: complete(s, el_range=(0, 100)))
    )


if __name__ == '__main__':
    test()
