from ..graph import Graph
from .tsp import tsp_brute_force, tsp_held_karp_bitset, tsp_held_karp_hashset


def test():
    from ...test import benchmark
    from ..factory import random_undirected

    def hamiltonian_cycle(graph: Graph, tsp_algorithm):
        distance, path = tsp_brute_force(graph)
        return path if distance != float('inf') else None

    def hamiltonian_path(graph: Graph, tsp_algorithm):
        distance, path = tsp_brute_force(graph)
        if distance != float('inf'):
            return path
        matrix = graph.adjacency_matrix()
        infinity_edges = []
        for i in range(len(path) - 1):
            if matrix[path[i]][path[i + 1]] == float('inf'):
                infinity_edges.append((i, i + 1))
        return path[infinity_edges[0][1]:] + path[:infinity_edges[0][0]] if len(infinity_edges) == 1 else None

    benchmark(
        [
            ('hamiltonian cycle > tsp brute force', lambda graph: hamiltonian_cycle(graph, tsp_brute_force)),
            (' hamiltonian path > tsp brute force', lambda graph: hamiltonian_path(graph, tsp_brute_force)),
            ('     hamiltonina cycle > tsp bitset', lambda graph: hamiltonian_cycle(graph, tsp_held_karp_bitset)),
            ('      hamiltonina path > tsp bitset', lambda graph: hamiltonian_path(graph, tsp_held_karp_bitset)),
            ('    hamiltonina cycle > tsp hashset', lambda graph: hamiltonian_cycle(graph, tsp_held_karp_hashset)),
            ('     hamiltonina path > tsp hashset', lambda graph: hamiltonian_path(graph, tsp_held_karp_hashset))
        ],
        test_input_iter=(random_undirected(i) for i in (2, 4, 6)),
        bench_size_iter=range(0, 11),
        bench_input=lambda s, r: random_undirected(s)
    )


if __name__ == '__main__':
    test()
