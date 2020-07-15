import collections

from ..connectivity import connected_traverse
from ..graph import Graph


def undirected_fleury(graph: Graph):
    """
    Fleury eulerian path algorithm for undirected graphs.
    This algorithm mutates the graph to preserve asymptotic complexities (`edge.data` and `edge._target` fields).

    > complexity:
    - time: `O(e**2)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find eulerian path

    > `return: (int(), bool)`: path of vertices and if is a cycle, or `None` if graph does not have a path
    """
    if graph.vertices_count() == 0:
        return None
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    remaining_edges = [graph.edges_count(v) for v in range(graph.vertices_count())]
    odd_vertices = [v for v, edges in enumerate(remaining_edges) if edges % 2 != 0]
    if len(odd_vertices) > 2:
        return None
    start = odd_vertices[0] if len(odd_vertices) > 0 else 0
    path = []
    connected_components = len(connected_traverse(graph))
    v = start
    while True:
        path.append(v)
        for edge in graph.edges(v):
            if edge.data is not None:
                continue
            target = edge._target
            edge._target = edge._source  # graph does not support edge deletion, loops are used to disconnect edges
            edge._opposite._target = edge._opposite._source
            remaining_edges[v] -= 1
            remaining_edges[target] -= 1
            remaining_connected_components = len(connected_traverse(graph))
            if remaining_connected_components > connected_components and remaining_edges[v] > 0:
                edge._target = edge._opposite._source
                edge._opposite._target = edge._source
                remaining_edges[v] += 1
                remaining_edges[target] += 1
                continue
            connected_components = remaining_connected_components
            edge.data = edge._opposite.data = True
            v = target
            break
        else:
            break
    return ((*path,), path[0] == path[-1]) if len(path) == graph.unique_edges_count() + 1 else None


def undirected_hierholzer(graph: Graph, /, recursive=False):
    """
    Hierholzer eulerian path algorithm for undirected graphs.
    This algorithm mutates the graph to preserve asymptotic complexities (`edge.data` field).
    This algorithm is naturally recursive, but the recursion depth can be too deep, which may a stack overflow or
    segmentation fault if the recursion depth is extended.
    Due to this, a iterative version is used by default.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find eulerian path
    - `recursive: bool? = False`: use the default recursive version of the algorithm

    > `return: (int(), bool)`: path of vertices and if is a cycle, or `None` if graph does not have a path
    """
    if graph.vertices_count() == 0:
        return None
    if not graph.is_undirected():
        raise Exception('graph must be undirected')
    remaining_edges = [graph.edges_count(v) for v in range(graph.vertices_count())]
    odd_vertices = [v for v, edges in enumerate(remaining_edges) if edges % 2 != 0]
    if len(odd_vertices) > 2:
        return None
    start = odd_vertices[0] if len(odd_vertices) > 0 else 0
    path = collections.deque()
    if recursive:
        def dfs(v: int):
            while remaining_edges[v] > 0:
                e = remaining_edges[v] = remaining_edges[v] - 1
                edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
                if edge.data == True:
                    continue
                edge.data = edge._opposite.data = True
                dfs(edge._target)
            path.appendleft(v)
        dfs(start)
    else:
        stack = [start]
        while len(stack) > 0:
            v = stack[-1]
            if remaining_edges[v] > 0:
                e = remaining_edges[v] = remaining_edges[v] - 1
                edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
                if edge.data == True:
                    continue
                edge.data = edge._opposite.data = True
                stack.append(edge._target)
                continue
            path.appendleft(v)
            stack.pop()
    return ((*path,), path[0] == path[-1]) if len(path) == graph.unique_edges_count() + 1 else None


def directed_hierholzer(graph: Graph, /, recursive=False):
    """
    Hierholzer eulerian path algorithm for directed graphs.
    This algorithm is naturally recursive, but the recursion depth can be too deep, which may a stack overflow or
    segmentation fault if the recursion depth is extended.
    Due to this, a iterative version is used by default.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find eulerian path
    - `recursive: bool? = False`: use the default recursive version of the algorithm

    > `return: (int(), bool)`: path of vertices and if is a cycle, or `None` if graph does not have a path
    """
    if graph.vertices_count() == 0:
        return None
    if not graph.is_directed():
        raise Exception('graph must be directed')
    incoming_edges = [0] * graph.vertices_count()
    outcoming_edges = [0] * graph.vertices_count()
    for edge in graph.edges():
        incoming_edges[edge._target] += 1
        outcoming_edges[edge._source] += 1
    start_vertices = []
    end_vertices = []
    for v in range(graph.vertices_count()):
        delta = outcoming_edges[v] - incoming_edges[v]
        if delta == 0:
            continue
        if abs(delta) > 1:
            return None
        (start_vertices if delta == 1 else end_vertices).append(v)
    if len(start_vertices) not in (0, 1) or len(start_vertices) != len(end_vertices):
        return None
    start = start_vertices[0] if len(start_vertices) > 0 else 0
    path = collections.deque()
    if recursive:
        def dfs(v: int):
            while outcoming_edges[v] > 0:
                e = outcoming_edges[v] = outcoming_edges[v] - 1
                edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
                dfs(edge._target)
            path.appendleft(v)
        dfs(start)
    else:
        stack = [start]
        while len(stack) > 0:
            v = stack[-1]
            if outcoming_edges[v] > 0:
                e = outcoming_edges[v] = outcoming_edges[v] - 1
                edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
                stack.append(edge._target)
                continue
            path.appendleft(v)
            stack.pop()
    return ((*path,), path[0] == path[-1]) if len(path) == graph.edges_count() + 1 else None


def test():
    import sys
    from ...test import benchmark
    from ..factory import random_directed_paired, random_undirected_paired
    sys.setrecursionlimit(10000)
    print('undirected graphs')
    benchmark(
        [
            ('              undirected fleury', lambda graph: undirected_fleury(graph.copy())),
            ('undirected hierholzer recursive', lambda graph: undirected_hierholzer(graph.copy(), True)),
            ('undirected hierholzer iterative', lambda graph: undirected_hierholzer(graph.copy(), False))
        ],
        test_input_iter=(random_undirected_paired(i) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100),
        bench_input=(lambda s, r: random_undirected_paired(s))
    )
    print('directed graphs')
    benchmark(
        [
            ('directed hierholzer recursive', lambda graph: directed_hierholzer(graph, True)),
            ('directed hierholzer iterative', lambda graph: directed_hierholzer(graph, False))
        ],
        test_input_iter=(random_directed_paired(i) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100),
        bench_input=(lambda s, r: random_directed_paired(s))
    )


if __name__ == '__main__':
    test()
