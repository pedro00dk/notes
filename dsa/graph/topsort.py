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
    root_vertices = [id for id, count in enumerate(incoming_edges) if count == 0]
    order = []
    while len(root_vertices) > 0:
        id = root_vertices.pop()
        order.append(graph.get_vertex(id))
        for edge in graph.edges(id):
            if edge._target is None:  # removed edge
                continue
            target = edge._target
            edge._target = None  # remove edge
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

    def dfs(id):
        if visited[id] == 2:  # visited
            return
        if visited[id] == 1:  # temporary
            raise Exception('topological sort only works with directed acyclic graphs')
        visited[id] = 1
        for edge in graph.edges(id):
            dfs(edge._target)
        visited[id] = 2
        order.append(graph.get_vertex(id))

    for id in range(graph.vertices_count()):
        if visited[id] != 2:  # unvisited or temporary
            dfs(id)
    order.reverse()
    return order


def test():
    from ..test import benchmark
    from . import factory
    benchmark(
        [
            (
                '    topological sort khan',
                lambda graph: [vertex._id for vertex in topsort_khan(graph)]
            ),
            (
                '     topological sort dfs',
                lambda graph: [vertex._id for vertex in topsort_dfs(graph)]
            )
        ],
        test_input_iter=(factory.random_dag() for i in range(5)),
        bench_size_iter=(1, 10, 100, 1000),
        bench_input=lambda s, r: factory.random_dag((s // 20, s // 10), (5, 10))
    )


if __name__ == '__main__':
    test()
