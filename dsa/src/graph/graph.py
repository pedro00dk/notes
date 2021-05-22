from __future__ import annotations

import collections
import dataclasses
from typing import Callable, Generator, Generic, Literal, Optional, TypeVar

V = TypeVar("V")
E = TypeVar("E")


@dataclasses.dataclass
class Vertex(Generic[V]):
    """
    Vertex container implementation.
    The `id` property must not be modified.
    The user can access and change vertex `weight` and `data`.
    Edges are mantained in a separate data structure.
    """

    id: int
    weight: float
    data: Optional[V] = None


@dataclasses.dataclass
class Edge(Generic[E]):
    """
    Directed edge container implementation.
    `source`, `target` and `opposite` properties must not be modified.
    `opposite` is a reference to the back edge if the edge is undirected.
    The user can access and change edge `length` and `data`.
    """

    source: int
    target: int
    length: float
    data: Optional[E] = None
    opposite: Optional[Edge[E]] = None


class Graph(Generic[V, E]):
    """
    Graph implementation based on adjacency lists (edges lists are default lists, not linked lists).

    > implementation details
    - vertices and edges can only be added, deleting them is not possible
    - only vertices have identifiers

    > complexity
    - space: `O(v + e)`
    - `v`: number of vertices in the graph
    - `e`: number of edges in the graph
    """

    def __init__(self):
        self._vertices: list[Vertex[V]] = []
        self._edges: list[list[Edge[E]]] = []
        self._all_edges: int = 0
        self._directed_edges: int = 0
        self._cycle_edges: int = 0

    def __len__(self) -> int:
        return len(self._vertices)

    def __str__(self) -> str:
        lines = "\n".join(
            f'{v.id} w={v.weight} => {", ".join(f"({e.target} l={e.length})" for e in es)}'
            for v, es in zip(self._vertices, self._edges)
        )
        return f"Graph [\n{lines}\n]"

    def __iter__(self) -> Generator[Vertex[V], None, None]:
        """
        Return a generator to traverse through graph vertices.

        > complexity
        - time: `O(v)`
        - space: `O(1)`
        - `v`: number of vertices in the graph

        - `return`: generator of vertices
        """
        return self.vertices()

    def _depth(
        self,
        v: int,
        visited: list[bool],
        yield_back: bool = False,
        parent: Optional[Vertex[V]] = None,
        edge: Optional[Edge[E]] = None,
        depth: int = 0,
    ) -> Generator[tuple[Vertex[V], Optional[Vertex[V]], Optional[Edge[E]], int], None, None]:
        """
        Return a generator for Depth First Search traversals.
        This implementation must not be used to implement other algorithms because of the performance impact of
        generators, allocated tuples and non-optminized implementation for specific algorithms.

        > complexity
        - time: `O(v + e)`
        - space: `O(v)`
        - `v`: number of vertices in the graph
        - `e`: number of edges in the graph

        > parameters
        - `v`: root vertex id (must not be visited, otherwise it will be visited again)
        - `visited`: list of visited vertices
        - `yield_back`: yield edges that point to already visited vertices
        - `parent`: parent vertex id
        - `edge`: the edge from `parent` to the next vertex
        - `depth`: base depth
        - `return`: iterator of vertices, parents, edges and depth
        """
        vertex = self._vertices[v]
        yield vertex, parent, edge, depth
        visited[v] = True
        for edge in self._edges[v]:
            if not visited[edge.target]:
                yield from self._depth(edge.target, visited, yield_back, parent=vertex, edge=edge, depth=depth + 1)
            elif yield_back:
                yield self._vertices[edge.target], vertex, edge, depth + 1

    def _breadth(
        self,
        v: int,
        visited: list[bool],
        yield_back: bool = False,
    ) -> Generator[tuple[Vertex[V], Optional[Vertex[V]], Optional[Edge[E]], int], None, None]:
        """
        Return a generator for Breadth First Search traversals.
        This implementation must not be used to implement other algorithms because of the performance impact of
        generators, allocated tuples and non-optminized implementation for the specific algorithm.

        > complexity
        - time: `O(v + e)`
        - space: `O(v)`
        - `v`: number of vertices in the graph
        - `e`: number of edges in the graph

        > parameters
        - `v`: root vertex id (must not be visited, otherwise it will be visited again)
        - `visited`: list of visited vertices
        - `yield_back`: yield edges that point to already visited vertices
        - `return`: iterator of vertices, parents, edges and depth
        """
        queue = collections.deque[tuple[int, Optional[Vertex[V]], Optional[Edge[E]], int]]()
        queue.append((v, None, None, 0))
        visited[v] = True
        while len(queue):
            v, parent, edge, depth = queue.popleft()
            vertex = self._vertices[v]
            yield vertex, parent, edge, depth
            for edge in self._edges[v]:
                if not visited[edge.target]:
                    queue.append((edge.target, vertex, edge, depth + 1))
                    visited[edge.target] = True
                elif yield_back:
                    yield self._vertices[edge.target], vertex, edge, depth + 1

    def traverse(
        self,
        v: int,
        mode: Literal["depth", "breadth"] = "depth",
        visited: Optional[list[bool]] = None,
        yield_back: bool = False,
    ) -> Generator[tuple[Vertex[V], Optional[Vertex[V]], Optional[Edge[E]], int], None, None]:
        """
        Return a generator for graph traversals.
        This implementation must not be used to implement other algorithms because of the performance impact of
        generators, allocated tuples and non-optminized implementation for the specific algorithm.

        > complexity
        - time: `O(v + e)`
        - space: `O(v)`
        - `v`: number of vertices in the graph
        - `e`: number of edges in the graph

        > parameters
        - `v`: root vertex id (must not be visited, otherwise it will be visited again)
        - `mode`: traversal mode
        - `visited`: list of visited vertices, which are skipped
        - `yield_back`: yield edges that point to already visited vertices
        - `return`: iterator of vertices, parents, edges and depth
        """
        visited = visited if visited is not None else [False] * self.vertices_count()
        return self._depth(v, visited, yield_back) if mode == "depth" else self._breadth(v, visited, yield_back)

    def vertices(self) -> Generator[Vertex[V], None, None]:
        """
        Return a generator of graph vertices.

        > complexity
        - time: `O(v)`
        - space: `O(1)`
        - `v`: number of vertices in the graph

        - `return`: generator of vertices
        """
        return (vertex for vertex in self._vertices)

    def edges(self, v: Optional[int] = None) -> Generator[Edge[E], None, None]:
        """
        Return a generator of graph edges.

        > complexity
        - time: `O(v + e)`
        - space: `O(1)`
        - `v`: number of vertices in the graph
        - `e`: number of edges in the graph

        > parameters
        - `v`: id of the vertex to collect edges, if `None`, collect through edges os all vertices
        - `return`: generator of edges
        """
        return (
            (edge for vertex_edges in self._edges for edge in vertex_edges)
            if v is None
            else (edge for edge in self._edges[v])
        )

    def vertices_count(self) -> int:
        """
        - `return`: number of vertices
        """
        return len(self._vertices)

    def edges_count(self, v: Optional[int] = None) -> int:
        """
        > parameters
        - `v`: id of the vertex to get edge count, if `None`, get all edges count
        - `return`: number of edges (undirected edges count as 2 edges)
        """
        return self._all_edges if v is None else len(self._edges[v])

    def unique_edges_count(self) -> int:
        """
        - `return`: number of edges (undirected edges count as 1 edge)
        """
        return (self._all_edges - self._directed_edges) // 2 + self._directed_edges

    def is_undirected(self) -> bool:
        """
        - `return`: if all edges are undirected
        """
        return self._directed_edges == 0

    def is_directed(self) -> bool:
        """
        - `return`: if all edges are directed
        """
        return self._directed_edges == self._all_edges

    def has_directed_edges(self) -> bool:
        """
        - `return`: if there is any directed edge
        """
        return self._directed_edges > 0

    def has_edge_cycles(self) -> bool:
        """
        - `return`: if there is any cycle edge
        """
        return self._cycle_edges > 0

    def make_vertex(self, weight: float = 1, data: Optional[V] = None) -> Vertex[V]:
        """
        Create a new vertex.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `weight`: vertex weight
        - `data`: vertex user data
        - `return`: vertex
        """
        vertex = Vertex(self.vertices_count(), weight, data)
        self._vertices.append(vertex)
        self._edges.append([])
        return vertex

    def make_edge(
        self,
        source: int,
        target: int,
        length: float = 1,
        data: Optional[E] = None,
        directed: bool = False,
    ) -> tuple[Edge[E], Optional[Edge[E]]]:
        """
        Create a new edge.
        Undirected edges are represented as two directed edges with the same data.
        Editing one of the undirected edges properties are not propagated to the other edge.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `source`: source vertex identifier
        - `target`: target vertex identifier
        - `length`: edge length
        - `data`: edge user data
        - `directed`: if edge is directed
        - `return`: the created edge or both edges if undirected
        """
        if source < 0 or source >= self.vertices_count() or target < 0 or target >= self.vertices_count():
            raise IndexError(f"source ({source}) or target ({target}) vertex out of range [0, {self.vertices_count()})")
        edge = Edge(source, target, length, data)
        self._edges[source].append(edge)
        self._all_edges += 1 + int(not directed)
        self._directed_edges += int(directed)
        is_cycle = source == target
        self._cycle_edges += int(is_cycle) + int(is_cycle and not directed)
        back_edge: Optional[Edge[E]] = None
        if not directed:
            back_edge = Edge(target, source, length, data)
            self._edges[target].append(back_edge)
            edge.opposite = back_edge
            back_edge.opposite = edge
        return edge, back_edge

    def get_vertex(self, v: int) -> Vertex[V]:
        """
        Return the vertex object associated with `v`.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `v`: vertex id
        - `return`: vertex
        """
        return self._vertices[v]

    def get_vertices(self) -> tuple[Vertex[V], ...]:
        """
        Return all graph vertices.

        > complexity
        - time: `O(v)`
        - space: `O(v)`

        > parameters
        - `return`: vertices
        """
        return (*self.vertices(),)

    def get_edges(self, v: Optional[int] = None) -> tuple[Edge[E], ...]:
        """
        Return the edges of the vertex associated with `v` or all edges if `v is None`.

        > complexity
        - time: `O(v + e)`
        - space: `O(e)`
        - `v`: number of vertices in the graph
        - `e`: number of edges in the graph

        > parameters
        - `v`: vertex id
        - `v`: vertex id, if `None` get all edges
        - `return`: edges
        """
        return (*self.edges(v),)

    def copy(self) -> Graph[V, E]:
        """
        Return a copy of the graph.
        Edges may be in a different order.

        > complexity
        - time: `O(v + e)`
        - space: `O(v + e)`
        - `v`: number of vertices in the graph
        - `e`: number of edges in the graph

        - `return`: copy of the graph
        """
        graph = Graph[V, E]()
        visited_edges = set[int]()
        for vertex in self.vertices():
            graph.make_vertex(vertex.weight, vertex.data)
        for edge in self.edges():
            edge_id = id(edge)
            if edge_id in visited_edges:
                continue
            graph.make_edge(edge.source, edge.target, edge.length, edge.data, edge.opposite is None)
            visited_edges.add(edge_id)
            visited_edges.add(id(edge.opposite))
        return graph

    def transposed(self) -> Graph[V, E]:
        """
        Return a copy of the graph with edges transposed.
        Edges may be in a different order.

        > complexity
        - time: `O(v + e)`
        - space: `O(v + e)`
        - `v`: number of vertices in the graph
        - `e`: number of edges in the graph

        - `return`: transposed copy of the graph
        """
        transposed_graph = Graph[V, E]()
        visited_edges = set[int]()
        for vertex in self.vertices():
            transposed_graph.make_vertex(vertex.weight, vertex.data)
        for edge in self.edges():
            edge_id = id(edge)
            if edge_id in visited_edges:
                continue
            transposed_graph.make_edge(edge.target, edge.source, edge.length, edge.data, edge.opposite is None)
            visited_edges.add(edge_id)
            visited_edges.add(id(edge.opposite))
        return transposed_graph

    def adjacency_matrix(
        self,
        absent_edge_length: float = float("inf"),
        tiebreak: Callable[[float, float], float] = min,
    ) -> list[list[float]]:
        """
        Return the adjacency matrix of the graph containing edge lengths.

        > complexity
        - time: `O(v**2)`
        - space: `O(v**2)`
        - `v`: number of vertices in the graph

        > parameters
        - `absent_edge_length`: length to use for absent edges
        - `tiebreak`: function used to choose a length if there is more than one edge with the same source and target
        - `return`: graph adjacency matrix
        """
        matrix = [[absent_edge_length] * self.vertices_count() for _ in range(self.vertices_count())]
        for edge in self.edges():
            matrix[edge.source][edge.target] = (
                edge.length
                if matrix[edge.source][edge.target] == absent_edge_length
                else tiebreak(edge.length, matrix[edge.source][edge.target])
            )
        for v in range(self.vertices_count()):
            matrix[v][v] = matrix[v][v] if matrix[v][v] != absent_edge_length else 0
        return matrix
