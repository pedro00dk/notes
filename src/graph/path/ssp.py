import heapq
from typing import Any, Optional, cast

from ..graph import Graph
from ..topsort import topsort_dfs


def sssp_dag(graph: Graph[Any, Any], start: int) -> list[tuple[float, int]]:
    """
    Single source shortest path for directed acyclic graphs.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters
    - `graph`: graph to compute single source shortest path
    - `start`: vertex to compute distances from
    - `return`: distances array containing distances to `start` and `parent`
    """
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    distances = cast(list[tuple[float, int]], [(float('inf'), None)] * graph.vertices_count())
    distances[start] = (0, start)
    for v in topsort_dfs(graph):
        vertex_distance, _ = distances[v]
        for edge in graph.edges(v):
            target_distance = vertex_distance + edge.length
            if target_distance < distances[edge.target][0]:
                distances[edge.target] = (target_distance, v)
    return distances


def sslp_dag(graph: Graph[Any, Any], start: int) -> list[tuple[float, int]]:
    """
    Single source longest path for directed acyclic graphs.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters
    - `graph`: graph to compute single source shortest path
    - `start`: vertex to compute distances from
    - `return`: distances array containing distances to `start` and `parent` 
    """
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    distances = cast(list[tuple[float, int]], [(float('inf'), None)] * graph.vertices_count())
    distances[start] = (0, start)
    for v in topsort_dfs(graph):
        vertex_distance, _ = distances[v]
        for edge in graph.edges(v):
            target_distance = vertex_distance - edge.length
            if target_distance < distances[edge.target][0]:
                distances[edge.target] = (target_distance, v)
    distances[:] = ((-distance if distance < float('inf') else float('inf'), parent) for distance, parent in distances)
    return distances


def sssp_dijkstra(graph: Graph[Any, Any], start: int, end: Optional[int] = None) -> list[tuple[float, int]]:
    """
    Dijkstra single source shortest path algorithm.
    Dijkstra does not support graphs with negative edge lengths (except if the graph does not contain negative cycles).

    > complexity
    - time: `O((v + e)*log(v)) ~> O(e*log(v))`
    - space: `O(v + e)`

    > parameters
    - `graph`: graph to compute single source shortest path
    - `start`: vertex to compute distances from
    - `end`: vertex to stop computation
    - `return`: distances array containing distances to `start` and `parent` 
    """
    if start < 0 or start >= graph.vertices_count() or end is not None and (end < 0 or end > graph.vertices_count()):
        raise IndexError(f'start ({start}) or end ({end}) vertex out of range [0, {graph.vertices_count()})')
    distances = cast(list[tuple[float, int]], [(float('inf'), None)] * graph.vertices_count())
    distances[start] = (0, start)
    heap = [distances[start]]
    while len(heap) > 0:
        distance, v = heapq.heappop(heap)
        if v == end:
            break
        for edge in graph.edges(v):
            target_distance = distance + edge.length
            if target_distance < distances[edge.target][0]:
                distances[edge.target] = (target_distance, v)
                heapq.heappush(heap, (target_distance, edge.target))
    return distances


def sssp_dijkstra_opt(graph: Graph[Any, Any], start: int, end: Optional[int] = None) -> list[tuple[float, int]]:
    """
    Check base dijkstra algorithm for documentation.

    > optimizations
    - use `visited´ array to avoid checking already visited edges
    - skip stale heap pairs by checking against current distance before iterating through edges
    """
    if start < 0 or start >= graph.vertices_count() or end is not None and (end < 0 or end > graph.vertices_count()):
        raise IndexError(f'start ({start}) or end ({end}) vertex out of range [0, {graph.vertices_count()})')
    distances = cast(list[tuple[float, int]], [(float('inf'), None)] * graph.vertices_count())
    distances[start] = (0, start)
    heap = [distances[start]]
    visited = [False] * graph.vertices_count()
    while len(heap) > 0:
        distance, v = heapq.heappop(heap)
        visited[v] = True
        if v == end:
            break
        if distance > distances[v][0]:
            continue
        for edge in graph.edges(v):
            if visited[edge.target]:
                continue
            target_distance = distance + edge.length
            if target_distance < distances[edge.target][0]:
                distances[edge.target] = (target_distance, v)
                heapq.heappush(heap, (target_distance, edge.target))
    return distances


def sssp_bellman_ford(
    graph: Graph[Any, Any],
    start: int,
    check_negative_cycles: bool = True,
) -> list[tuple[float, int]]:
    """
    Bellman Ford single source longest path algorithm.

    > complexity
    - time: `O(v*e)`
    - space: `O(v)`

    > parameters
    - `graph`: graph to compute single source shortest path
    - `start`: vertex to compute distances from
    - `check_negative_cycles`: check negative cycles and set their distances to negative infinity, not necessary if all
        edges have positive length
    - `return`: distances array containing distances to `start` and `parent` 
    """
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    distances = cast(list[tuple[float, int]], [(float('inf'), None)] * graph.vertices_count())
    distances[start] = (0, start)
    for _ in range(graph.vertices_count() - 1):
        for edge in graph.edges():
            target_distance = distances[edge.source][0] + edge.length
            if target_distance < distances[edge.target][0]:
                distances[edge.target] = (target_distance, edge.source)
    if check_negative_cycles:
        for _ in range(graph.vertices_count() - 1):
            for edge in graph.edges():
                target_distance = distances[edge.source][0] + edge.length
                if target_distance < distances[edge.target][0]:
                    distances[edge.target] = (float('-inf'), edge.source)
    return distances


def apsp_floyd_warshall(
    graph: Graph[Any, Any],
    check_negative_cycles: bool = True
) -> tuple[list[list[float]], list[list[int]]]:
    """
    Floyd Warshall all-pairs shortest path algorithm.

    > complexity
    - time: `O(v**3)`
    - space: `O(v**2)`

    > parameters
    - `graph`: graph to compute single source shortest path
    - `check_negative_cycles`: check negative cycles and set their distances to negative infinity, not necessary if all
        edges have positive length
    - `return`: distances and parents matrices,
        distances[i][j] contains the shortest distances from the vertex i to a vertex,
        parents contains the parents for each pair path (see `floyd_warshall_rebuild_path`)
    """
    if graph.vertices_count() == 0:
        raise Exception('graph must contain at least 1 vertex')
    inf = float('inf')
    matrix = graph.adjacency_matrix()
    distances = matrix
    parents = cast(list[list[int]], [[None] * graph.vertices_count() for _ in range(graph.vertices_count())])
    for i in range(graph.vertices_count()):
        for j in range(graph.vertices_count()):
            if distances[i][j] != inf:
                parents[i][j] = j
    for k in range(graph.vertices_count()):
        for i in range(graph.vertices_count()):
            for j in range(graph.vertices_count()):
                new_path = distances[i][k] + distances[k][j]
                if new_path >= distances[i][j]:
                    continue
                distances[i][j] = new_path
                parents[i][j] = parents[i][k]
    if check_negative_cycles:
        for k in range(graph.vertices_count()):
            for i in range(graph.vertices_count()):
                for j in range(graph.vertices_count()):
                    new_path = distances[i][k] + distances[k][j]
                    if new_path >= distances[i][j]:
                        continue
                    distances[i][j] = -inf
                    parents[i][j] = -1
    return distances, parents


def floyd_warshall_rebuild_path(
    distances: list[list[float]],
    parents: list[list[int]],
    start: int,
    end: int,
) -> tuple[float, Optional[list[int]]]:
    """
    Rebuild the path between `start` and `end` from the `distances` and `parents` provided by the `apsp_floyd_warshall`
    algorithm.

    > complexity
    - time: `O(v)`
    - space: `O(v)`

    > parameters
    - `distances`: floyd warshall distances matrix
    - `parents`: floyd warshall parents matrix
    - `start`: vertex to compute distances from
    - `end`: vertex to stop computation
    - `return`: distance from `start` to `end` and the path between them,
        if path is empty, then there is no path between `start` and `end`,
        or if path is `None`, there is a negative cycle between `start` and `end`
    """
    if start < 0 or start >= len(distances) or end is not None and end < 0 or end > len(distances):
        raise IndexError(f'start ({start}) or end ({end}) vertex out of range [0, {len(distances)})')
    path: list[int] = []
    if distances[start][end] == float('inf'):
        return float('inf'), path
    current = start
    while True:
        if current == -1:
            return -float('inf'), None
        path.append(current)
        if current == end:
            break
        current = parents[current][end]
    path.reverse()
    return distances[start][end], path


def test():
    from ...test import benchmark
    from ..factory import random_dag, random_directed, random_undirected

    print('directed acyclic graphs')
    benchmark(
        (
            ('           sssp dag', lambda graph: sssp_dag(graph, 0)),
            ('           sslp dag', lambda graph: sslp_dag(graph, 0)),
            ('      sssp dijkstra', lambda graph: sssp_dijkstra(graph, 0)),
            ('  sssp dijkstra opt', lambda graph: sssp_dijkstra_opt(graph, 0)),
            ('  sssp bellman ford', lambda graph: sssp_bellman_ford(graph, 0)),
            ('apsp floyd warshall', lambda graph: apsp_floyd_warshall(graph)[0][0]),
        ),
        test_inputs=(*(random_dag(el_range=(-10, 15)) for _ in range(3)),),
        bench_sizes=(1, 10, 100),
        bench_input=lambda s: random_dag((max(s // 4, 1), max(s // 3, 1)), (3, 4), el_range=(-10, 15)),
    )
    print('undirected graphs')
    benchmark(
        (
            ('      sssp dijkstra', lambda graph: sssp_dijkstra(graph, 0)),
            ('  sssp dijkstra opt', lambda graph: sssp_dijkstra_opt(graph, 0)),
            ('  sssp bellman ford', lambda graph: sssp_bellman_ford(graph, 0)),
            ('apsp floyd warshall', lambda graph: apsp_floyd_warshall(graph)[0][0]),
        ),
        test_inputs=(*(random_undirected(10, el_range=(1, 10)) for _ in range(3)),),
        bench_sizes=(1, 10, 100),
        bench_input=lambda s: random_undirected(s, el_range=(1, 10)),
    )
    print('directed graphs')
    benchmark(
        (
            ('      sssp dijkstra', lambda graph: sssp_dijkstra(graph, 0)),
            ('  sssp dijkstra opt', lambda graph: sssp_dijkstra_opt(graph, 0)),
            ('  sssp bellman ford', lambda graph: sssp_bellman_ford(graph, 0)),
            ('apsp floyd warshall', lambda graph: apsp_floyd_warshall(graph)[0][0]),
        ),
        test_inputs=(*(random_directed(10, el_range=(1, 10)) for _ in range(3)),),
        bench_sizes=(1, 10, 100),
        bench_input=lambda s: random_undirected(s, el_range=(1, 10)),
    )


if __name__ == '__main__':
    test()
