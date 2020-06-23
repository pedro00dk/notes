import heapq

from ..graph import Graph
from ..topsort import topsort_dfs


def sssp_dag(graph: Graph, start: int):
    """
    Single source shortest path for directed acyclic graphs.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to compute single source shortest path
    - `start: int`: vertex to compute distances from

    > `return: (int | float, int)[]`: distances array containing distances to `start` and `parent`
    """
    if graph.vertices_count() == 0:
        return []
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    distances = [(float('inf'), None)] * graph.vertices_count()
    distances[start] = (0, None)
    for v in topsort_dfs(graph):
        vertex_distance, parent = distances[v]
        for edge in graph.edges(v):
            target_distance = vertex_distance + edge.length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, v)
    return distances


def sslp_dag(graph: Graph, start: int):
    """
    Single source longest path for directed acyclic graphs.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to compute single source shortest path
    - `start: int`: vertex to compute distances from

    > `return: (int | float, int)[]`: distances array containing distances to `start` and `parent` 
    """
    if graph.vertices_count() == 0:
        return []
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    distances = [(float('inf'), None)] * graph.vertices_count()
    distances[start] = (0, None)
    for v in topsort_dfs(graph):
        vertex_distance, parent = distances[v]
        for edge in graph.edges(v):
            target_distance = vertex_distance - edge.length  # negate edge length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, v)
    inf = float('inf')
    for i in range(len(distances)):
        distance, parent = distances[i]
        distances[i] = (-distance if distance < inf else inf, parent)
    return distances


def sssp_dijkstra(graph: Graph, start: int, /, end: int = None):
    """
    Dijkstra single source shortest path algorithm.
    Dijkstra does not support graphs with negative edge lengths (except directed acyclic graphs).

    > complexity:
    - time: `O((v + e)*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to compute single source shortest path
    - `start: int`: vertex to compute distances from
    - `end: int? = None`: vertex to stop computation

    > `return: (int | float, int)[]`: distances array containing distances to `start` and `parent` 
    """
    if graph.vertices_count() == 0:
        return []
    if start < 0 or start >= graph.vertices_count() or end is not None and (end < 0 or end > graph.vertices_count()):
        raise IndexError(f'start ({start}) or end ({end}) vertices out of range [0, {graph.vertices_count()})')
    distances = [(float('inf'), None)] * graph.vertices_count()
    distances[start] = (0, None)
    heap = []
    heapq.heappush(heap, (0, start))
    while len(heap) > 0:
        distance, v = heapq.heappop(heap)
        if v == end:
            break
        for edge in graph.edges(v):
            target_distance = distance + edge.length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, v)
                heapq.heappush(heap, (target_distance, edge._target))
    return distances


def sssp_dijkstra_opt(graph: Graph, start: int, /, end: int = None):
    """
    Check base dijkstra algorithm for documentation.

    > optimizations:
    - use `visited´ array to avoid checking already visited edges
    - skip stale heap pairs by checking against current distance before iterating through edges
    """
    if graph.vertices_count() == 0:
        return []
    if start < 0 or start >= graph.vertices_count() or end is not None and (end < 0 or end > graph.vertices_count()):
        raise IndexError(f'start ({start}) or end ({end}) vertices out of range [0, {graph.vertices_count()})')
    visited = [False] * graph.vertices_count()
    distances = [(float('inf'), None)] * graph.vertices_count()
    distances[start] = (0, None)
    heap = []
    heapq.heappush(heap, (0, start))
    while len(heap) > 0:
        distance, v = heapq.heappop(heap)
        if v == end:
            break
        visited[v] = True
        if distance > distances[v][0]:
            continue
        for edge in graph.edges(v):
            if visited[edge._target]:
                continue
            target_distance = distance + edge.length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, v)
                heapq.heappush(heap, (target_distance, edge._target))
    return distances


def sssp_bellman_ford(graph: Graph, start: int, /, check_negative_cycles=True):
    """
    Bellman Ford single source longest path algorithm.

    > complexity:
    - time: `O(v*e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to compute single source shortest path
    - `start: int`: vertex to compute distances from
    - `check_negative_cycles: bool? = True`: check negative cycles and set their distances to negative infinity, not
        necessary if all edges have positive length

    > `return: (int | float, int)[]`: distances array containing distances to `start` and `parent` 
    """
    if graph.vertices_count() == 0:
        return []
    distances = [(float('inf'), None)] * graph.vertices_count()
    distances[start] = (0, None)
    for i in range(graph.vertices_count() - 1):
        for edge in graph.edges():
            target_distance = distances[edge._source][0] + edge.length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, edge._source)
    if check_negative_cycles:
        for i in range(graph.vertices_count() - 1):
            for edge in graph.edges():
                target_distance = distances[edge._source][0] + edge.length
                if target_distance < distances[edge._target][0]:
                    distances[edge._target] = (float('-inf'), edge._source)
    return distances


def apsp_floyd_warshall(graph: Graph, /, check_negative_cycles=True):
    """
    Floyd Warshall all-pairs shortest path algorithm.

    > complexity:
    - time: `O(v**3)`
    - space: `O(v**2)`

    > parameters:
    - `graph: Graph`: graph to compute single source shortest path
    - `check_negative_cycles: bool? = True`: check negative cycles and set their distances to negative infinity, not
        necessary if all edges have positive length

    > `return: ((int | float)[][], int[][])`: distances and parents matrices,
        distances[i][j] contains the shortest distances from the vertex i to a vertex,
        parents contains the parents for each pair path (see `floyd_warshall_rebuild_path`)
    """
    if graph.vertices_count() == 0:
        return ([], [])
    inf = float('inf')
    matrix = graph.adjacency_matrix()
    distances = matrix
    parents = [[None] * graph.vertices_count() for i in range(graph.vertices_count())]
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


def floyd_warshall_rebuild_path(distances: list, parents: list, start: int, end: int):
    """
    Rebuild the path between `start` and `end` from the `distances` and `parents` provided by the `apsp_floyd_warshall`
    algorithm.

    > complexity:
    - time: `O(v)`
    - space: `O(v)`

    > parameters:
    - `distances: (int | float)[][]`: floyd warshall distances matrix
    - `parents: (int | float)[][]`: floyd warshall parents matrix
    - `start: int`: vertex to compute distances from
    - `end: int`: vertex to stop computation

    > `return: (int | float, int[])`: distance from `start` to `end` and the path between them,
    if path is empty, then there is no path between `start` and `end`,
    or if path is `None`, there is a negative cycle between `start` and `end`
    """
    if start < 0 or start >= len(distances) or end is not None and end < 0 or end > len(distances):
        raise IndexError(f'start ({start}) or end ({end}) vertices out of range [0, {len(distances)})')
    path = []
    if distances[start][end] == float('inf'):
        return path
    current = start
    while True:
        if current == -1:
            return None
        path.append(current)
        if current == end:
            break
        current = parents[current][end]
    path.reverse()
    return distances[start][end], path


def test():
    from ...test import benchmark
    from ..factory import random_undirected, random_directed, random_dag
    # skip zero size inputs because in all benchmarks because of floyd warshall array accesses
    print('random directed acyclic graphs')
    benchmark(
        [
            ('                sssp dag', lambda graph: sssp_dag(graph, 0)),
            ('                sslp dag', lambda graph: sslp_dag(graph, 0)),
            ('           sssp dijkstra', lambda graph: sssp_dijkstra(graph, 0)),
            ('       sssp dijkstra opt', lambda graph: sssp_dijkstra_opt(graph, 0)),
            ('       sssp bellman ford', lambda graph: sssp_bellman_ford(graph, 0)),
            ('apsp floyd warshall apsp', lambda graph: apsp_floyd_warshall(graph)[0][0])
        ],
        test_input_iter=(random_dag(el_range=(-10, 15)) for i in range(3)),
        bench_size_iter=(1, 10, 100),
        bench_input=lambda s, r: random_dag((max(s // 4, 1), max(s // 3, 1)), (3, 4), el_range=(-10, 15))
    )
    print('random undirected graphs')
    benchmark(
        [
            ('           sssp dijkstra', lambda graph: sssp_dijkstra(graph, 0)),
            ('       sssp dijkstra opt', lambda graph: sssp_dijkstra_opt(graph, 0)),
            ('       sssp bellman ford', lambda graph: sssp_bellman_ford(graph, 0)),
            ('apsp floyd warshall apsp', lambda graph: apsp_floyd_warshall(graph)[0][0])
        ],
        test_input_iter=(random_undirected(10, el_range=(1, 10)) for i in range(3)),
        bench_size_iter=(1, 10, 100),
        bench_input=lambda s, r: random_undirected(s, el_range=(1, 10))
    )
    print('random directed graphs')
    benchmark(
        [
            ('           sssp dijkstra', lambda graph: sssp_dijkstra(graph, 0)),
            ('       sssp dijkstra opt', lambda graph: sssp_dijkstra_opt(graph, 0)),
            ('       sssp bellman ford', lambda graph: sssp_bellman_ford(graph, 0)),
            ('apsp floyd warshall apsp', lambda graph: apsp_floyd_warshall(graph)[0][0])
        ],
        test_input_iter=(random_directed(10, el_range=(1, 10)) for i in range(3)),
        bench_size_iter=(1, 10, 100),
        bench_input=lambda s, r: random_undirected(s, el_range=(1, 10))
    )


if __name__ == '__main__':
    test()
