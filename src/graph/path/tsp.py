import itertools

from ..graph import Graph


def tsp_brute_force(graph: Graph, /, start=0, absent_edge_length=float('inf')):
    """
    Brute force traveling salesman problem implementation.
    If `graph` is not complete and a path is not found, infinity is returned as distance and the path is invalid.

    > optimizations:
    - remove `start` vertex from permutations because it is fixed, this reduces the complexity from `O((v + 1)!)`
        (`v!` permutations * `v` distance computations) to `O(v!)` (`(v - 1)!` permutations * `v` distance computations)

    > complexity:
    - time: `O(v!)`
    - space: `O(v**2)` due to adjacency matrix creation

    > parameters:
    - `graph: Graph`: graph to find itinerary
    - `start: int? = 0`: start vertex
    - `absent_edge_length: (int | float)? = float('inf')`: length to use for absent edges, usually this algorithm is
        used in complete graphs, but when used as a hamiltonian path algorithm, this value must not be infinity, this
        allows finding paths with the minimal amount of absent edges.

    > `return: (int | float, int())`: the best distance and best path
    """
    if graph.vertices_count() == 0:
        raise Exception('graph must contain at least 1 vertex')
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    matrix = graph.adjacency_matrix()
    vertices = [v for v in range(graph.vertices_count()) if v != start or graph.vertices_count() == 1]
    distance = float('inf')
    path = ()
    for permutation in itertools.permutations(vertices):
        permutation_distance = matrix[permutation[-1]][start] + matrix[start][permutation[0]]
        for i in range(len(permutation) - 1):
            permutation_distance += matrix[permutation[i]][permutation[i + 1]]
        if permutation_distance >= distance:
            continue
        distance = permutation_distance
        path = permutation
    return distance, (start, *(path if graph.vertices_count() > 1 else ()))


def tsp_held_karp_bitset(graph: Graph, /, start=0, absent_edge_length=float('inf')):
    """
    Held-Karp traveling salesman problem implementation.
    If `graph` is not complete and a path is not found, infinity is returned as distance and the path is invalid.

    This implementation is based on bitsets, where a set of vertices is represented by a single number.
    Ex.: (little endian) 100110 --> 1  1  0  1  0  1 --> (1, 5) (1, 4) (0, 3) (1, 2) (0, 1) (1, 0) --> (0, 2, 4, 5).
    In python, this implementation only becomes faster for large values of `v` (> 15).
    For lower level languages, this implementation should be faster than the hashset implementation most of the times.
    The bitset implementation uses `v` times more memory than the hashset implementation.
    The used memory in this implementation is `v * (2**v)`, where in the hashset implementation, the memory usage grows
    up to `sum(c(v, k) for k in range(0, v))` which is equals to `2**v - 1`

    > complexity:
    - time: `O((2**v)*(v**2))`
    - space: `O(v*(2**v))`

    > parameters:
    - `graph: Graph`: graph to find itinerary
    - `start: int? = 0`: start vertex
    - `absent_edge_length: (int | float)? = float('inf')`: length to use for absent edges, usually this algorithm is
        used in complete graphs, but when used as a hamiltonian path algorithm, this value must not be infinity, this
        allows finding paths with the minimal amount of absent edges.

    > `return: (int | float, int())`: the best distance and best path
    """
    if graph.vertices_count() == 0:
        raise Exception('graph must contain at least 1 vertex')
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    matrix = graph.adjacency_matrix()
    paths = [[None] * (1 << graph.vertices_count()) for i in range(graph.vertices_count())]

    def bit_combinations(n: int, k: int):
        for combination in itertools.combinations([*range(n)], k):
            v = 0
            for bit in combination:
                v |= 1 << bit
            yield v

    # add first paths from start to each vertex
    for v in range(graph.vertices_count()):
        paths[v][0] = (matrix[start][v], start)

    # compute best path of all subsets based on smaller subsets
    for k in range(1, graph.vertices_count()):
        for subset in bit_combinations(graph.vertices_count(), k):
            if subset & (1 << start) != 0:
                continue
            for v in range(graph.vertices_count()):  # vertex to increase path
                if v == start or subset & (1 << v) != 0:
                    continue
                best_subpath_distance = float('inf')
                best_parent = None
                for u in range(graph.vertices_count()):  # vertex already in path
                    if u == start or u == v or subset & (1 << u) == 0:
                        continue
                    subpath_distance = paths[u][subset ^ (1 << u)][0] + matrix[u][v]
                    if subpath_distance >= best_subpath_distance:
                        continue
                    best_subpath_distance = subpath_distance
                    best_parent = u
                paths[v][subset] = (best_subpath_distance, best_parent)

    # get best distance from subset containing all vertices except start, to start
    final_subset = (1 << graph.vertices_count()) - 1 ^ (1 << start)
    distance = float('inf') if final_subset != 0 else 0   # 0 means graph contains only one vertex
    parent = None
    for u in range(graph.vertices_count()):
        if u == start:
            continue
        subpath_distance = paths[u][final_subset ^ (1 << u)][0] + matrix[u][start]
        if subpath_distance >= distance:
            continue
        distance = subpath_distance
        parent = u
    paths[start][final_subset] = (distance, parent)

    # get best path from subset containing all vertices except start
    subset = final_subset
    path = []
    while parent is not None and parent != start:  # parent is none if graph contains only one vertex
        path.append(parent)
        subset ^= (1 << parent)
        parent = paths[parent][subset][1]
    path.append(start)

    return distance, (*reversed(path),)


def tsp_held_karp_hashset(graph: Graph, /, start=0, absent_edge_length=float('inf')):
    """
    Held-Karp traveling salesman problem implementation.
    If `graph` is not complete and a path is not found, infinity is returned as distance and the path is invalid.

    This implementation is based on hashsets, where a set of vertices is represented by a frozenset.

    > complexity:
    - time: `O((2**v)*(v**2))`
    - space: `O(2**v)`

    > parameters:
    - `graph: Graph`: graph to find itinerary (must be complete)
    - `start: int? = 0`: start vertex
    - `absent_edge_length: (int | float)? = float('inf')`: length to use for absent edges, usually this algorithm is
        used in complete graphs, but when used as a hamiltonian path algorithm, this value must not be infinity, this
        allows finding paths with the minimal amount of absent edges.

    > `return: (int | float, int())`: the best distance and best path
    """
    if graph.vertices_count() == 0:
        raise Exception('graph must contain at least 1 vertex')
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    matrix = graph.adjacency_matrix()
    paths = {}

    # add first paths from start to each vertex
    for v in range(graph.vertices_count()):
        paths[(v, frozenset())] = (matrix[start][v], start)

    # compute best path of all subsets based on smaller subsets
    for k in range(1, graph.vertices_count()):
        for tupleset in itertools.combinations([*range(graph.vertices_count())], k):
            subset = frozenset(tupleset)
            if start in subset:
                continue
            for v in range(graph.vertices_count()):  # vertex to increase path
                if v == start or v in subset:
                    continue
                best_subpath_distance = float('inf')
                best_parent = None
                for u in subset:  # vertex already in path
                    subpath_distance = paths[(u, subset.difference((u,)))][0] + matrix[u][v]
                    if subpath_distance >= best_subpath_distance:
                        continue
                    best_subpath_distance = subpath_distance
                    best_parent = u
                paths[(v, subset)] = (best_subpath_distance, best_parent)

    # get best distance from subset containing all vertices except start, to start
    final_subset = frozenset(range(graph.vertices_count())).difference((start,))
    distance = float('inf') if len(final_subset) > 0 else 0  # 0 means graph contains only one vertex
    parent = None
    for u in final_subset:
        subpath_distance = paths[(u, final_subset.difference((u,)))][0] + matrix[u][start]
        if subpath_distance >= distance:
            continue
        distance = subpath_distance
        parent = u
    paths[(start, final_subset)] = (distance, parent)

    # get best path from subset containing all vertices except start
    subset = final_subset
    path = []
    while parent is not None and parent != start:  # parent is none if graph contains only one vertex
        path.append(parent)
        subset = subset.difference((parent,))
        parent = paths[(parent, subset)][1]
    path.append(start)

    return distance, (*reversed(path),)


def tsp_nearest_heighbor(graph: Graph, /, start=0):
    """
    Nearest neighbors traveling salesman problem implementation (heuristic).
    If graph is not complete and a path is not found, infinity is returned as distance and the path is invalid.

    This implementation may not produce optmal results.

    > complexity:
    - time: `O((2**v)*(v**2))`
    - space: `O(2**v)`

    > parameters:
    - `graph: Graph`: graph to find itinerary (must be complete)
    - `start: int? = 0`: start vertex

    > `return: (int | float, int())`: the best distance and best path (heuristic)
    """
    if graph.vertices_count() == 0:
        raise Exception('graph must contain at least 1 vertex')
    if start < 0 or start >= graph.vertices_count():
        raise IndexError(f'start vertex ({start}) out of range [0, {graph.vertices_count()})')
    visited = [False] * graph.vertices_count()
    distance = 0
    path = [start]
    visited[start] = True
    for i in range(graph.vertices_count() - 1):
        best_segment_distance = float('inf')
        best_target = None
        for edge in graph.edges(path[-1]):
            if visited[edge._target] or edge.length >= best_segment_distance:
                continue
            best_segment_distance = edge.length
            best_target = edge._target
        distance += best_segment_distance
        path.append(best_target)
        visited[best_target] = True
    distance += min(edge.length for edge in graph.edges(path[-1]) if edge._target == start) if len(path) > 1 else 0
    return distance, (*path,)


def test():
    from ...test import benchmark, heuristic_approximation
    from ..factory import complete

    def save_cost(algorithm, input, costs):
        result = algorithm(input)
        costs.append(result[0])
        return result

    optimal_costs = []
    nearest_neighbor_costs = []
    print('all algorithms')
    benchmark(
        [
            ('     tsp brute force', lambda graph: save_cost(tsp_brute_force, graph, optimal_costs)),
            ('          tsp bitset', tsp_held_karp_bitset),
            ('         tsp hashset', tsp_held_karp_hashset),
            ('tsp nearest neighbor', lambda graph: save_cost(tsp_nearest_heighbor, graph, nearest_neighbor_costs))
        ],
        test_inputs=(complete(i, el_range=(0, 10)) for i in (2, 4, 6)),
        bench_sizes=range(1, 11),
        bench_input=lambda s: complete(s, el_range=(0, 100))
    )
    print('without brute force')
    benchmark(
        [
            ('          tsp bitset', lambda graph: save_cost(tsp_held_karp_bitset, graph, optimal_costs)),
            ('         tsp hashset', tsp_held_karp_hashset),
            ('tsp nearest neighbor', lambda graph: save_cost(tsp_nearest_heighbor, graph, nearest_neighbor_costs))
        ],
        test_inputs=(),
        bench_sizes=range(11, 15),
        bench_input=lambda s: complete(s, el_range=(0, 100))
    )
    print('only heuristics')
    benchmark(
        [
            ('tsp nearest neighbor', tsp_nearest_heighbor)
        ],
        test_inputs=(),
        bench_sizes=(20, 50, 100),
        bench_input=lambda s: complete(s, el_range=(0, 100))
    )
    heuristic_approximation('nearest neighbors', optimal_costs, nearest_neighbor_costs)


if __name__ == '__main__':
    test()
