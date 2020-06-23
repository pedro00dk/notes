import collections

from ..dset import DisjointSet
from .graph import Graph


def connected_traverse(graph: Graph, /, mode='depth'):
    """
    Find connected components in `graph` using traversals to expand components.
    `graph` must be undirected, otherwise, the algorithm can not assure the components are strongly connected.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search components
    - `mode: ('depth' | 'breadth')? = 'depth'`: the traversal algorithm to use

    > `return: int[][]`: list containing connected vertices ids
    """
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    visited = [False] * graph.vertices_count()
    components = []

    def dfs(v: int, component: list):
        component.append(v)
        visited[v] = True
        for edge in graph.edges(v):
            if not visited[edge._target]:
                dfs(edge._target, component)

    def bfs(v: int, component: list):
        queue = collections.deque()
        queue.append(v)
        while len(queue) > 0:
            v = queue.popleft()
            component.append(v)
            visited[v] = True
            for edge in graph.edges(v):
                if not visited[edge._target]:
                    dfs(edge._target, component)

    traversal = dfs if mode == 'depth' else bfs
    for v in range(graph.vertices_count()):
        if visited[v]:
            continue
        component = []
        traversal(v, component)
        components.append(component)
    return components


def connected_disjoint_set(graph: Graph):
    """
    Find connected components in `graph` using a disjoint set.
    `graph` must be undirected, otherwise, the algorithm can not assure the components are strongly connected.

    > complexity:
    - time: `O(v + e)`, the extra `v` is due to disjoint set operations to extract component as a `int[][]` object
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search components

    > `return: int[][]`: list containing connected vertices ids
    """
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    disjoint_set = DisjointSet(graph.vertices_count())
    for edge in graph.edges():
        disjoint_set.union(edge._source, edge._target)
    components = [[] for i in range(disjoint_set.sets())]
    index = 0
    indices = {}
    for v in range(graph.vertices_count()):
        component = disjoint_set.find(v)
        if component not in indices:
            indices[component] = index
            index += 1
        components[indices[component]].append(v)
    return components


def biconnected_tarjan(graph: Graph):
    """
    Tarjan's and Hopcroft's Biconnected Components algorithm.
    `graph` must be undirected, otherwise, the algorithm can not assure the components are biconnected.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search components

    > `return: (int[], (int, int), int[][])`: tuple containing articulations, bridges and biconnected components
    """
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    next_order = [0]
    order = [None] * graph.vertices_count()  # also encode visited (order[v] is not none)
    low = [None] * graph.vertices_count()
    stack = collections.deque()
    articulations = set()
    bridges = []
    components = []

    def dfs(v: int, parent: int):
        order[v] = low[v] = next_order[0]
        next_order[0] += 1
        children = 0
        for edge in graph.edges(v):
            if order[edge._target] is None:  # not visited
                children += 1
                stack.append(edge)
                dfs(edge._target, v)
                low[v] = min(low[v], low[edge._target])
                if parent is None and children > 1 or \
                        parent is not None and order[v] <= low[edge._target]:  # component found
                    if order[v] < low[edge._target]:  # bridge found
                        bridges.append((edge._source, edge._target))
                    articulations.add(v)  # articulations comming from bridges or cycles
                    target = edge._target
                    component = set()
                    while True:
                        edge = stack.pop()
                        component.add(edge._source)
                        component.add(edge._target)
                        if edge._source == v and edge._target == target:
                            break
                    components.append(component)
            elif parent != edge._target and low[v] > order[edge._target]:
                low[v] = min(low[v], low[edge._target])
                stack.append(edge)

    for v in range(graph.vertices_count()):
        if order[v] is None:
            dfs(v, None)
        stack.clear()
    return (articulations, bridges, components)


def strong_connected_tarjan(graph: Graph):
    """
    Tarjan's Strongly Connected Components algorithm.
    Tarjan's algorithm can also be used for topological sorting.
    If the graph being processed is a directed acyclic graph, each component will contain a single vertex and components
    will be in a reverse topological order.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search components

    > `return: int[][]`: list containing strongly connected vertices ids
    """
    next_order = [0]
    order = [None] * graph.vertices_count()  # also encode visited and stacked (order[v] is not None, order[v] != - 1)
    low = [None] * graph.vertices_count()
    stack = collections.deque()
    components = []

    def dfs(v: int):
        order[v] = low[v] = next_order[0]
        next_order[0] += 1
        stack.append(v)
        for edge in graph.edges(v):
            if order[edge._target] is None:  # not visited
                dfs(edge._target)
            if order[edge._target] != -1:  # stacked (can not be unvisited due to step above)
                low[v] = min(low[v], low[edge._target])
        if low[v] != order[v]:
            return
        component = []
        while True:
            u = stack.pop()
            order[u] = -1
            component.append(u)
            if u == v:
                break
        components.append(component)

    for v in range(graph.vertices_count()):
        if order[v] is None:
            dfs(v)
    return components


def strong_connected_kosaraju(graph: Graph):
    """
    Kosraju's Strongly Connected Components algorithm.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to search components

    > `return: int[][]`: list containing strongly connected vertices ids
    """
    visited = [False] * graph.vertices_count()
    stack = collections.deque()

    def dfs_stack(v: int):
        visited[v] = True
        for edge in graph.edges(v):
            if not visited[edge._target]:
                dfs_stack(edge._target)
        stack.append(v)

    def dfs_component(v: int, component: list):
        component.append(v)
        visited[v] = True
        for edge in graph.edges(v):
            if not visited[edge._target]:
                dfs_component(edge._target, component)

    for v in range(graph.vertices_count()):
        if visited[v]:
            continue
        dfs_stack(v)

    transposed_graph = graph.transposed()
    visited = [False] * graph.vertices_count()
    components = []
    while len(stack) > 0:
        v = stack.pop()
        if visited[v]:
            continue
        component = []
        dfs_component(v, component)
        components.append(component)
    return components


def test():
    from ..test import benchmark
    from .factory import random_undirected

    def test_biconnected_tarjan(graph):
        articulations, bridges, components = biconnected_tarjan(graph)
        return {'articulations': articulations, 'bridges': bridges, 'components': components}

    benchmark(
        [
            ('   connected traverse depth', lambda graph: connected_traverse(graph, mode='depth')),
            (' connected traverse breadth', lambda graph: connected_traverse(graph, mode='breadth')),
            ('     connected disjoint set', connected_disjoint_set),
            ('         biconnected tarjan', test_biconnected_tarjan),
            ('    strong connected tarjan', strong_connected_tarjan),
            ('  strong connected kosaraju', strong_connected_kosaraju)
        ],
        test_input_iter=(random_undirected(i, 0.1) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100, 1000),
        bench_input=lambda s, r: random_undirected(s, 0.05)
    )


if __name__ == '__main__':
    test()
