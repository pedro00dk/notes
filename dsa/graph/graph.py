import itertools
import random

from ..linked.list import LinkedList
from ..linked.queue import Queue


class Graph:
    @classmethod
    def complete(cls, vertices=5):
        graph = Graph()
        for vertex in range(vertices):
            graph.make_vertex()
            for target in range(0, vertex):
                graph.make_edge(vertex, target)
        return graph

    @classmethod
    def random(cls, vertices=5, density=0.5):
        graph = Graph()
        for vertex in range(vertices):
            graph.make_vertex()
        edges = round(min(max(0, density), 1) * vertices * (vertices - 1) / 2)
        for source, target in random.sample([*itertools.combinations(range(vertices), 2)], edges):
            graph.make_edge(source, target)
        return graph

    @classmethod
    def random_dag(cls, ranks_range=(3, 5), vertices_range=(1, 5), probability=0.5):
        graph = Graph()
        ranks = random.randint(*ranks_range)
        previous_vertices = 0
        for rank in range(ranks):
            vertices = random.randint(*vertices_range)
            for vertice in range(previous_vertices, vertices + previous_vertices):
                graph.make_vertex()
            for previous in range(previous_vertices):
                for vertice in range(previous_vertices, vertices + previous_vertices):
                    if random.random() < probability:
                        graph.make_edge(previous, vertice, bidirectional=False)
                    pass
            previous_vertices += vertices
        return graph

    def __init__(self):
        self.vertices = []
        pass

    def __str__(self):
        data = '\n'.join(f'{v}: {[e for e, w in edges]}' for v, (edges, w) in enumerate(self.vertices))
        return f'Graph [\n{data}\n]'

    def __len__(self):
        return len(self.vertices)

    def _depth_search(self, vertex, visited, before=True, previous=None, depth=0):
        if visited[vertex]:
            return
        visited[vertex] = True
        if before:
            yield vertex, previous
        for target, weight in self.vertices[vertex][0]:
            yield from self._depth_search(target, visited, vertex, depth + 1)
        if not before:
            yield vertex, previous

    def _breadth_search(self, vertex, visited, before=True, previous=None, depth=0):
        queue = Queue()
        queue.offer((vertex, previous))
        while queue.size > 0:
            vertex, previous = queue.poll()
            if visited[vertex]:
                continue
            visited[vertex] = True
            yield vertex, previous
            for target, weight in self.vertices[vertex][0]:
                queue.offer((target, vertex))

    def traverse(self, vertex, mode='dfs', visited=None, before=True):
        if vertex < 0 or vertex >= len(self.vertices):
            raise IndexError('out of range')
        visited = visited if visited is not None else [False] * len(self.vertices)
        return self._depth_search(vertex, visited, before) if mode == 'dfs' else \
            self._breadth_search(vertex, visited, before)

    def make_vertex(self, weight=1):
        vertex = len(self.vertices)
        self.vertices.append(([], weight))
        return vertex

    def make_edge(self, source, target, weight=1, bidirectional=True):
        if source < 0 or source >= len(self.vertices) or target < 0 or target >= len(self.vertices):
            raise IndexError('out of range')
        self.vertices[source][0].append((target, weight))
        if bidirectional:
            self.vertices[target][0].append((source, weight))


def test():
    g = Graph.complete(5)
    print(g)
    for vertex, previous in g.traverse(0, 'dfs'):
        print(vertex, end=' ')
    print()
    for vertex, previous in g.traverse(0, 'bfs'):
        print(vertex, end=' ')
    print()
    print('Complete Graph:\n', Graph.complete())
    print('Random Graph:\n', Graph.random())
    print('Random Directed Acyclic Graph:\n', Graph.random_dag())


if __name__ == '__main__':
    test()
