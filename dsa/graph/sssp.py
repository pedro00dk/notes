from ..search.heap import Heap
from .graph import Graph
from .topsort import topological_sort


def single_source_shortest_path_dag(graph, source):
    if source < 0 or source >= len(graph):
        raise IndexError('out of range')
    if len(graph) == 0:
        return []
    distances = [(float('inf'), None)] * len(graph)
    distances[source] = (0, None)
    for vertex in topological_sort(graph):
        weight, edges = graph.vertices[vertex]
        vertex_distance = distances[vertex][0]
        for target, edge_weight in edges:
            target_distance = vertex_distance + edge_weight
            if distances[target][0] > target_distance:
                distances[target] = (target_distance, vertex)
    return distances


def single_source_longest_path_dag(graph, source):
    if source < 0 or source >= len(graph):
        raise IndexError('out of range')
    if len(graph) == 0:
        return []
    distances = [(float('inf'), None)] * len(graph)
    distances[source] = (0, None)
    for vertex in topological_sort(graph):
        weight, edges = graph.vertices[vertex]
        vertex_distance = distances[vertex][0]
        for target, edge_weight in edges:
            target_distance = vertex_distance - edge_weight
            if distances[target][0] > target_distance:
                distances[target] = (target_distance, vertex)
    inf = float('inf')
    distances = [(-target_distance if distance != inf else inf, previous) for distance, previous in distances]
    return distances


def dijkstra(graph: Graph, source, sink=None):
    if source < 0 or source >= len(graph) or sink is not None and (sink < 0 or sink >= len(graph)):
        raise IndexError('out of range')
    if len(graph) == 0:
        return
    distances = [(float('inf'), None)] * len(graph)
    distances[source] = (0, None)
    heap = Heap(mode=lambda x, y: x[1] < y[1])
    heap.offer((source, 0))
    while len(heap) > 0:
        vertex, vertex_distance = heap.poll()
        if vertex == sink:
            break
        if distances[vertex][0] < vertex_distance:
            continue
        for target, edge_weight in graph.vertices[vertex][1]:
            target_distance = vertex_distance + edge_weight
            if distances[target][0] > target_distance:
                distances[target] = (target_distance, vertex)
                heap.offer((target, target_distance))
    return distances


def test():
    print('dags')
    for i in range(3):
        g = Graph.random_dag(ew_range=(1, 15))
        print(g)
        print('sssp', single_source_shortest_path_dag(g, 0))
        print('sslp', single_source_longest_path_dag(g, 0))
        print('dijkstra', dijkstra(g, 0))
        print()
    
    print('randoms')
    for i in range(5):
        g = Graph.random(10, ew_range=(1, 15))
        print(g)
        print('dijkstra', dijkstra(g, 0))
        print()


if __name__ == '__main__':
    test()
