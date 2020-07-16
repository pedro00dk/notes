from ..graph import Graph
from .tsp import tsp_brute_force, tsp_held_karp_bitset, tsp_held_karp_hashset


def hamiltonian_cycle(graph: Graph, tsp_algorithm):
    """
    Hamiltonian cycle algorithm based on traveling salesman algorithm.
    To find a cycle, a tsp algorithm is used.
    If `tsp_algorithm` result distance is not infinity, then a cycle exists.

    > complexity:
    - time: O(tsp_algorithm)
    - space: O(tsp_algorithm)

    > parameters:
    - `graph: Graph`: graph to find cycle
    - `tsp_algorithm: Graph => (int(), int | float)`: a tsp algorithm

    > `return: int()`: the cycle if it exists or `None` otherwise or if graph is empty
    """
    itinerary = tsp_algorithm(graph)
    if itinerary is None:
        return None
    path, distance = itinerary
    return path if distance != float('inf') else None


def hamiltonian_path(graph: Graph, tsp_algorithm):
    """
    Hamiltonian path algorithm based on traveling salesman algorithm.
    To find a path, a tsp algorithm is used.
    If `tsp_algorithm` result distance is not infinity or contains at most 1one infinity edge, then a path exists.

    > complexity:
    - time: O(tsp_algorithm)
    - space: O(tsp_algorithm)

    > parameters:
    - `graph: Graph`: graph to find path
    - `tsp_algorithm: Graph => (int(), int | float)`: a tsp algorithm

    > `return: int()`: the path if it exists or `None` otherwise or if graph is empty
    """
    itinerary = tsp_algorithm(graph)
    if itinerary is None:
        return None
    path, distance = itinerary
    if distance != float('inf'):
        return path
    matrix = graph.adjacency_matrix()
    infinity_edges = []
    for i in range(len(path) - 1):
        if matrix[path[i]][path[i + 1]] == float('inf'):
            infinity_edges.append((i, i + 1))
    return path[infinity_edges[0][1]:] + path[:infinity_edges[0][0]] if len(infinity_edges) == 1 else None


def test():
    from ...test import benchmark
    from ..factory import random_undirected
    benchmark(
        [
            ('hamiltonian cycle > tsp brute force', lambda graph: hamiltonian_cycle(graph, tsp_brute_force)),
            (' hamiltonian path > tsp brute force', lambda graph: hamiltonian_path(graph, tsp_brute_force)),
            ('     hamiltonina cycle > tsp bitset', lambda graph: hamiltonian_cycle(graph, tsp_held_karp_bitset)),
            ('      hamiltonina path > tsp bitset', lambda graph: hamiltonian_path(graph, tsp_held_karp_bitset)),
            ('    hamiltonina cycle > tsp hashset', lambda graph: hamiltonian_cycle(graph, tsp_held_karp_hashset)),
            ('     hamiltonina path > tsp hashset', lambda graph: hamiltonian_path(graph, tsp_held_karp_hashset))
        ],
        test_input_iter=(random_undirected(i, density=0.8) for i in (2, 3, 4, 5, 6, 7)),
        bench_size_iter=range(0, 11),
        bench_input=lambda s, r: random_undirected(s)
    )


if __name__ == '__main__':
    test()
