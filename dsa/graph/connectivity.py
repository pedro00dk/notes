from ..dset import DisjointSet
from ..linear.queue import Queue
from ..linear.stack import Stack
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
    groups = []

    def dfs(id: int, group: list):
        group.append(graph.get_vertex(id))
        visited[id] = True
        for edge in graph.edges(id):
            if not visited[edge._target]:
                dfs(edge._target, group)

    def bfs(id: int, group: list):
        queue = Queue()
        queue.offer(id)
        while not queue.empty():
            id = queue.poll()
            group.append(graph.get_vertex(id))
            visited[id] = True
            for edge in graph.edges(id):
                if not visited[edge._target]:
                    dfs(edge._target, group)

    traversal = dfs if mode == 'depth' else bfs

    for id in range(graph.vertices_count()):
        if visited[id]:
            continue
        group = []
        traversal(id, group)
        groups.append(group)
    return groups


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
    groups = [[] for i in range(disjoint_set.sets())]
    index = 0
    indices = {}
    for id in range(graph.vertices_count()):
        group = disjoint_set.find(id)
        if group not in indices:
            indices[group] = index
            index += 1
        groups[indices[group]].append(graph.get_vertex(id))
    return groups


def biconnected_tarjan(graph: Graph):
    """
    Tarjan's and Hopcroft's Biconnected Components algorithm.
    `graph` must be undirected, otherwise, the algorithm can not assure the groups are biconnected.

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search groups

    > `return: (Vertex[], Vertex[][])`: tuple containing articulation points and biconnected groups
    """
    if not graph.is_undirected():
        raise Exception('connected algorithm only works with undirected graphs')
    next_order = [0]
    order = [None] * graph.vertices_count()  # also used to encode visited (None)
    low = [None] * graph.vertices_count()
    parent = [None] * graph.vertices_count()
    stack = Stack()

    articulations = set()
    groups = []

    def dfs(id: int):
        order[id] = low[id] = next_order[0]
        next_order[0] += 1
        children = 0
        for edge in graph.edges(id):
            if order[edge._target] is None:  # not visited
                parent[edge._target] = id
                children += 1
                stack.push(edge)
                dfs(edge._target)
                low[id] = min(low[id], low[edge._target])
                if parent[id] is None and children > 1 or parent[id] is not None and low[edge._target] >= order[id]:
                    articulations.add(id)
                    target = edge._target
                    group = set()
                    while True:
                        edge = stack.pop()
                        group.add(edge._source)
                        group.add(edge._target)
                        if edge._source == id and edge._target == target:
                            break
                    groups.append([graph.get_vertex(v) for v in group])
            elif parent[id] != edge._target and low[id] > order[edge._target]:
                low[id] = min(low[id], low[edge._target])
                stack.push(edge)

    for id in range(graph.vertices_count()):
        if order[id] is None:
            dfs(id)
        while not stack.empty():
            stack.pop()

    return ([graph.get_vertex(v) for v in articulations], groups)


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
    order = [None] * graph.vertices_count()  # also used to encode visited and stacked (None, -1)
    low = [None] * graph.vertices_count()
    stack = Stack()
    groups = []

    def dfs(id: int):
        order[id] = low[id] = next_order[0]
        next_order[0] += 1
        stack.push(id)
        for edge in graph.edges(id):
            if order[edge._target] is None:  # not visited
                dfs(edge._target)
            if order[edge._target] != -1:  # stacked
                low[id] = min(low[id], low[edge._target])
        if low[id] == order[id]:
            group = []
            while True:
                nid = stack.pop()
                order[nid] = -1
                group.append(graph.get_vertex(nid))
                if nid == id:
                    break
            groups.append(group)

    for id in range(graph.vertices_count()):
        if order[id] is None:
            dfs(id)
    return groups


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
    stack = Stack()

    def dfs_stack(id: int):
        visited[id] = True
        for edge in graph.edges(id):
            if not visited[edge._target]:
                dfs_stack(edge._target)
        stack.push(id)

    def dfs_group(id: int, group: list):
        group.append(graph.get_vertex(id))
        visited[id] = True
        for edge in graph.edges(id):
            if not visited[edge._target]:
                dfs_group(edge._target, group)

    for id in range(graph.vertices_count()):
        if visited[id]:
            continue
        dfs_stack(id)

    transposed_graph = graph.transposed()
    visited = [False] * graph.vertices_count()
    groups = []

    while not stack.empty():
        id = stack.pop()
        if visited[id]:
            continue
        group = []
        dfs_group(id, group)
        groups.append(group)
    return groups


def test():
    from ..test import benchmark
    from . import factory
    benchmark(
        [
            (
                '   connected traverse depth',
                lambda graph: [[vertex._id for vertex in group] for group in connected_traverse(graph, mode='depth')]
            ),
            (
                ' connected traverse breadth',
                lambda graph: [[vertex._id for vertex in group] for group in connected_traverse(graph, mode='breadth')]
            ),
            (
                '     connected disjoint set',
                lambda graph: [[vertex._id for vertex in group] for group in connected_disjoint_set(graph)]
            ),
            (
                '         biconnected trajan',
                lambda graph: [[vertex._id for vertex in group] for group in biconnected_tarjan(graph)[1]]
            ),
            (
                '    strong connected tarjan',
                lambda graph: [[vertex._id for vertex in group] for group in strong_connected_tarjan(graph)]
            ),
            (
                '  strong connected kosaraju',
                lambda graph: [[vertex._id for vertex in group] for group in strong_connected_kosaraju(graph)]
            )
        ],
        test_input_iter=(factory.random_undirected(i, 0.1) for i in (5, 10, 15, 20)),
        bench_size_iter=(1, 10, 100, 1000),
        bench_input=lambda s, r: factory.random_undirected(s, 0.05),
    )


if __name__ == '__main__':
    test()
