from ..dset import DisjointSet
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
    visited = [False] * len(graph)
    groups = []
    for vertex in graph.vertices():
        if visited[vertex._id]:
            continue
        groups.append([vertex for vertex, *_ in graph.traverse(vertex._id, mode, visited=visited)])
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


def tarjan_scc(graph: Graph):
    """
    Tarjan's Strongly Connected Components algorithm.
    This algorithm uses the DFS already implemented in Graph.
    Because of that, there is less flexibility of the place where code can be executed in the DFS.
    As a result, extra logic is necessary to implement the algorithm:
    - the low_link comparison which is normally done after each in the vertex scope after each child DFS, is executed
        in the child scope when it returns (child has access to parent vertex)
    - conditions to avoid checks for completed groups in back edges are added because back edges are yielded just like
        any other edge

    > complexity:
    - time: `O(v + e)`
    - space: `O(v)`

    > parameters:
    - `graph: Graph`: graph to search groups

    > `return: Vertex[][]`: list containing vertex groups
    """
    next_order_id = 0
    order_ids = [None] * graph.vertices_count()  # also used to check if vertex is stacked (when value is not None)
    low_links = [None] * graph.vertices_count()
    visited = [False] * graph.vertices_count()
    stack = Stack()
    groups = []
    for vertex in graph.vertices():
        if visited[vertex._id]:
            continue
        for vertex, parent, *_, before, back in graph.traverse(vertex._id, 'depth', visited, True, True, True):
            if before and not back:
                order_ids[vertex._id] = low_links[vertex._id] = next_order_id
                next_order_id += 1
                stack.push(vertex._id)
            elif not before and order_ids[vertex._id] is not None:
                if parent is not None:
                    low_links[parent._id] = min(low_links[parent._id], low_links[vertex._id])
                if not back and low_links[vertex._id] == order_ids[vertex._id]:
                    group = []
                    while True:
                        id = stack.pop()
                        order_ids[id] = None
                        group.append(graph.get_vertex(id))
                        if id == vertex._id:
                            break
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
                '    tarjan strong connected',
                lambda graph: [[vertex._id for vertex in group] for group in tarjan_scc(graph)]
            )
        ],
        loads=[connected_traverse],
        test_input_iter=(factory.random_undirected(i, 0.1) for i in (5, 10, 15, 20)),
        bench_size_iter=(1, 10, 100, 1000),
        bench_input=lambda s, r: factory.random_undirected(s, 0.05),
        bench_tries=50
    )


if __name__ == '__main__':
    test()
