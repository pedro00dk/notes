import itertools
from typing import Any, Callable, Union, cast

from ..graph import Edge, Graph


def vertex_cover_brute_force(graph: Graph[Any, Any]) -> list[int]:
    """
    Brute force vertex cover algorithm.
    This algorithm mutates the graph to implement optimizations (`edge.data` field).

    > optimizations
    - try selecting vertices that are always in the selected group before the algorithm starts, a vertex `v` will always
        be selected if `v` has an edge to another vertex `u`, such that `u` has only that single edge.

    > complexity
    - time: `O((2**k)*v*e)`
    - space: `O(v + e)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`
    - `k`: number of vertices of the best cover

    > parameters
    - `graph`: graph to find cover
    - `return`: selection of vertices that cover all edges
    """
    if not graph.is_undirected():
        raise Exception("graph must be undirected")
    selected = [0.0] * graph.vertices_count()
    selected_marker = 1  # selected marker used to avoid reseting selected list after each failed combination
    for v in range(graph.vertices_count()):
        if selected[v] < selected_marker and graph.edges_count(v) == 1:
            selected[graph._edges[v][0].target] = float("inf")  # type: ignore
    selectable_vertices = [v for v, s in enumerate(selected) if s < selected_marker]
    uncovered_edges: list[Edge[Any]] = []
    for edge in graph.edges():
        if edge.data is None and selected[edge.source] < selected_marker and selected[edge.target] < selected_marker:
            uncovered_edges.append(edge)
            opposite = cast(Edge[Any], edge.opposite)
            edge.data = opposite.data = True  # avoid putting the opposite edge in uncovered edges
    for i in range(len(selectable_vertices)):
        for combination in itertools.combinations(selectable_vertices, i):
            for v in combination:
                selected[v] = selected_marker
            for edge in uncovered_edges:
                if selected[edge.source] < selected_marker and selected[edge.target] < selected_marker:
                    selected_marker += 1
                    break
            else:
                return [v for v, s in enumerate(selected) if s >= selected_marker]
    return []  # when graph is empty


def vertex_cover_greedy(graph: Graph[Any, Any]) -> list[int]:
    """
    Greedy vertex cover algorithm (heuristic).
    This algorithm cover remaining edges by selecting the vertex which has more edges.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find cover
    - `return`: selection of vertices that cover all edges (heuristic)
    """
    selected = [False] * graph.vertices_count()
    for edge in graph.edges():
        if selected[edge.source] or selected[edge.target]:
            continue
        v = edge.source if graph.edges_count(edge.source) > graph.edges_count(edge.target) else edge.target
        selected[v] = True
    return [v for v, s in enumerate(selected) if s]


def vertex_cover_greedy_double(graph: Graph[Any, Any]) -> list[int]:
    """
    Greedy double vertex cover algorithm (heuristic).
    This algorithm cover remaining edges selecting both vertices of the edge.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find cover
    - `return`: selection of vertices that cover all edges (heuristic)
    """
    selected = [False] * graph.vertices_count()
    for edge in graph.edges():
        if selected[edge.source] or selected[edge.target]:
            continue
        selected[edge.source] = selected[edge.target] = True
    return [v for v, s in enumerate(selected) if s]


def weighted_vertex_cover_brute_force(graph: Graph[Any, Any]) -> tuple[float, list[int]]:
    """
    Brute force weighted vertex cover algorithm.
    This algorithm mutates the graph to implement optimizations (`edge.data` field).
    The normal vertex cover minimizes the number of selected vertices, weighted cover minimizes the total cost first
    and then the number of vertices.

    > complexity
    - time: `O((2**v)*v*e)`
    - space: `O(v + e)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find cover
    - `return`: selection of vertices that cover all edges with minimal cost
    """
    if not graph.is_undirected():
        raise Exception("graph must be undirected")
    selected = [0] * graph.vertices_count()
    selected_marker = 1  # selected marker used to avoid reseting selected list after each failed combination
    uncovered_edges: list[Edge[Any]] = []
    for edge in graph.edges():
        if edge.data is None:
            uncovered_edges.append(edge)
            opposite = cast(Edge[Any], edge.opposite)
            edge.data = opposite.data = True  # avoid putting the opposite edge in uncovered edges
    best_cost = float("inf")
    best_cover = ()
    for i in range(graph.vertices_count()):
        for combination in itertools.combinations(range(graph.vertices_count()), i):
            cost = sum(graph.get_vertex(v).weight for v in combination)
            if cost >= best_cost:
                continue
            for v in combination:
                selected[v] = selected_marker
            for edge in uncovered_edges:
                if selected[edge.source] < selected_marker and selected[edge.target] < selected_marker:
                    selected_marker += 1
                    break
            else:
                best_cost = cost
                best_cover = combination
    return best_cost if len(best_cover) > 0 else 0, [*best_cover]


def weighted_vertex_cover_greedy(graph: Graph[Any, Any]) -> tuple[float, list[int]]:
    """
    Greedy weighted vertex cover algorithm (heuristic).
    This algorithm cover remaining edges by selecting the vertex with the better cost per edge
    (vertex weight / vertex edge count).
    The cost of a vertex is updated when it is not chosen.

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find cover
    - `return`: selection of vertices that cover all edges (heuristic)
    """
    selected = [False] * graph.vertices_count()
    remaining_edges = [graph.edges_count(v) for v in range(graph.vertices_count())]
    vertex_costs = [
        graph.get_vertex(v).weight / remaining_edges[v] if remaining_edges[v] > 0 else float("inf")
        for v in range(graph.vertices_count())
    ]
    for edge in graph.edges():
        if selected[edge.source] or selected[edge.target]:
            continue
        v = edge.source if vertex_costs[edge.source] > vertex_costs[edge.target] else edge.target
        u = edge.source if v == edge.target else edge.target
        selected[v] = True
        remaining_edges[u] -= 1
        vertex_costs[u] = graph.get_vertex(u).weight / remaining_edges[u] if remaining_edges[u] > 0 else float("inf")
    cover = [v for v, s in enumerate(selected) if s]
    cost = sum(graph.get_vertex(v).weight for v in cover)
    return cost, cover


def weighted_vertex_cover_pricing(graph: Graph[Any, Any]) -> tuple[float, list[int]]:
    """
    Pricing method for weighted vertex cover algorithm (heuristic).

    > complexity
    - time: `O(v + e)`
    - space: `O(v)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find cover
    - `return`: selection of vertices that cover all edges (heuristic)
    """
    remaining_price = [graph.get_vertex(v).weight for v in range(graph.vertices_count())]
    for edge in graph.edges():
        min_price = min(remaining_price[edge.source], remaining_price[edge.target])
        remaining_price[edge.source] -= min_price
        remaining_price[edge.target] -= min_price
    cover = [v for v, p in enumerate(remaining_price) if p == 0]
    cost = sum(graph.get_vertex(v).weight for v in cover)
    return cost, cover


def weighted_vertex_cover_pricing_sorted(graph: Graph[Any, Any]) -> tuple[float, list[int]]:
    """
    Pricing method with sorted edge weights for weighted vertex cover algorithm (heuristic).

    > complexity
    - time: `O(e*log(e) + v)`
    - space: `O(v + e)`
    - `v`: number of vertices in `graph`
    - `e`: number of edges in `graph`

    > parameters
    - `graph`: graph to find cover
    - `return`: selection of vertices that cover all edges (heuristic)
    """
    remaining_price = [graph.get_vertex(v).weight for v in range(graph.vertices_count())]
    sorted_edges = sorted(
        graph.edges(), key=lambda edge: min(remaining_price[edge.source], remaining_price[edge.target])
    )
    for edge in sorted_edges:
        min_price = min(remaining_price[edge.source], remaining_price[edge.target])
        remaining_price[edge.source] -= min_price
        remaining_price[edge.target] -= min_price
    cover = [v for v, p in enumerate(remaining_price) if p == 0]
    cost = sum(graph.get_vertex(v).weight for v in cover)
    return cost, cover


def test():
    from ...test import benchmark, heuristic_approximation
    from ..factory import random_undirected

    def save_size(
        algorithm: Callable[[Graph[Any, Any]], Union[list[int], tuple[float, list[int]]]],
        input: Graph[Any, Any],
        sizes: list[float],
    ) -> Union[list[int], tuple[float, list[int]]]:
        result = algorithm(input)
        sizes.append(len(result) if isinstance(result, list) else len(result[1]))
        return result

    def save_weight(
        algorithm: Callable[[Graph[Any, Any]], tuple[float, list[int]]], input: Graph[Any, Any], weights: list[float]
    ) -> tuple[float, list[int]]:
        result = algorithm(input)
        weights.append(result[0])
        return result

    optimal_sizes: list[float] = []
    greedy_sizes: list[float] = []
    greedy_double_sizes: list[float] = []
    optimal_weights: list[float] = []
    greedy_weights: list[float] = []
    pricing_weights: list[float] = []
    pricing_sorted_weights: list[float] = []
    benchmark(
        (
            (
                "            vertex cover brute force",
                lambda graph: save_size(vertex_cover_brute_force, graph, optimal_sizes),
            ),
            ("                 vertex cover greedy", lambda graph: save_size(vertex_cover_greedy, graph, greedy_sizes)),
            (
                "          vertex cover greedy double",
                lambda graph: save_size(vertex_cover_greedy_double, graph, greedy_double_sizes),
            ),
            (
                "   weighted vertex cover brute force",
                lambda graph: save_weight(weighted_vertex_cover_brute_force, graph, optimal_weights),
            ),
            (
                "        weighted vertex cover greedy",
                lambda graph: save_weight(weighted_vertex_cover_greedy, graph, greedy_weights),
            ),
            (
                "       weighted vertex cover pricing",
                lambda graph: save_weight(weighted_vertex_cover_pricing, graph, pricing_weights),
            ),
            (
                "weighted vertex cover pricing sorted",
                lambda graph: save_weight(weighted_vertex_cover_pricing_sorted, graph, pricing_sorted_weights),
            ),
        ),
        test_inputs=(*(random_undirected(i, vw_range=(1, 10)) for i in (4, 5, 6, 7)),),
        bench_sizes=(*range(10), *range(10, 16, 2)),
        bench_input=lambda s: random_undirected(s, vw_range=(1, 10)),
        preprocess_input=Graph[Any, Any].copy,
    )
    heuristic_approximation("greedy", optimal_sizes, greedy_sizes)
    heuristic_approximation("greedy double", optimal_sizes, greedy_double_sizes)
    heuristic_approximation("weighted greedy", optimal_weights, greedy_weights)
    heuristic_approximation("weighted pricing", optimal_weights, pricing_weights)
    heuristic_approximation("weighted pricing sorted", optimal_weights, pricing_sorted_weights)


if __name__ == "__main__":
    test()
