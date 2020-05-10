import itertools
import random

from ..linked.list import LinkedList
from ..linked.queue import Queue


class Graph:
    def __init__(self):
        self._vertices = []
        self._edges = []
        self._edges_length = 0
        self._directed_edges = 0
        self._cycle_edges = 0

    def __len__(self):
        return self.vertices_length()

    def __str__(self):
        lines = "\n".join(
            f'{v._id} w={v.weight} => {", ".join(f"({e._target} l={e.length})" for e in es)}'
            for v, es in ((self.get_vertex(id), self.get_edges(id)) for id in range(self.vertices_length()))
        )
        return f'Graph [\n{lines}\n]'
        pass

    def __iter__(self):
        return self.vertices()

    def _depth(self, id, /, visited, yield_all_edges = False, yield_after = False, *, previous = None, edge = None, depth = 0):
        vertex = self._vertices[id]
        if visited[id]:
            if yield_all_edges and edge is not None:
                yield vertex, previous, edge, depth
            return
        visited[id] = True
        if not yield_after:
            yield vertex, previous, edge, depth
        for edge in self._edges[id]:
            yield from self._depth(
                edge._target, visited, yield_after, yield_all_edges, previous=vertex, edge=edge, depth=depth + 1
            )
        if yield_after:
            yield vertex, previous, edge, depth

    def _breadth(self, id, / , visited, yield_all_edges=False):
        queue = Queue()
        queue.offer((id, None, None, 0))
        while not queue.empty():
            id, previous, edge, depth = queue.poll()
            vertex = self._vertices[id]
            if visited[id]:
                if yield_all_edges and edge is not None:
                    yield vertex, previous, edge, depth
                continue
            visited[id] = True
            yield vertex, previous, edge, depth
            for edge in self._edges[id]:
                queue.offer((edge._target, vertex, edge, depth + 1))

    def make_vertex(self, / , weight=1, data=None):
        vertex = Vertex(self.vertices_length(), weight, data)
        self._vertices.append(vertex)
        self._edges.append([])
        return vertex

    def make_edge(self, source, target, /, length=1, data=None, *, directed=False):
        if source < 0 or source >= self.vertices_length() or target < 0 or target >= self.vertices_length():
            raise IndexError('out of range')
        self._edges[source].append(Edge(source, target, length, data))
        self._edges_length += 1 + int(not directed)
        self._directed_edges += int(directed)
        is_cycle = source == target
        self._cycle_edges += int(is_cycle) + int(is_cycle and not directed)
        if not directed:
            self._edges[target].append(Edge(target, source, length, data))

    def get_vertex(self, id):
        return self._vertices[id]

    def get_edges(self, id):
        return (*self._edges[id],)

    def vertices_length(self):
        return len(self._vertices)

    def edges_length(self):
        return self._edges_length

    def unique_edges_length(self):
        return (self._edges_length - self._directed_edges) / 2 + self._directed_edges

    def is_undirected(self):
        return self._directed_edges == 0

    def is_directed(self):
        return self._directed_edges == self._edges_length

    def has_directed_edges(self):
        return self._directed_edges > 0

    def has_edge_cycles(self):
        return self._cycle_edges > 0

    def vertices(self):
        return iter(self._vertices)

    def edges(self, id=None):
        if id is not None:
            return iter(self._edges[id])
        return (edge for edges in self._edges for edge in edges)

    def traverse(self, id, mode='depth', / , visited=None, yield_all_edges=False, yield_after=False):
        visited = visited if visited is not None else [False] * self.vertices_length()
        return self._depth(id, visited, yield_all_edges, yield_after) if mode == 'depth' else \
            self._breadth(id, visited, yield_all_edges)


class Vertex:
    def __init__(self, id, / , weight=1, data=None):
        self._id = id
        self.weight = weight
        self.data = data


class Edge:
    def __init__(self, source, target, / , length=1, data=None):
        self._source = source
        self._target = target
        self.length = length
        self.data = data
