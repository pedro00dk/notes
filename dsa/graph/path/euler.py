import collections

from ..connectivity import connected_traverse
from ..graph import Graph


def undirected_fleury(graph: Graph):
    """
    Fleury eulerian path algorithm for directed graphs.

    > complexity:
    - time: `O(e**2)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find eulerian path

    > `return: (int[], bool)`: path of vertices ids or `None` if a path is not found, and if the path is a cycle
    """
    if graph.vertices_count() == 0:
        return (), None
    if not graph.is_undirected():
        raise Exception('undirected eulerian path algorithm only works with undirected graphs')
    edges = [0] * graph.vertices_count()
    for edge in graph.edges():
        if edge.data == 1:  # 1 means count visited
            continue
        edges[edge._target] += 1
        edges[edge._source] += 1
        edge.data = edge._opposite.data = 1
    odd_vertices = []
    for v in range(graph.vertices_count()):
        if edges[v] % 2 != 0:
            odd_vertices.append(v)
    if len(odd_vertices) > 2:
        return None, False
    start_vertex = odd_vertices[0] if len(odd_vertices) > 0 else 0
    path = []
    starting_connected_groups = sum(int(len(component) > 1) for component in connected_traverse(graph))

    def dfs(v: int):
        path.append(v)
        while edges[v] > 0:
            e = edges[v] = edges[v] - 1
            edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
            edge_target = edge._target
            # graph does not support vertex or edge deletion, simulate delete by creating an edge loop
            # since connectivity algorithms are also used edge loops are created to disconnect vertices
            if edge.data == 2:
                continue
            edge._target = v
            edge._opposite._target = edge_target
            connected_groups = sum(int(len(component) > 1) for component in connected_traverse(graph))
            if connected_groups > starting_connected_groups:
                edge._target = edge_target
                edge._opposite._target = v
                continue
            edge.data = edge._opposite.data = 2
            dfs(edge_target)

    if graph.vertices_count() > 0:
        dfs(start_vertex)
    return ((*path,), len(odd_vertices) == 0) if len(path) == graph.unique_edges_count() + 1 else (None, False)


def undirected_hierholzer(graph: Graph):
    """
    Hierholzer eulerian path algorithm for undirected graphs.
    To maintain asymptotic complexities, the undirected implementation mutates graph edges `data` property to mark back
    edges as visited, preventing a graph copy.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find eulerian path

    > `return: (int[], bool)`: path of vertices ids or `None` if a path is not found, and if the path is a cycle
    """
    if graph.vertices_count() == 0:
        return (), None
    if not graph.is_undirected():
        raise Exception('undirected eulerian path algorithm only works with undirected graphs')
    edges = [0] * graph.vertices_count()
    for edge in graph.edges():
        if edge.data == 1:  # 1 means count visited
            continue
        edges[edge._target] += 1
        edges[edge._source] += 1
        edge.data = edge._opposite.data = 1
    odd_vertices = []
    for v in range(graph.vertices_count()):
        if edges[v] % 2 != 0:
            odd_vertices.append(v)
    if len(odd_vertices) > 2:
        return None, False
    start_vertex = odd_vertices[0] if len(odd_vertices) > 0 else 0
    path = collections.deque()

    # # recursive implementation gets too deep, causing a stack overflow
    # def dfs(v: int):
    #     while edges[v] > 0:
    #         e = edges[v] = edges[v] - 1
    #         edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
    #         if edge.data == 2:  # 2 means dfs visited
    #             continue
    #         edge.data = edge._opposite.data = 2
    #         dfs(edge._target)
    #     path.appendleft(v)

    # if graph.vertices_count() > 0:
    #     dfs(start_vertex)

    # iterative implementation using a stack
    stack = [start_vertex]
    while len(stack) > 0:
        v = stack[-1]
        if edges[v] > 0:
            e = edges[v] = edges[v] - 1
            edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
            if edge.data == 2:  # 2 means dfs visited
                continue
            edge.data = edge._opposite.data = 2
            stack.append(edge._target)
            continue
        path.appendleft(v)
        stack.pop()

    return ((*path,), len(odd_vertices) == 0) if len(path) == graph.unique_edges_count() + 1 else (None, False)


def directed_hierholzer(graph: Graph):
    """
    Hierholzer eulerian path algorithm for directed graphs.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to find eulerian path

    > `return: (int[], bool)`: path of vertices ids or `None` if a path is not found, and if the path is a cycle
    """
    if graph.vertices_count() == 0:
        return (), None
    if not graph.is_directed():
        raise Exception('directed eulerian path algorithm only works with directed graphs')
    incoming_edges = [0] * graph.vertices_count()
    outcoming_edges = [0] * graph.vertices_count()
    for edge in graph.edges():
        incoming_edges[edge._target] += 1
        outcoming_edges[edge._source] += 1
    start_vertices = []
    end_vertices = []
    for v in range(graph.vertices_count()):
        edge_delta = outcoming_edges[v] - incoming_edges[v]
        if abs(edge_delta) > 1:
            return None, False
        elif edge_delta == 1:
            start_vertices.append(v)
        elif edge_delta == -1:
            end_vertices.append(v)
    if not (len(start_vertices) == 0 and len(end_vertices) == 0 or len(start_vertices) == 1 and len(end_vertices) == 1):
        return None, False
    start_vertex = start_vertices[0] if len(start_vertices) > 0 else 0
    path = collections.deque()

    # # recursive implementation gets too deep, causing a stack overflow
    # def dfs(v: int):
    #     while outcoming_edges[v] > 0:
    #         e = outcoming_edges[v] = outcoming_edges[v] - 1
    #         edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
    #         dfs(edge._target)
    #     path.appendleft(v)

    # if graph.vertices_count() > 0:
    #     dfs(start_vertex)

    # iterative implementation using a stack
    stack = [start_vertex]
    while len(stack) > 0:
        v = stack[-1]
        if outcoming_edges[v] > 0:
            e = outcoming_edges[v] = outcoming_edges[v] - 1
            edge = graph._edges[v][e]  # direct access to graph edges to avoid creating copies of arrays
            stack.append(edge._target)
            continue
        path.appendleft(v)
        stack.pop()

    return ((*path,), len(start_vertices) == 0) if len(path) == graph.edges_count() + 1 else (None, False)


def test():
    import sys
    from ...test import benchmark
    from ..factory import random_directed_paired, random_undirected_paired
    # stack size too short for fleury recursion steps + connected recursion steps
    sys.setrecursionlimit(5000)
    print('undirected graphs')
    benchmark(
        [
            ('    undirected fleury', lambda graph: undirected_fleury(graph.copy())),
            ('undirected hierholzer', lambda graph: undirected_hierholzer(graph.copy()))
        ],
        test_input_iter=(random_undirected_paired(i) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100),
        bench_input=(lambda s, r: random_undirected_paired(s))
    )
    print('directed graphs')
    benchmark(
        [('directed hierholzer', lambda graph: directed_hierholzer(graph.copy()))],
        test_input_iter=(random_directed_paired(i) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100, 1000),
        bench_input=(lambda s, r: random_directed_paired(s))
    )


if __name__ == '__main__':
    test()
