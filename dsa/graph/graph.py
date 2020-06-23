import collections


class Vertex:
    """
    Vertex container implementation.
    The `_id` property must not be modified.
    The user can access and change vertex `weight` and `data`.
    Vertex edges are mantained in a separate data structure, so the users can not edit them.
    """

    def __init__(self, id: int, /, weight=1, data=None):
        """
        > parameters:
        - `id: int`: vertex identifier
        - `weight: (int | float)? = 1`: vertex weight
        - `data: any? = None`: vertex user data
        """
        self._id = id
        self.weight = weight
        self.data = data


class Edge:
    """
    Directed edge container implementation.
    `_source` and `_target` properties must not be modified.
    The user can access and change edge `length` and `data`.
    """

    def __init__(self, source: int, target: int, /, length=1, data=None):
        """
        > parameters:
        - `_source: int`: source vertex identifier
        - `_target: int`: target vertex identifier
        - `length: (int | float)? = 1`: edge length
        - `data: any? = None`: edge user data
        """
        self._source = source
        self._target = target
        self.length = length
        self.data = data


class Graph:
    """
    Graph implementation.
    This implementation uses adjacency lists (edges lists are default lists, not linked lists).
    Implementation details:
    - vertices and edges can only be added, deleting then is not possible
    - only vertices have identifiers
    """

    def __init__(self):
        self._vertices = []
        self._edges = []
        self._all_edges = 0
        self._directed_edges = 0
        self._cycle_edges = 0

    def __len__(self):
        return len(self._vertices)

    def __str__(self):
        lines = '\n'.join(
            f'{v._id} w={v.weight} => {", ".join(f"({e._target} l={e.length})" for e in es)}'
            for v, es in zip(self._vertices, self._edges))
        return f'Graph [\n{lines}\n]'

    def __iter__(self):
        return self.vertices()

    def _depth(self, v: int, visited: list, /, yield_before=True, yield_after=False, yield_back=False, *, parent=None, edge=None):
        """
        Return a generator for Depth First Search traversals.
        This implementation must not be used to implement other algorithms because of the performance impact of
        generators, allocated tuples and non-optminized implementation for reference only.

        > complexity:
        - time: `O(v + e)`
        - space: `O(v)`

        > parameters:
        - `v: int`: root vertex id
        - `visited: bool[]`: list of visited vertices
        - `yield_before: bool? = True`: yield vertices before yield all its children
        - `yield_after: bool? = False`: yield vertices after yield all its children
        - `yield_back: bool? = False`: yield edges that point to already visited vertices
        - `INTERNAL parent: int? = None`: parent vertex id
        - `INTERNAL edge: Edge? = None`: the edge from `parent` to the next vertex
        - `INTERNAL depth: int? = 0`: base depth

        > `return: Generator<(Vertex, Vertex, Edge, int, bool, bool)>`: generator of vertices, parents, edges, depth,
            if yielded before (`True`, otherwise `False`), and if is a back edge
        """
        vertex = self._vertices[v]
        if visited[v]:
            if yield_back and edge is not None:
                if yield_before:
                    yield vertex, parent, edge
                if yield_after:
                    yield vertex, parent, edge
            return
        if yield_before:
            yield vertex, parent, edge
        visited[v] = True
        for edge in self._edges[v]:
            yield from self._depth(
                edge._target, visited, yield_before, yield_after, yield_back, parent=vertex, edge=edge
            )
        if yield_after:
            yield vertex, parent, edge

    def _breadth(self, v: int, visited: list, /, yield_back=False):
        """
        Return a generator for Breadth First Search traversals.
        This implementation must not be used to implement other algorithms because of the performance impact of
        generators, allocated tuples and non-optminized implementation for reference only.

        > complexity:
        - time: `O(v + e)`
        - space: `O(v)`

        > parameters:
        - `v: int`: root vertex id
        - `visited: bool[]`: list of visited vertices
        - `yield_back: bool? = False`: yield edges that point to already visited vertices

        > `return: Generator<(Vertex, Vertex, Edge, int, bool, bool)>`: generator of vertices, parents, edges, depth,
            if yielded before (always `True` in this algorithm), and if is a back edge
        """
        queue = collections.deque()
        queue.append((v, None, None, 0))
        while len(queue):
            v, parent, edge, depth = queue.popleft()
            vertex = self._vertices[v]
            if visited[v]:
                if yield_back and edge is not None:
                    yield vertex, parent, edge, depth, True
                continue
            yield vertex, parent, edge, depth, True, False
            visited[v] = True
            for edge in self._edges[v]:
                queue.append((edge._target, vertex, edge, depth + 1))

    def traverse(self, v: int, mode='depth', /, visited: list = None, yield_before=True, yield_after=False, yield_back=False):
        """
        Return a generator for graph traversals.
        This implementation must not be used to implement other algorithms because of the performance impact of
        generators, allocated tuples and non-optminized implementation for reference only.

        > complexity:
        - time: `O(v + e)`
        - space: `O(v)`

        > parameters:
        - `v: int`: root vertex id
        - `mode: 'depth' | 'breadth'`: traversal mode
        - `visited: bool[]? = [False] * self.vertices_count()`: list of visited vertices
        - `yield_before: bool? = True`: yield vertices before yield all its children (only for `mode == 'depth'`)
        - `yield_after: bool? = False`: yield vertices after yield all its children (only for `mode == 'depth'`)
        - `yield_back: bool? = False`: yield edges that point to already visited vertices

        > `return: Generator<(Vertex, Vertex, Edge, int, bool, bool)>`: generator of vertices, parents, edges, depth,
            if yielded before (`True`, otherwise `False`), and if is a back edge
        """
        visited = visited if visited is not None else [False] * self.vertices_count()
        return self._depth(v, visited, yield_before, yield_after, yield_back) if mode == 'depth' else \
            self._breadth(v, visited, yield_back)

    def vertices(self):
        """
        Return a generator to traverse through graph vertices.

        > complexity:
        - time: `O(v)`
        - space: `O(1)`

        > `return: Generator<(int, float, any)>`: generator of vertices ids, weights and data
        """
        return iter(self._vertices)

    def edges(self, /, v: int = None):
        """
        Return a generator to traverse through graph edges.

        > complexity:
        - time: `O(e)`
        - space: `O(1)`

        > parameters:
        - `v: int? = None`: id of the vertex to traverse, if `None`, traverse through edges os all vertices

        > `return: Generator<(int, float, any)>`: generator of vertices ids which contains the edge, lengths and data
        """
        return (edge for vertex_edges in self._edges for edge in vertex_edges) if v is None else iter(self._edges[v])

    def vertices_count(self):
        """
        > `return: int`: number of vertices
        """
        return len(self._vertices)

    def edges_count(self, v: int = None):
        """
        > parameters:
        - `v: int? = None`: id of the vertex to get edge count, if `None`, get all edges count

        > `return: int`: number of edges (undirected edges count as 2 edges)
        """
        return self._all_edges if v is None else len(self._edges[v])

    def unique_edges_count(self):
        """
        > `return: int`: number of edges (undirected edges count as 1 edge)
        """
        return (self._all_Edges - self._directed_edges) / 2 + self._directed_edges

    def is_undirected(self):
        """
        > `return: bool`: if all edges are undirected
        """
        return self._directed_edges == 0

    def is_directed(self):
        """
        > `return: bool`: if all edges are directed
        """
        return self._directed_edges == self._all_edges

    def has_directed_edges(self):
        """
        > `return: bool`: if there is any directed edge
        """
        return self._directed_edges > 0

    def has_edge_cycles(self):
        """
        > `return: bool`: if there is any cycle edge
        """
        return self._cycle_edges > 0

    def make_vertex(self, /, weight=1, data=None):
        """
        Create a new vertex.

        > parameters:
        - `weight: (int | float)? = 1`: vertex weight
        - `data: any? = None`: vertex user data

        > `return: Vertex`: vertex
        """
        vertex = Vertex(self.vertices_count(), weight, data)
        self._vertices.append(vertex)
        self._edges.append([])
        return vertex

    def make_edge(self, source: int, target: int, /, length=1, data=None, directed=False):
        """
        Create a new edge.
        Undirected edges are represented as two directed edges with the same data.
        Editing one of the undirected edges properties are not propagated to the other edge.

        > parameters:
        - `source: int`: source vertex identifier
        - `target: int`: target vertex identifier
        - `length: (int | float)? = 1`: edge length
        - `data: any? = None`: edge user data
        - `directed: bool? = None`: if edge is directed

        > `return: Edge | (Edge, Edge)`: the created edge or both edges if undirected
        """
        if source < 0 or source >= self.vertices_count() or target < 0 or target >= self.vertices_count():
            raise IndexError(f'source ({source}) or target ({target}) vertex out of range [0, {self.vertices_count()})')
        edge = Edge(source, target, length, data)
        self._edges[source].append(edge)
        self._all_edges += 1 + int(not directed)
        self._directed_edges += int(directed)
        is_cycle = source == target
        self._cycle_edges += int(is_cycle) + int(is_cycle and not directed)
        if not directed:
            back_edge = Edge(target, source, length, data)
            self._edges[target].append(back_edge)
        return edge if directed else (edge, back_edge)

    def get_vertex(self, v: int):
        """
        Return the vertex object associated with `v`.

        > parameters:
        - `v: int`: vertex id

        > `return: Vertex`: vertex
        """
        return self._vertices[v]

    def get_edges(self, v: int):
        """
        Return the edge tuple list of the vertex associated with `v`.

        > parameters:
        - `v: int`: vertex id

        > `return: Edge()`: edge tuple list
        """
        return (*self._edges[v],)

    def copy(self):
        """
        Return a copy of the graph.

        > complexity:
        - time: `O(v + e)`
        - space: `O(v + e)`

        > `return: Graph`: copy of the graph
        """
        graph = Graph()
        for vertex in self.vertices():
            graph.make_vertex(vertex.weight, vertex.data)
        for edge in self.edges():
            graph.make_edge(edge._source, edge._target, edge.length, edge.data, True)
        return graph

    def transposed(self):
        """
        Return a copy of the graph with edges transposed.

        > complexity:
        - time: `O(v + e)`
        - space: `O(v + e)`

        > `return: Graph`: transposed copy of the graph
        """
        transposed_graph = Graph()
        for vertex in self.vertices():
            transposed_graph.make_vertex(vertex.weight, vertex.data)
        for edge in self.edges():
            transposed_graph.make_edge(edge._target, edge._source, edge.length, edge.data, True)
        return transposed_graph

    def adjacency_matrix(self, /, absent_edge_length=float('inf')):
        """
        Return the adjacency matrix of the graph containing edge lengths.

        > complexity:
        - time: `O(v**2)`
        - space: `O(v**2)`

        > parameters:
        - `absent_edge_length: (int | float)? = float('inf')`: length to use in non existent edges

        > `return: (int | float)[][]`: graph adjacency matrix
        """
        matrix = [[absent_edge_length] * self.vertices_count() for i in range(self.vertices_count())]
        for edge in self.edges():
            matrix[edge._source][edge._target] = edge.length
        for v in range(self.vertices_count()):
            matrix[v][v] = matrix[v][v] if matrix[v][v] != absent_edge_length else 0
        return matrix
