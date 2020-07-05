import heapq

from ..dset import DisjointSet
from .graph import Graph


def mst_prim(graph: Graph):
    """
    Prim's minimum spanning tree algorithm.

    > complexity:
    - time: `O(e*log(e)) ~> O(e*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find tree

    > `return: (int | float, (int, int, int | float)[])`: the best distance and the tree edges (source, target, length)
    """
    if not graph.is_undirected():
        raise Exception('minimum spanning tree algorithm only works with undirected graphs')
    if graph.vertices_count() < 2:
        return None, ()
    start = 0
    tree_cost = 0
    tree_edges = []
    visited = [False] * graph.vertices_count()
    heap = []
    for edge in graph.edges(start):
        # nan is used to exploit heapq impl by stopping comparisons before the edge object (all nan comps return false)
        heapq.heappush(heap, (edge.length, float('nan'), edge))
    visited[start] = True
    while len(heap) > 0 and len(tree_edges) < graph.vertices_count() - 1:
        length, _, edge = heapq.heappop(heap)
        if visited[edge._target]:
            continue
        tree_edges.append(edge)
        tree_cost += length
        for edge in graph.edges(edge._target):
            if not visited[edge._target]:
                heapq.heappush(heap, (edge.length, float('nan'), edge))
        visited[edge._source] = True
    return (tree_cost, (*((edge._source, edge._target, edge.length) for edge in tree_edges),)) \
        if len(tree_edges) == graph.vertices_count() - 1 else (None, ())


def mst_kruskal(graph: Graph):
    """
    Kruskal's minimum spanning tree algorithm.

    > complexity:
    - time: `O(e*log(e)) ~> O(e*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find tree

    > `return: (int | float, (int, int, int | float)[])`: the best distance and the tree edges (source, target, length)
    """
    if not graph.is_undirected():
        raise Exception('minimum spanning tree algorithm only works with undirected graphs')
    if graph.vertices_count() < 2:
        return None, ()
    tree_cost = 0
    tree_edges = []
    sorted_edges = [*graph.edges()]
    sorted_edges.sort(key=lambda edge: edge.length)
    disjoint_set = DisjointSet(graph.vertices_count())
    for edge in sorted_edges:
        if len(tree_edges) == graph.vertices_count() - 1:
            break
        if disjoint_set.connected(edge._source, edge._target):
            continue
        tree_edges.append(edge)
        tree_cost += edge.length
        disjoint_set.union(edge._source, edge._target)
    return (tree_cost, (*((edge._source, edge._target, edge.length) for edge in tree_edges),)) \
        if len(tree_edges) == graph.vertices_count() - 1 else (None, ())


def mst_boruvka(graph: Graph):
    """
    Boruvka's minimum spanning tree algorithm.

    > complexity:
    - time: `O((v + e)*log(v)) ~> O(e*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find tree

    > `return: (int | float, (int, int, int | float)[])`: the best distance and the tree edges (source, target, length)
    """
    if not graph.is_undirected():
        raise Exception('minimum spanning tree algorithm only works with undirected graphs')
    if graph.vertices_count() < 2:
        return None, ()
    tree_cost = 0
    tree_edges = []
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
            tree_edges.append(shortest_edge)
            tree_cost += shortest_edge.length
            disjoint_set.union(shortest_edge._source, shortest_edge._target)
        shortest_edges = [None] * graph.vertices_count()
    return (tree_cost, (*((edge._source, edge._target, edge.length) for edge in tree_edges),)) \
        if len(tree_edges) == graph.vertices_count() - 1 else (None, ())


def test():
    from ..test import benchmark
    from .factory import complete
    benchmark(
        [
            ('  mst prim', mst_prim),
            ('mst kruskal', mst_kruskal),
            ('mst boruvka', mst_boruvka)
        ],
        test_input_iter=(complete(i, el_range=(0, 100)) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100, 1000),
        bench_input=(lambda s, r: complete(s, el_range=(0, 100)))
    )


if __name__ == '__main__':
    test()
