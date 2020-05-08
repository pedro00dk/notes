from .graph import Graph
from .topsort import topological_sort


def single_source_shortest_path_dag(graph, source):
    if source < 0 or source >= len(graph):
        raise IndexError('out of range')
    if len(graph) == 0:
        return
    distances = [(float('inf'), None)] * len(graph)
    distances[source] = (0, None)
    for vertex in topological_sort(graph):
        weight, edges = graph.vertices[vertex]
        for target, edge_weight in edges:
            distance = distances[vertex][0] + edge_weight
            if distances[target][0] > distance:
                distances[target] = (distance, vertex)
    return distances


def single_source_longest_path_dag(graph, source):
    if source < 0 or source >= len(graph):
        raise IndexError('out of range')
    if len(graph) == 0:
        return
    distances = [(float('inf'), None)] * len(graph)
    distances[source] = (0, None)
    for vertex in topological_sort(graph):
        weight, edges = graph.vertices[vertex]
        for target, edge_weight in edges:
            distance = distances[vertex][0] - edge_weight
            if distances[target][0] > distance:
                distances[target] = (distance, vertex)
    inf = float('inf')
    distances = [(-distance if distance != inf else inf, previous) for distance, previous in distances]
    return distances


def test():
    g = Graph.random_dag(ew_range=(-5, 15))
    print(g)
    print(single_source_shortest_path_dag(g, 0))
    print(single_source_longest_path_dag(g, 0))
    print()


if __name__ == '__main__':
    test()
