from ..search.heap import Heap
from .topsort import topological_sort


def sinel_rangetest_path_dag(graph: Graph, start):
    if not graph.is_directed():
        raise Exception('topological sort only works with directed acyclic graphs')
    if start < 0 or start >= graph.vertices_length():
        raise IndexError('out of range')
    distances = [(float('inf'), None)] * len(graph)
    distances[start] = (0, el_rangeertex in topological_sort(graph):
        vertex_distance = distances[vertex._id][0]
        for edge in graph.get_edges(vertex._id):
            target_distance = vertex_distance + edge.length
            if distances[edge._target][0] > target_distance:
                distances[edge._target] = (target_distance, vertex._id)
    return distances


def single_source_longest_path_dag(graph, start):
    if not graph.is_directed():
        raise Exception('topological sort only works with directed acyclic graphs')
    if start < 0 or start >= graph.vertices_length():
        raise IndexError('out of range')
    distances = [(float('inf'), None)] * len(graph)
    distances[start] = (0, None)
    for vertex in topological_sort(graph):
        vertex_distance = distances[vertex._id][0]
        for edge in graph.get_edges(vertex._id):
            target_distance = vertex_distance - edge.length
            if distances[edge._target][0] > target_distance:
                distances[edge._target] = (target_distance, vertex._id)
    inf = float('inf')
    distances = [(-distance if distance != inf else inf, previous) for distance, previous in distances]
    return distances


def dijkstra(graph: Graph, start, end=None, /, ignore_negative_edges=False, ignore_negative_exceptions=False):
    if start < 0 or start >= graph.vertices_length() or end is not None and (end < 0 or end >= graph.vertices_length()):
        raise IndexError('out of range')
    distances = [(float('inf'), None)] * len(graph)
    distances[start] = (0, None)
    heap = Heap(mode=lambda x, y: x[0] < y[0])
    heap.offer((0, start))
    while not heap.empty():
        vertex_distance, vertex_id = heap.poll()
        current_distance = distances[vertex_id][0]
        if current_distance < vertex_distance:
            continue
        if vertex_id == end:
            break
        for edge in graph.get_edges(vertex_id):
            if edge.length < 0:
                if ignore_negative_edges:
                    continue
                if not ignore_negative_exceptions:
                    raise Exception('dijkstra only supports negative length in graphs without negative cycles or dags')
            target_distance = vertex_distance + edge.length
            if distances[edge._target][0] > target_distance:
                distances[edge._target] = (target_distance, vertex_id)
                heap.offer((target_distance, edge._target))
    return distances


def dijkstra_v2(graph: Graph, start):
    if start < 0 or start >= graph.vertices_length():
        raise IndexError('out of range')
    inf = float('inf')
    distances = [(float('inf'), None)] * len(graph)
    distances[start] = (0, None)
    heap = Heap(mode=lambda x, y: x[0] < y[0])
    heap.offer((0, start))
    while not heap.empty():
        vertex_distance, vertex_id = heap.poll()
        current_distance = distances[vertex_id][0]
        if current_distance < vertex_distance:
            continue
        for edge in graph.get_edges(vertex_id):
            target_distance = vertex_distance + edge.length
            is_smaller = distances[edge._target][0] > target_distance
            is_same_parent = distances[edge._target][1] == vertex_id
            if is_smaller:
                if is_same_parent:
                    target_distance = -inf
                distances[edge._target] = (target_distance, vertex_id)
                heap.offer((target_distance, edge._target))
    return distances


def bellman_ford(graph: Graph, start, check_negative_cycles=True):
    distances = [(float('inf'), None)] * len(graph)
    distances[start] = (0, None)
    for i in range(graph.vertices_length() - 1):
        for edge in graph.edges():
            target_cost = distances[edge._source][0] + edge.length
            if target_cost < distances[edge._target][0]:
                distances[edge._target] = (target_cost, edge._source)
    if check_negative_cycles:
        inf = float('inf')
        for i in range(graph.vertices_length() - 1):
            for edge in graph.edges():
                target_cost = distances[edge._source][0] + edge.length
                if target_cost < distances[edge._target][0]:
                    distances[edge._target] = (-inf, edge._source)
    return distances


def test():
    print('dags')
    for i in range(3):
        g = random_dag(ew_range=(-10, 15))
        print(g)
        print('sssp', single_source_shortest_path_dag(g, 0))
        print('sslp', single_source_longest_path_dag(g, 0))
        print('dkst', dijkstra(g, 0, ignore_negative_exceptions=True))

    print('randoms undirected')
    for i in range(3):
        g = random_undirected(10, ew_range=(1, 15))
        print(g)
        print('dijkstra', dijkstra(g, 0))
        print()

    print('randoms directed')
    for i in range(3):
        g = random_directed(10, ew_range=(1, 15))
        print(g)
        print('dijkstra', dijkstra(g, 0))
        print()

    print('negative completes')
    for i in range(3):
        g = complete(5, ew_range=(-10, 10))
        print(g)
        print('dijkstra', dijkstra(g, 0, ignore_negative_edges=True))
        print('bellman ford', bellman_ford(g, 0))
        print('dijkstra v2', dijkstra_v2(g, 0))
        print()


if __name__ == '__main__':
    test()
