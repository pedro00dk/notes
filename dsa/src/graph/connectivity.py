import collections
import itertools
from typing import Any, Literal, Optional, cast

from ..dset import DisjointSet
from .graph import Graph


def connected_traverse(graph: Graph[Any, Any], mode: Literal["depth", "breadth"] = "depth") -> list[list[int]]:
    """
    Find connected components in `graph` using traversals to expand components.
    `graph` must be undirected, otherwise, the algorithm can not assure the components are strongly connected.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to search components
    - `mode`: the traversal algorithm to use
    - `return`: list containing connected vertices ids
    """
    if not graph.is_undirected():
        raise Exception("graph must be undirected")
    visited = [False] * graph.vertices_count()
    components: list[list[int]] = []

    def dfs(v: int, component: list[int]):
        component.append(v)
        visited[v] = True
        for edge in graph.edges(v):
            if not visited[edge.target]:
                dfs(edge.target, component)

    def bfs(v: int, component: list[int]):
        queue = collections.deque[int]()
        queue.append(v)
        visited[v] = True
        while len(queue) > 0:
            v = queue.popleft()
            component.append(v)
            for edge in graph.edges(v):
                if not visited[edge.target]:
                    queue.append(edge.target)
                    visited[edge.target] = True

    traversal = dfs if mode == "depth" else bfs
    for v in range(graph.vertices_count()):
        if visited[v]:
            continue
        component: list[int] = []
        traversal(v, component)
        components.append(component)
    return components


def connected_disjoint_set(graph: Graph[Any, Any]) -> list[list[int]]:
    """
    Find connected components in `graph` using a disjoint set.
    `graph` must be undirected, otherwise, the algorithm can not assure the components are strongly connected.

    > complexity
    - time: `O(v + e)`, the extra `v` is due to disjoint set operations to extract component as a `int[][]` object
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to search components
    - `return`: list containing connected vertices ids
    """
    if not graph.is_undirected():
        raise Exception("graph must be undirected")
    disjoint_set = DisjointSet(graph.vertices_count())
    for edge in graph.edges():
        disjoint_set.union(edge.source, edge.target)
    components: list[list[int]] = [[] for _ in range(disjoint_set.sets())]
    index = 0
    indices: dict[int, int] = {}
    for v in range(graph.vertices_count()):
        component = disjoint_set.find(v)
        if component not in indices:
            indices[component] = index
            index += 1
        components[indices[component]].append(v)
    return components


def biconnected_tarjan(graph: Graph[Any, Any]) -> tuple[list[tuple[int, int]], list[int], list[list[tuple[int, int]]]]:
    """
    Tarjan and Hopcroft bridges, articulations and biconnected components algorithm.
    `graph` must be undirected, otherwise, the algorithm can not assure the components are biconnected.

    Note that brides are not directly correlated to articulations and biconnected components.
    Removing a bridge will disconnect a biconnected component of size 2 only.
    Removing an articulation from a biconnected component of size 2 will not, because the remaining vertex is
    "connected" with an empty set of vertices.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to search components
    - `return`: tuple containing bridges, articulations and edges of biconnected components
    """
    if not graph.is_undirected():
        raise Exception("graph must be undirected")
    next_order = 0
    order = cast(list[int], [None] * graph.vertices_count())  # also encode visited (order[v] is not None)
    low = cast(list[int], [None] * graph.vertices_count())
    stack: list[tuple[int, int]] = []
    articulations = set[int]()
    bridges: list[tuple[int, int]] = []
    bicomponents: list[list[tuple[int, int]]] = []

    def dfs(v: int, parent: Optional[int]):
        nonlocal next_order
        order[v] = low[v] = next_order
        next_order += 1
        children = 0
        for edge in graph.edges(v):
            if edge.target == parent:
                continue
            edge_tuple = (edge.source, edge.target)
            if order[edge.target] is not None:  # visited
                if low[v] > order[edge.target]:
                    low[v] = order[edge.target]
                    stack.append(edge_tuple)
                continue
            stack.append(edge_tuple)
            dfs(edge.target, v)  # not visited
            children += 1
            low[v] = min(low[v], low[edge.target])
            if order[v] <= low[edge.target]:
                if order[v] < low[edge.target]:
                    bridges.append(edge_tuple)
                if parent is not None or children >= 2:
                    articulations.add(v)
                bicomponent = [edge_tuple, *itertools.takewhile(lambda e: e != edge_tuple, reversed(stack))]
                bicomponents.append(bicomponent)
                del stack[-len(bicomponents[-1]) :]

    for v in range(graph.vertices_count()):
        if order[v] is None:
            dfs(v, None)
    return (bridges, [*articulations], bicomponents)


def strong_connected_tarjan(graph: Graph[Any, Any]) -> list[list[int]]:
    """
    Tarjan strongly connected components algorithm.
    This algorithm can also be used for topological sorting.
    If the graph being processed is directed and acyclic, each component will contain a single vertex and components
    will be in a reverse topological order. (Kosaraju's outputs in normal order)

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to search components
    - `return`: list containing strongly connected components
    """
    if not graph.is_directed():
        raise Exception("graph must be directed")
    next_order = 0
    order = cast(list[int], [None] * graph.vertices_count())  # also encode visited and stacked (not None, != -1)
    low = cast(list[int], [None] * graph.vertices_count())
    stack: list[int] = []
    components: list[list[int]] = []

    def dfs(v: int):
        nonlocal next_order
        order[v] = low[v] = next_order
        next_order += 1
        stack.append(v)
        for edge in graph.edges(v):
            if order[edge.target] is None:  # not visited
                dfs(edge.target)
            if order[edge.target] != -1:  # stacked (can not be unvisited due to step above)
                low[v] = min(low[v], low[edge.target])
        if low[v] != order[v]:
            return
        components.append([v, *itertools.takewhile(lambda u: u != v, reversed(stack))])
        del stack[-len(components[-1]) :]
        for u in components[-1]:
            order[u] = -1

    for v in range(graph.vertices_count()):
        if order[v] is None:
            dfs(v)
    return components


def strong_connected_kosaraju(graph: Graph[Any, Any]) -> list[list[int]]:
    """
    Kosaraju strongly connected components algorithm.
    This algorithm can also be used for topological sorting.
    If the graph being processed is directed and acyclic, each component will contain a single vertex and components
    will be in topological order. (Tarjan's outputs in reversed order)

    > complexity
    - time: `O(v + e)`
    - space: `O(v + e)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to search components
    - `return`: list containing strongly connected vertices ids
    """
    if not graph.is_directed():
        raise Exception("graph must be directed")
    visited = [False] * graph.vertices_count()
    stack: list[int] = []

    def dfs_stack(v: int):
        visited[v] = True
        for edge in graph.edges(v):
            if not visited[edge.target]:
                dfs_stack(edge.target)
        stack.append(v)

    for v in range(graph.vertices_count()):
        if visited[v]:
            continue
        dfs_stack(v)

    transposed_graph = graph.transposed()
    visited = [False] * graph.vertices_count()

    def dfs_component(v: int, component: list[int]):
        visited[v] = True
        component.append(v)
        for edge in transposed_graph.edges(v):
            if not visited[edge.target]:
                dfs_component(edge.target, component)

    components: list[list[int]] = []
    while len(stack) > 0:
        v = stack.pop()
        if visited[v]:
            continue
        component: list[int] = []
        dfs_component(v, component)
        components.append(component)
    return components


def test():
    from ..test import benchmark
    from .factory import random_directed, random_undirected

    def test_biconnected_tarjan(graph: Graph[Any, Any]):
        bridges, articulations, components = biconnected_tarjan(graph)
        return {
            "components": [(*set(v for e in c for v in e),) for c in components],
            "articulations": articulations,
            "bridges": bridges,
        }

    print("undirected graphs")
    benchmark(
        (
            ("  connected traverse depth", lambda graph: connected_traverse(graph, mode="depth")),
            ("connected traverse breadth", lambda graph: connected_traverse(graph, mode="breadth")),
            ("    connected disjoint set", connected_disjoint_set),
            ("        biconnected tarjan", test_biconnected_tarjan),
        ),
        test_inputs=(*(random_undirected(i, 0.1) for i in (5, 10, 15, 20)),),
        bench_sizes=(0, 1, 10, 100, 1000),
        bench_input=lambda s: random_undirected(s, 0.05),
    )
    print("directed graphs")
    benchmark(
        (
            ("  strong connected tarjan", strong_connected_tarjan),
            ("strong connected kosaraju", strong_connected_kosaraju),
        ),
        test_inputs=(*(random_directed(i, 0.1) for i in (5, 10, 15, 20)),),
        bench_sizes=(0, 1, 10, 100, 1000),
        bench_input=lambda s: random_directed(s, 0.05),
    )


if __name__ == "__main__":
    test()
