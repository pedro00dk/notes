import heapq
from typing import Any, Optional, cast

from ..dset import DisjointSet
from .graph import Edge, Graph


def mst_prim(graph: Graph[Any, Any]) -> Optional[tuple[float, list[tuple[int, int, float]]]]:
    """
    Prim minimum spanning tree algorithm.

    > complexity
    - time: `O(e*log(e)) ~> O(e*log(v))`
    - space: `O(v + e)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph: Graph`: graph to find tree
    - `return`: tree cost and edges (source, target, length), or `None` if the graph contains more than one component
    """
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    cost = 0
    edges: list[Edge[Any]] = []
    visited = [False] * graph.vertices_count()
    heap: list[tuple[float, float, Edge[Any]]] = []
    for edge in graph.edges(0) if graph.vertices_count() > 0 else ():
        heapq.heappush(heap, (edge.length, float('nan'), edge))  # exploit heapq impl with NaN, stopping comparisons
    if graph.vertices_count() > 0:
        visited[0] = True
    while len(heap) > 0 and len(edges) < graph.vertices_count() - 1:
        _, _, edge = heapq.heappop(heap)
        if visited[edge.target]:
            continue
        visited[edge.target] = True
        cost += edge.length
        edges.append(edge)
        for edge in graph.edges(edge.target):
            if not visited[edge.target]:
                heapq.heappush(heap, (edge.length, float('nan'), edge))
    return (cost, [(edge.source, edge.target, edge.length) for edge in edges]) \
        if len(edges) == graph.vertices_count() - 1 else None


def mst_kruskal(graph: Graph[Any, Any]) -> Optional[tuple[float, list[tuple[int, int, float]]]]:
    """
    Kruskal minimum spanning tree algorithm.

    > complexity
    - time: `O(e*log(e)) ~> O(e*log(v))`
    - space: `O(v + e)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find tree
    - `return`: tree cost and edges (source, target, length), or `None` if the graph contains more than one component
    """
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    cost = 0
    edges: list[Edge[Any]] = []
    sorted_edges = [*graph.edges()]
    sorted_edges.sort(key=lambda edge: edge.length)
    disjoint_set = DisjointSet(graph.vertices_count())
    for edge in sorted_edges:
        if len(edges) == graph.vertices_count() - 1:
            break
        if disjoint_set.connected(edge.source, edge.target):
            continue
        cost += edge.length
        edges.append(edge)
        disjoint_set.union(edge.source, edge.target)
    return (cost, [(edge.source, edge.target, edge.length) for edge in edges]) \
        if len(edges) == graph.vertices_count() - 1 else None


def mst_boruvka(graph: Graph[Any, Any]) -> Optional[tuple[float, list[tuple[int, int, float]]]]:
    """
    Boruvka minimum spanning tree algorithm.

    > complexity
    - time: `O((v + e)*log(v)) ~> O(e*log(v))`
    - space: `O(v + e)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find tree
    - `return`: tree cost and edges (source, target, length), or `None` if the graph contains more than one component
    """
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    cost = 0
    edges: list[Edge[Any]] = []
    disjoint_set = DisjointSet(graph.vertices_count())
    shortest_edges = cast(list[Optional[Edge[Any]]], [None] * graph.vertices_count())
    found_union = True
    while disjoint_set.sets() > 1 and found_union:
        found_union = False
        for edge in graph.edges():
            if disjoint_set.connected(edge.source, edge.target):
                continue
            source_set = disjoint_set.find(edge.source)
            target_set = disjoint_set.find(edge.target)
            shortest_source_edge = shortest_edges[source_set]
            shortest_target_edge = shortest_edges[source_set]
            if shortest_source_edge is None or edge.length < shortest_source_edge.length:
                shortest_edges[source_set] = edge
            if shortest_target_edge is None or edge.length < shortest_target_edge.length:
                shortest_edges[target_set] = edge
        for v in range(graph.vertices_count()):
            shortest_edge = shortest_edges[v]
            if shortest_edge is None or disjoint_set.connected(shortest_edge.source, shortest_edge.target):
                continue
            edges.append(shortest_edge)
            cost += shortest_edge.length
            disjoint_set.union(shortest_edge.source, shortest_edge.target)
            found_union = True
        shortest_edges = cast(list[Optional[Edge[Any]]], [None] * graph.vertices_count())
    return (cost, [(edge.source, edge.target, edge.length) for edge in edges]) \
        if len(edges) == graph.vertices_count() - 1 else None


def test():
    from ..test import benchmark
    from .factory import complete
    benchmark(
        (
            ('   mst prim', mst_prim),
            ('mst kruskal', mst_kruskal),
            ('mst boruvka', mst_boruvka),
        ),
        test_inputs=(*(complete(i, el_range=(0, 100)) for i in (5, 10, 15, 20)),),
        bench_sizes=(0, 1, 10, 100),
        bench_input=(lambda s: complete(s, el_range=(0, 100))),
    )


if __name__ == '__main__':
    test()
