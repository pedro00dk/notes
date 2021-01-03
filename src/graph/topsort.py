from typing import Any

from .graph import Graph


def topsort_khan(graph: Graph[Any, Any]) -> list[int]:
    """
    Khan topological sort algorithm.
    This algorithm mutates the graph to preserve asymptotic complexities (`edge.data` field).

    > complexity
    - time: `O(v + e)`
    - space: `O(v + e)` extra `e` due to graph copy
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to compute topological order
    - `return`: topological order
    """
    if not graph.is_directed():
        raise Exception('graph must be directed')
    incoming_edges = [0] * graph.vertices_count()
    total_edges = 0
    for edge in graph.edges():
        incoming_edges[edge.target] += 1
        total_edges += 1
    root_vertices = [v for v, count in enumerate(incoming_edges) if count == 0]
    order = []
    while len(root_vertices) > 0:
        v = root_vertices.pop()
        order.append(v)
        for edge in graph.edges(v):
            if edge.data == True:  # graph does not support edge deletion, edge.data == True indicates edge deletion
                continue
            edge.data = True
            incoming_edges[edge.target] -= 1
            total_edges -= 1
            if incoming_edges[edge.target] == 0:
                root_vertices.append(edge.target)
    if total_edges > 0:
        raise Exception('graph must be acyclic')
    return order


def topsort_dfs(graph: Graph[Any, Any]) -> list[int]:
    """
    Topological sort algorithm based on depth first search.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to compute topological order
    - `return`: topological order
    """
    if not graph.is_directed():
        raise Exception('graph must be directed')
    visited = [0] * graph.vertices_count()  # 0: unvisited, 1: visited, 2: all children visited
    order: list[int] = []

    def dfs(v: int):
        if visited[v] == 1:  # visited
            raise Exception('graph must be acyclic')
        visited[v] = 1
        for edge in graph.edges(v):
            if visited[edge.target] != 2:  # not all children visited
                dfs(edge.target)
        visited[v] = 2
        order.append(v)

    for v in range(graph.vertices_count()):
        if visited[v] != 2:  # not all children visited
            dfs(v)
    order.reverse()
    return order


def test():
    from ..test import benchmark
    from .connectivity import (strong_connected_kosaraju,
                               strong_connected_tarjan)
    from .factory import random_dag
    benchmark(
        (
            ('    topological sort khan', lambda graph: topsort_khan(graph)),
            ('     topological sort dfs', topsort_dfs),
            ('  topological sort tarjan', lambda graph: [*reversed([v for v, in strong_connected_tarjan(graph)])]),
            ('topological sort kosaraju', lambda graph: [v for v, in strong_connected_kosaraju(graph)]),
        ),
        test_inputs=(*(random_dag() for _ in range(5)),),
        bench_sizes=(0, 1, 10, 100),
        bench_input=lambda s: random_dag((s // 10, s // 5), (5, 10)),
        preprocess_input=Graph[Any, Any].copy,
    )


if __name__ == '__main__':
    test()
