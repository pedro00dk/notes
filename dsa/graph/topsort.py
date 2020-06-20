from .graph import Graph


def topsort_khan(graph: Graph):
    """
    Khan's topological sort algorithm.
    This implementation has some tweaks due to graph data structure limitations
    - Khan's algorithm require graph mutation (a copy of the graph is created to apply the algorithm)
    - graph does not support edge removal, a hack is used this (set `edge._target = None`)
    - graph does not provide info on root vertices and vertices amount of incoming edges (edges are counted beforehand)

    > complexity:
    - time: `O(v + e)`
    - space: `O(v + e)` extra `e` due to graph copy

    > parameters:
    - `graph: Graph`: graph to compute topological order

    > `return: Vertex[]`: topological order
    """
    graph = graph.copy()  # copy needed because graph is be mutated
    incoming_edges = [0] * graph.vertices_count()
    total_edges = 0
    for edge in graph.edges():
        incoming_edges[edge._target] += 1
        total_edges += 1
    root_vertices = [v for v, count in enumerate(incoming_edges) if count == 0]
    order = []
    while len(root_vertices) > 0:
        v = root_vertices.pop()
        order.append(v)
        for edge in graph.edges(v):
            if edge.data == True:  # removed edge
                continue
            target = edge._target
            edge.data = True  # remove edge
            incoming_edges[target] -= 1  # decrease edge count
            total_edges -= 1
            if incoming_edges[target] == 0:
                root_vertices.append(target)
    if total_edges > 0:
        raise Exception('topological sort only works with directed acyclic graphs')
    return order


def topsort_dfs(graph: Graph):
    """
    Topological sort algorithm based on depth first search.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to compute topological order

    > `return: Vertex[]`: topological order
    """
    visited = [0] * graph.vertices_count()  # 0: unvisited, 1: temporary, 2: visited
    order = []

    def dfs(v: int):
        if visited[v] == 1:  # temporary
            raise Exception('topological sort only works with directed acyclic graphs')
        visited[v] = 1
        for edge in graph.edges(v):
            if visited[edge._target] != 2:  # not visited
                dfs(edge._target)
        visited[v] = 2
        order.append(v)

    for v in range(graph.vertices_count()):
        if visited[v] != 2:  # not visited or temporary
            dfs(v)
    order.reverse()
    return order


def test():
    from ..test import benchmark
    from .connectivity import strong_connected_tarjan
    from .factory import random_dag
    benchmark(
        [
            ('  topological sort khan', topsort_khan),
            ('   topological sort dfs', topsort_dfs),
            ('topological sort tarjan', lambda graph: [*reversed([v for v, in strong_connected_tarjan(graph)])])
        ],
        test_input_iter=(random_dag() for i in range(5)),
        bench_size_iter=(0, 1, 10, 100, 1000),
        bench_input=lambda s, r: random_dag((s // 20, s // 10), (5, 10))
    )


if __name__ == '__main__':
    test()
