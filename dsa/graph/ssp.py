import heapq

from .graph import Graph
from .topsort import topsort_dfs


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
    for vertex in topsort_dfs(graph):
        vertex_distance, parent = distances[vertex._id]
        for edge in graph.edges(vertex._id):
            target_distance = vertex_distance + edge.length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, vertex._id)
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
    for vertex in topsort_dfs(graph):
        vertex_distance, parent = distances[vertex._id]
        for edge in graph.edges(vertex._id):
            target_distance = vertex_distance - edge.length  # negate edge length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, vertex._id)
    inf = float('inf')
    for i in range(len(distances)):
        distance, parent = distances[i]
        distances[i] = (-distance if distance < inf else inf, parent)
    return distances


def dijkstra(graph: Graph, start: int, /, end: int = None, ignore_negative_edges=False, ignore_negative_exceptions=False):
    """
    Dijkstra single source shortest path algorithm.
    Dijkstra does not support graphs with negative edge lengths (except if the graph is directed acyclic).

    > complexity:
    - time: `O((v + e)*log(v))`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to compute single source shortest path
    - `start: int`: vertex to compute distances from
    - `end: int? = None`: vertex to stop computation
    - `ignore_negative_edges: bool? = False`: skip edge with negative weight
    - `ignore_negative_exceptions: bool? = False`: prevent raising exception if negative edge is found, the algorithm
        may get stuck in an infinity loop if there is a cycle with negative length, this option can be enabled for
        direct acyclic graphs

    > `return: (int | float, int)[]`: distances array containing distances to `start` and `parent` 
    """
    if graph.vertices_count() == 0:
        return []
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    distances = [(float('inf'), None)] * len(graph)
    distances[start] = (0, None)
    heap = []
    heapq.heappush(heap, (0, start))
    while len(heap) > 0:
        vertex_distance, vertex_id = heapq.heappop(heap)
        if vertex_id == end:
            break
        for edge in graph.edges(vertex_id):
            if edge.length < 0:
                if ignore_negative_edges:
                    continue
                if not ignore_negative_exceptions:
                    raise Exception('unsupported negative edge length')
            target_distance = vertex_distance + edge.length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, vertex_id)
                heapq.heappush(heap, (target_distance, edge._target))
    return distances


def dijkstra_opt(graph: Graph, start: int, /, end: int = None, ignore_negative_edges=False, ignore_negative_exceptions=False):
    """
    Check base dijkstra algorithm for documentation.

    > optimizations:
    - use `visited´ array to avoid checking already visited edges
    - skip stale heap pairs by checking against current distance before iterating through edges
    """
    if graph.vertices_count() == 0:
        return []
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    visited = [False] * graph.vertices_count()
    distances = [(float('inf'), None)] * graph.vertices_count()
    distances[start] = (0, None)
    heap = []
    heapq.heappush(heap, (0, start))
    while len(heap) > 0:
        vertex_distance, vertex_id = heapq.heappop(heap)
        if vertex_id == end:
            break
        visited[vertex_id] = True
        if vertex_distance > distances[vertex_id][0]:
            continue
        for edge in graph.edges(vertex_id):
            if visited[edge._target]:
                continue
            if edge.length < 0:
                if ignore_negative_edges:
                    continue
                if not ignore_negative_exceptions:
                    raise Exception('unsupported negative edge length')
            target_distance = vertex_distance + edge.length
            if target_distance < distances[edge._target][0]:
                distances[edge._target] = (target_distance, vertex_id)
                heapq.heappush(heap, (target_distance, edge._target))
    return distances


def bellman_ford(graph: Graph, start: int, /, check_negative_cycles=True):
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


def test():
    from ..test import benchmark
    from .factory import random_undirected, random_directed, random_dag
    print('random directed acyclic graphs')
    benchmark(
        [
            ('single source shortest path', lambda graph: sssp_dag(graph, 0)),
            ('single source longuest path', lambda graph: sslp_dag(graph, 0)),
            ('              dijkstra sssp', lambda graph: dijkstra(graph, 0, ignore_negative_exceptions=True)),
            ('          dijkstra opt sssp', lambda graph: dijkstra_opt(graph, 0, ignore_negative_exceptions=True)),
            ('          bellman ford sssp', lambda graph: bellman_ford(graph, 0))
        ],
        test_input_iter=(random_dag(el_range=(-10, 15)) for i in range(3)),
        bench_size_iter=(0, 1, 10, 100),
        bench_input=lambda s, r: random_dag((s // 4, s // 3), (3, 4), el_range=(-10, 15))
    )
    print('random undirected graphs')
    benchmark(
        [
            ('              dijkstra sssp', lambda graph: dijkstra(graph, 0)),
            ('          dijkstra opt sssp', lambda graph: dijkstra_opt(graph, 0)),
            ('          bellman ford sssp', lambda graph: bellman_ford(graph, 0))
        ],
        test_input_iter=(random_undirected(10, el_range=(1, 10)) for i in range(3)),
        bench_size_iter=(0, 1, 10, 100),
        bench_input=lambda s, r: random_undirected(s, el_range=(1, 10))
    )
    print('random directed graphs')
    benchmark(
        [
            ('              dijkstra sssp', lambda graph: dijkstra(graph, 0)),
            ('          dijkstra opt sssp', lambda graph: dijkstra_opt(graph, 0)),
            ('          bellman ford sssp', lambda graph: bellman_ford(graph, 0))
        ],
        test_input_iter=(random_directed(10, el_range=(1, 10)) for i in range(3)),
        bench_size_iter=(0, 1, 10, 100),
        bench_input=lambda s, r: random_undirected(s, el_range=(1, 10))
    )


if __name__ == '__main__':
    test()
