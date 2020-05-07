import itertools
import random

from ..linked.list import LinkedList
from ..linked.queue import Queue


class Graph:
    def __init__(self):
        self.vertices = []
        pass

    def __str__(self):
        data = '\n'.join(f'{v}: {[e for e, w in edges]}' for v, (edges, w) in enumerate(self.vertices))
        return f'Graph [\n{data}\n]'

    def __len__(self):
        return len(self.vertices)

    @classmethod
    def complete(cls, n):
        graph = Graph()
        for vertex in range(n):
            graph.make_vertex()
            for target in range(0, vertex):
                graph.make_edge(vertex, target)
        return graph

    @classmethod
    def random(cls, n, d=0.5):
        graph = Graph()
        for vertex in range(n):
            graph.make_vertex()
        edges = round(min(max(0, d), 1) * n * (n - 1) / 2)
        for source, target in random.sample([*itertools.combinations(range(n), 2)], edges):
            graph.make_edge(source, target)
        return graph

    def _depth_search(self, vertex, visited, depth=0):
        if visited[vertex]:
            return
        visited[vertex] = True
        yield vertex, self.vertices[vertex][1]
        for target, weight in self.vertices[vertex][0]:
            yield from self._depth_search(target, visited, depth + 1)

    def _breadth_search(self, vertex, visited, depth=0):
        queue = Queue()
        queue.offer(vertex)
        while queue.size > 0:
            vertex = queue.poll()
            if visited[vertex]:
                continue
            visited[vertex] = True
            yield vertex, self.vertices[vertex][1]
            for target, weight in self.vertices[vertex][0]:
                queue.offer(target)

    def make_vertex(self, weight=1):
        vertex = len(self.vertices)
        self.vertices.append((LinkedList(), weight))
        return vertex

    def make_edge(self, source, target, weight=1, bidirectional=True):
        if source < 0 or source >= len(self.vertices) or target < 0 or target >= len(self.vertices):
            raise IndexError('out of range')
        self.vertices[source][0].push((target, weight))
        if bidirectional:
            self.vertices[target][0].push((source, weight))

    def traverse(self, vertex, mode='dfs', visited=None):
        if vertex < 0 or vertex >= len(self.vertices):
            raise IndexError('out of range')
        visited = visited if visited is not None else [False] * len(self.vertices)
        return self._depth_search(vertex, visited) if mode == 'dfs' else self._breadth_search(vertex, visited)


def test():
    g = Graph.complete(5)
    print(g)
    for vertex, weight in g.traverse(0, 'dfs'):
        print(vertex, end=' ')
    print()
    for vertex, weight in g.traverse(0, 'bfs'):
        print(vertex, end=' ')
    print()


if __name__ == '__main__':
    test()
