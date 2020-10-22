import collections
import math

from .graph import Edge, Graph


def edge_capacity(edge: Edge):
    """
    Return the edge remaining capacity.
    The edge maximum capacity is stored in the edge `length` property.
    The edge used capacity is stored in the edge `data` property.

    > parameters:
    - `edge: Edge`: graph edge
    """
    return edge.length - edge.data


def augment_edge(edge: Edge, flow):
    """
    Increase the used capacity in the received edge, decreasing it on the opposite edge.
    The edge maximum capacity is stored in the edge `length` property.
    The edge used capacity is stored in the edge `data` property.
    `edge` can be both a normal edge or a residual edge.

    > parameters:
    - `edge: Edge`: graph edge
    - `flow: int | float`: graph edge
    """
    edge.data += flow
    edge._opposite.data -= flow


def pathfinder_dfs(flow_graph: Graph, source: int, sink: int):
    """
    Depth first search augmenting path finder and flow pusher for Ford Fulkerson maxflow/mincut algorithm.

    > parameters:
    - `flow_graph: Graph`: graph created by the maxflow main function (used for preseting closure variables)
    - `source: int`: graph source vertex
    - `sink: int`: graph sink source

    > `return`: function for finding augmenting paths and pushing flow
    """
    def find_augmenting_path(flow_graph: Graph, v: int, flow, visited: list, visited_marker: int):
        """
        This function finds augmenting paths using a depth first search and increases the path flow.
        The performance depends on the edges capacities, which means this function is not strongly polynomial.

        > complexity: (of ford fulkerson algorithm using this core)
        - time: `O(f*e)` where `f` is the difference from the minimum to the maximum edge capacity
        - space: `O(v + e)`

        > parameters:
        - `flow_graph: Graph`: graph created by the maxflow main function
        - `v: int`: source vertex (it is named as `v` because it changes to other vertices in recursive calls)
        - `flow: int | float`: the flow to be pushed
        - `visited: int[]`: visited array (uses int to allow fast reset)
        - `visited_marker: int`: current visited marker for visited array

        > `return: (int | float, bool)`: the bottleneck of the found augmenting path and if should keep finding paths
        """
        if v == sink:
            return flow, True
        visited[v] = visited_marker
        for edge in flow_graph.edges(v):
            if edge_capacity(edge) <= 0 or visited[edge._target] == visited_marker:
                continue
            bottleneck, _ = find_augmenting_path(
                flow_graph, edge._target, min(flow, edge_capacity(edge)), visited, visited_marker
            )
            if bottleneck <= 0:
                continue
            augment_edge(edge, bottleneck)
            return bottleneck, True
        return 0, False

    return find_augmenting_path


def pathfinder_edmonds_karp(flow_graph: Graph, source: int, sink: int):
    """
    Edmonds Karp augmenting path finder and flow pusher for Ford Fulkerson maxflow/mincut algorithm.

    > parameters:
    - `flow_graph: Graph`: graph created by the maxflow main function (used for preseting closure variables)
    - `source: int`: graph source vertex
    - `sink: int`: graph sink source

    > `return`: function for finding algmenting paths and pushing flow
    """
    def find_augmenting_path(flow_graph: Graph, v: int, flow, visited: list, visited_marker: int):
        """
        This function finds augmenting paths using a breadth first search and increases the path flow.

        > complexity: (of ford fulkerson algorithm using this core)
        - time: `O(v*e**2)`
        - space: `O(v)`

        > parameters:
        - `flow_graph: Graph`: graph created by the maxflow main function
        - `v: int`: source vertex (it is named as `v` because it changes to other vertices in recursive calls)
        - `flow: int | float`: the flow to be pushed
        - `visited: int[]`: visited array (uses int to allow fast reset)
        - `visited_marker: int`: current visited marker for visited array

        > `return: (int | float, bool)`: the bottleneck of the found augmenting path and if should keep finding paths
        """
        queue = collections.deque()
        parent_edges = [None] * flow_graph.vertices_count()
        visited[v] = visited_marker
        queue.append(v)
        while len(queue) > 0:
            v = queue.popleft()
            for edge in flow_graph.edges(v):
                if edge_capacity(edge) <= 0 or visited[edge._target] == visited_marker:
                    continue
                visited[edge._target] = visited_marker
                parent_edges[edge._target] = edge
                queue.append(edge._target)
        if parent_edges[sink] is None:
            return 0, False
        bottleneck = flow
        edge = parent_edges[sink]
        while edge is not None:
            bottleneck = min(bottleneck, edge_capacity(edge))
            edge = parent_edges[edge._source]
        edge = parent_edges[sink]
        while edge is not None:
            augment_edge(edge, bottleneck)
            edge = parent_edges[edge._source]
        return bottleneck, True

    return find_augmenting_path


def pathfinder_dfs_capacity_scaling(flow_graph: Graph, source: int, sink: int):
    """
    Depth first search with capacity scaling augmenting path finder and flow pusher for Ford Fulkerson maxflow/mincut
    algorithm.

    > parameters:
    - `flow_graph: Graph`: graph created by the maxflow main function (used for preseting closure variables)
    - `source: int`: graph source vertex
    - `sink: int`: graph sink source

    > `return: int | float`: the bottleneck of the found augmenting path
    """
    u = max(edge.length for edge in flow_graph.edges())
    delta = 1 << math.floor(math.log2(u))

    def find_augmenting_path(flow_graph: Graph, v: int, flow, visited: list, visited_marker: int):
        """
        This function finds augmenting paths using a depth first search and increases the path flow.
        Different from the default depth first search algorithm, capacity scaling prioritizes edges with higher
        available capacity.
        Let `u` be the largest edge capacity value and 'delta' the largest power of 2 smaller than `u`.
        The algorithm takes paths where edges capacities are greater or equal 'delta', if no path is found, `delta`
        is divided by 2.
        The performance depends on the edges capacities, which means this core is not strongly polynomial.

        > complexity: (of ford fulkerson algorithm using this core)
        - time: `O(e**2*log(u))` where `f` is the difference from the minimum to the maximum edge capacity
        - space: `O(v + e)`

        > parameters:
        - `flow_graph: Graph`: graph created by the maxflow main function
        - `v: int`: source vertex (it is named as `v` because it changes to other vertices in recursive calls)
        - `sink: int`: sink vertex id
        - `flow: int | float`: the flow to be pushed
        - `visited: int[]`: visited array (uses int to allow fast reset)
        - `visited_marker: int`: current visited marker for visited array

        > `return: (int | float, bool)`: the bottleneck of the found augmenting path and if should keep finding paths
        """
        nonlocal delta
        divide = True
        if v == sink:
            return flow, True
        visited[v] = visited_marker
        for edge in flow_graph.edges(v):
            if edge_capacity(edge) <= delta or visited[edge._target] == visited_marker:
                continue
            bottleneck, _ = find_augmenting_path(
                flow_graph, edge._target, min(flow, edge_capacity(edge)), visited, visited_marker
            )
            if bottleneck <= 0:
                continue
            augment_edge(edge, bottleneck)
            return bottleneck, True
        if v == source:
            delta /= 2
        return 0, delta > 0

    return find_augmenting_path


def pathfinder_dinic(flow_graph: Graph, source: int, sink: int):
    """
    Dinic augmenting path finder and flow pusher for Ford Fulkerson maxflow/mincut algorithm.
    Note: Dinic's algorithm was developed as a standalone method for finding maxflow, but here, it is implemented as a
    module to the Ford Fulkerson algorithm.

    > parameters:
    - `flow_graph: Graph`: graph created by the maxflow main function (used for preseting closure variables)
    - `source: int`: graph source vertex
    - `sink: int`: graph sink source

    > `return: int | float`: the bottleneck of the found augmenting path
    """
    levels = [-1] * flow_graph.vertices_count()
    next_edge = [0] * flow_graph.vertices_count()

    def build_level_graph():
        """
        Build the level graph used by the Dinic pathfinding algorithm.
        """
        levels[:] = (-1 for i in range(flow_graph.vertices_count()))
        next_edge[:] = (0 for i in range(flow_graph.vertices_count()))
        queue = collections.deque()
        queue.append(source)
        levels[source] = 0
        while len(queue) > 0:
            v = queue.popleft()
            for edge in flow_graph.edges(v):
                if edge_capacity(edge) <= 0 or levels[edge._target] != -1:
                    continue
                queue.append(edge._target)
                levels[edge._target] = levels[v] + 1

    def find_augmenting_path(flow_graph: Graph, v: int, flow, visited: list, visited_marker: int):
        """
        This function finds augmenting paths using a breadth first search to build a level graph and then depth first
        searches to find short paths.

        > complexity: (of ford fulkerson algorithm using this core)
        - time: `O(v**2*e)` where `f` is the difference from the minimum to the maximum edge capacity
        - space: `O(v + e)`

        > parameters:
        - `flow_graph: Graph`: graph created by the maxflow main function
        - `v: int`: source vertex (it is named as `v` because it changes to other vertices in recursive calls)
        - `sink: int`: sink vertex id
        - `flow: int | float`: the flow to be pushed
        - `visited: int[]`: visited array (uses int to allow fast reset)
        - `visited_marker: int`: current visited marker for visited array

        > `return: (int | float, bool)`: the bottleneck of the found augmenting path and if should keep finding paths
        """
        if v == sink:
            return flow, True
        while next_edge[v] < flow_graph.edges_count(v):
            edge = flow_graph._edges[v][next_edge[v]]  # direct access to graph edges to avoid creating copies of arrays
            next_edge[v] += 1
            if edge_capacity(edge) <= 0 or levels[edge._target] <= levels[v]:
                continue
            bottleneck, _ = find_augmenting_path(
                flow_graph, edge._target, min(flow, edge_capacity(edge)), visited, visited_marker
            )
            if bottleneck <= 0:
                continue
            augment_edge(edge, bottleneck)
            return bottleneck, True
        if v == source:
            build_level_graph()
        return 0, levels[sink] != -1

    build_level_graph()
    return find_augmenting_path


def maxflow_ford_fulkerson(graph: Graph, /, source=0, sink: int = None, pathfinder=pathfinder_dfs):
    """
    Ford Fulkerson maxflow/mincut algorithm.
    This algorithm mutates the graph to implement optimizations (`edge.data` field).
    A flow graph is created as an undirected graph based on `graph`, containing the original directed edges plus
    residual edges.
    This algorithm accepts different pathfiding functions, which are strategies for finding augmenting paths and pushing
    flow through edges.
    THe minium cut is collected from the residual graph after pushing flow.

    > complexity: (check path finding functions)

    > parameters:
    - `graph: Graph`: graph to compute maxflow and mincut
    - `source: int? = 0`: graph source vertex
    - `sink: int? = graph.vertex_count() - 1`: graph sink source
    - `pathfinder: ((Graph, int, int) => (Graph, int, int, int | float, int[], int) => (int | float, bool))? =
        pathfinder_dfs`: function that returns for another function for finding augmenting paths (see documentation)

    > `return: (int | float, (int, int, int | float)[])`: maxflow and edges in the mincut (source, target, capacity)
    """
    if not graph.is_directed():
        raise Exception('graph must be directed')
    sink = sink if sink is not None else graph.vertices_count() - 1
    flow_graph = Graph()
    for vertex in graph.vertices():
        flow_graph.make_vertex(vertex.weight, vertex.data)
    for edge in graph.edges():
        base_edge, residual_edge = flow_graph.make_edge(edge._source, edge._target, edge.length, 0)
        residual_edge.length = 0
    visited = [0] * graph.vertices_count()
    visited_marker = 1  # visited marker used to avoid reseting visited list after each augmenting path
    maxflow = 0
    find_augmenting_path = pathfinder(flow_graph, source, sink)
    while True:
        bottleneck, keep = find_augmenting_path(flow_graph, source, float('inf'), visited, visited_marker)
        maxflow += bottleneck
        visited_marker += 1
        if not keep:
            break
    mincut = []
    queue = collections.deque()
    queue.append(source)
    visited[source] = visited_marker
    while len(queue) > 0:
        v = queue.popleft()
        for edge in flow_graph.edges(v):
            if visited[edge._target] == visited_marker or edge_capacity(edge) <= 0:
                continue
            queue.append(edge._target)
            visited[edge._target] = visited_marker
    for v, marker in enumerate(visited):
        if marker != visited_marker:
            continue
        for edge in graph.edges(v):
            if visited[edge._target] != visited_marker:
                mincut.append((edge._source, edge._target, edge.length))
    return maxflow, mincut


def test():
    from ..test import benchmark
    from .factory import random_flow
    benchmark(
        [
            (
                '                 maxflow ford fulkerson dfs',
                lambda graph: maxflow_ford_fulkerson(graph, pathfinder=pathfinder_dfs)
            ),
            (
                '        maxflow ford fulkerson edmonds karp',
                lambda graph: maxflow_ford_fulkerson(graph, pathfinder=pathfinder_edmonds_karp)
            ),
            (
                'maxflow ford fulkerson dfs capacity scaling',
                lambda graph: maxflow_ford_fulkerson(graph, pathfinder=pathfinder_dfs_capacity_scaling)
            ),
            (
                '               maxflow ford fulkerson dinic',
                lambda graph: maxflow_ford_fulkerson(graph, pathfinder=pathfinder_dinic)
            )
        ],
        test_inputs=(
            random_flow((i, i), (i // 2, i // 2), ancestor_probability=0, el_range=(10, 50))[0] for i in (2, 3, 4, 5)
        ),
        bench_sizes=(0, 1, 10, 100),
        bench_input=lambda s: random_flow((s // 10, s // 5), (5, 10), el_range=(10, 50))[0],
        preprocess_input=Graph.copy
    )


if __name__ == '__main__':
    test()
