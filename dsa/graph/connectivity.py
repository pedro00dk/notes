import collections

from ..dset import DisjointSet
from .graph import Graph


def connected_traverse(graph: Graph, /, mode='depth'):
    """
    Find connected groups in `graph` using traversals to expand groups.
    `graph` must be undirected, otherwise, the algorithm can not assure the groups are strongly connected.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search groups
    - `mode: ('depth' | 'breadth')? = 'depth'`: the traversal algorithm to use

    > `return: Vertex[][]`: list containing vertex groups
    """
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    visited = [False] * graph.vertices_count()
    components = []

    def dfs(id: int, component: list):
        component.append(graph.get_vertex(id))
        visited[id] = True
        for edge in graph.edges(id):
            if not visited[edge._target]:
                dfs(edge._target, component)

    def bfs(id: int, component: list):
        queue = collections.deque()
        queue.append(id)
        while len(queue) > 0:
            id = queue.popleft()
            component.append(graph.get_vertex(id))
            visited[id] = True
            for edge in graph.edges(id):
                if not visited[edge._target]:
                    dfs(edge._target, component)

    traversal = dfs if mode == 'depth' else bfs

    for id in range(graph.vertices_count()):
        if visited[id]:
            continue
        group = []
        traversal(id, group)
        components.append(group)
    return components


def connected_disjoint_set(graph: Graph):
    """
    Find connected groups in `graph` using a disjoint set.
    `graph` must be undirected, otherwise, the algorithm can not assure the groups are strongly connected.

    > complexity:
    - time: `O(v + e)`, the extra `v` is due to disjoint set operations to extract group as a `Vertex[][]` object
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search groups

    > `return: Vertex[][]`: list containing vertex groups
    """
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    disjoint_set = DisjointSet(graph.vertices_count())
    for edge in graph.edges():
        disjoint_set.union(edge._source, edge._target)
    components = [[] for i in range(disjoint_set.sets())]
    index = 0
    indices = {}
    for id in range(graph.vertices_count()):
        component = disjoint_set.find(id)
        if component not in indices:
            indices[component] = index
            index += 1
        components[indices[component]].append(graph.get_vertex(id))
    return components


def biconnected_tarjan(graph: Graph):
    """
    Tarjan's and Hopcroft's Biconnected Components algorithm.
    `graph` must be undirected, otherwise, the algorithm can not assure the groups are biconnected.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search groups

    > `return: (Vertex[], Edge[], Vertex[][])`: tuple containing articulations, bridges and biconnected groups
    """
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    next_order = [0]
    order = [None] * graph.vertices_count()  # also encode visited (order[id] is not none)
    low = [None] * graph.vertices_count()
    stack = collections.deque()
    articulations = set()
    bridges = []
    components = []

    def dfs(id: int, parent: int):
        order[id] = low[id] = next_order[0]
        next_order[0] += 1
        children = 0
        for edge in graph.edges(id):
            if order[edge._target] is None:  # not visited
                children += 1
                stack.append(edge)
                dfs(edge._target, id)
                low[id] = min(low[id], low[edge._target])
                if parent is None and children > 1 or \
                        parent is not None and order[id] <= low[edge._target]:  # component found
                    if order[id] < low[edge._target]:  # bridge found
                        bridges.append(edge)
                    articulations.add(id)  # articulations comming from bridges or cycles
                    target = edge._target
                    component = set()
                    while True:
                        edge = stack.pop()
                        component.add(edge._source)
                        component.add(edge._target)
                        if edge._source == id and edge._target == target:
                            break
                    components.append([graph.get_vertex(v) for v in component])
            elif parent != edge._target and low[id] > order[edge._target]:
                low[id] = min(low[id], low[edge._target])
                stack.append(edge)

    for id in range(graph.vertices_count()):
        if order[id] is None:
            dfs(id, None)
        stack.clear()

    return ([graph.get_vertex(v) for v in articulations], bridges, components)


def strong_connected_tarjan(graph: Graph):
    """
    Tarjan's Strongly Connected Components algorithm.
    Tarjan's algorithm can also be used for topological sorting.
    If the graph being processed is a directed acyclic graph, each group will contain a single vertex and groups will be
    in a reverse topological order.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search groups

    > `return: Vertex[][]`: list containing vertex groups
    """
    next_order = [0]
    order = [None] * graph.vertices_count()  # also encode visited and stacked (order[id] is not None, order[id] != - 1)
    low = [None] * graph.vertices_count()
    stack = collections.deque()
    components = []

    def dfs(id: int):
        order[id] = low[id] = next_order[0]
        next_order[0] += 1
        stack.append(id)
        for edge in graph.edges(id):
            if order[edge._target] is None:  # not visited
                dfs(edge._target)
            if order[edge._target] != -1:  # stacked (can not be unvisited due to step above)
                low[id] = min(low[id], low[edge._target])
        if low[id] != order[id]:
            return
        component = []
        while True:
            vid = stack.pop()
            order[vid] = -1
            component.append(graph.get_vertex(vid))
            if vid == id:
                break
        components.append(component)

    for id in range(graph.vertices_count()):
        if order[id] is None:
            dfs(id)
    return components


def strong_connected_kosaraju(graph: Graph):
    """
    Kosraju's Strongly Connected Components algorithm.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v + e)`

    > parameters:
    - `graph: Graph`: graph to search groups

    > `return: Vertex[][]`: list containing vertex groups
    """
    visited = [False] * graph.vertices_count()
    stack = collections.deque()

    def dfs_stack(id: int):
        visited[id] = True
        for edge in graph.edges(id):
            if not visited[edge._target]:
                dfs_stack(edge._target)
        stack.append(id)

    def dfs_component(id: int, group: list):
        group.append(graph.get_vertex(id))
        visited[id] = True
        for edge in graph.edges(id):
            if not visited[edge._target]:
                dfs_component(edge._target, group)

    for id in range(graph.vertices_count()):
        if visited[id]:
            continue
        dfs_stack(id)

    transposed_graph = graph.transposed()
    visited = [False] * graph.vertices_count()
    components = []

    while len(stack) > 0:
        id = stack.pop()
        if visited[id]:
            continue
        component = []
        dfs_component(id, component)
        components.append(component)
    return components


def test():
    from ..test import benchmark
    from .factory import random_undirected

    def test_biconnected_tarjan(graph):
        articulations, bridges, components = biconnected_tarjan(graph)
        return {
            'articulations': [vertex._id for vertex in articulations],
            'bridges': [(edge._source, edge._target) for edge in bridges],
            'components': [[vertex._id for vertex in component] for component in components]
        }

    benchmark(
        [
            (
                '   connected traverse depth',
                lambda graph: [[vertex._id for vertex in component]
                               for component in connected_traverse(graph, mode='depth')]
            ),
            (
                ' connected traverse breadth',
                lambda graph: [[vertex._id for vertex in component]
                               for component in connected_traverse(graph, mode='breadth')]
            ),
            (
                '     connected disjoint set',
                lambda graph: [[vertex._id for vertex in component] for component in connected_disjoint_set(graph)]
            ),
            (
                '         biconnected tarjan',
                lambda graph: test_biconnected_tarjan(graph)
            ),
            (
                '    strong connected tarjan',
                lambda graph: [[vertex._id for vertex in component] for component in strong_connected_tarjan(graph)]
            ),
            (
                '  strong connected kosaraju',
                lambda graph: [[vertex._id for vertex in component] for component in strong_connected_kosaraju(graph)]
            )
        ],
        test_input_iter=(random_undirected(i, 0.1) for i in (5, 10, 15, 20)),
        bench_size_iter=(0, 1, 10, 100, 1000),
        bench_input=lambda s, r: random_undirected(s, 0.05)
    )


if __name__ == '__main__':
    test()
