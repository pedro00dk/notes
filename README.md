# Notes - Data Structures and Algorithms

Collection of data structures and algorithms implemented in Python.

The minimum python version required is 3.9.
Scripts of this project must be run as a module:

```shell
cd <project-root>
$ python -m src.<module>.<file> # without .py

$ # examples:
$ python -m src.sorting.quicksort
$ python -m src.tree.avl
$ python -m src.graph.path.ssp
```

#### Notes

-   The `n` value in most asymptotic complexity descriptions refer to the main input size, which may be a list or string size, the absolute value of a numeric parameter, the size of a data structure, etc. Other complexity variables are usually described in the comments or in the code.

---

The time complexity in **big-O** notation is shown beside algorithms names.
Space complexity is available in algorithms files.

---

## Sorting Algorithms

-   [bubblesort](./src/sorting/bubblesort.py) **- O(n<sup>2</sup>)**
-   [insertionsort](./src/sorting/insertionsort.py) **- O(n<sup>2</sup>)**
-   [selectionsort](./src/sorting/selectionsort.py) **- O(n<sup>2</sup>)**
-   [heapsort](./src/sorting/heapsort.py) **- O(n\*log(n))**
-   [mergesort](./src/sorting/mergesort.py) **- O(n\*log(n))**
-   [quicksort](./src/sorting/quicksort.py)
    -   quicksort hoare's partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   quicksort lomuto's partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   quicksort dual pivot partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
-   [treesort](./src/sorting/treesort.py) (_see data structures trees section_) **- O(n\*`Tree.put` + `Tree.__iter__`))**
    -   treesort binary search tree **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   treesort avl **- O(n\*log(n))**
    -   treesort red-black tree **- O(n\*log(n))**
    -   treesort van emde boas **- O(n\*log(log(u)))**
-   [shellsort](./src/sorting/shellsort.py)
    -   shellsort Shell1959 **- O(n<sup>2</sup>)**
    -   shellsort FrankLazarus1960 **- O(n<sup>3/2</sup>)**
    -   shellsort Hibbard1963 **- O(n<sup>3/2</sup>)**
    -   shellsort PapernovStasevich1965 **- O(n<sup>3/2</sup>)**
    -   shellsort Knuth1973 **- O(n<sup>3/2</sup>)**
    -   shellsort Sedgewick1982 **- O(n<sup>4/3</sup>)**
    -   shellsort Tokuda1992 **- unknown**
    -   shellsort Ciura2001 **- unknown**
-   [countingsort](./src/sorting/countingsort.py) **- O(n + k)**
-   [bucketsort](./src/sorting/bucketsort.py) **- best: O(n), average: O(n + (n<sup>2</sup>/k) + k), worst O(n<sup>2</sup>)**
-   [radixsort](./src/sorting/radixsort.py)
    -   radixsort least-significant-digit **- O(n\*w)**
    -   radixsort most-significant-digit **- O(n\*w)**
-   [stoogesort](./src/sorting/stoogesort.py) **- O(n<sup>2.7</sup>)**
-   [slowsort](./src/sorting/slowsort.py) **- O(T(n)), where T(n) = T(n-1) + T(n/2)\*2 + 1**
-   [bogosort](./src/sorting/bogosort.py)
    -   bogosort random **- unbounded**
    -   bogosort deterministic **- O((n + 1)!)**

## Data Structures

-   [`Linked[T]` abstract](./src/linked/abc.py)
    -   `__str__` **- O(`Linked.__iter__`)**
    -   `__len__` **- abstract**
    -   `__iter__` **- abstract**
    -   `__contains__` **- O(`Linked.__iter__`)**
    -   `index` **- O(`Linked.__iter__`)**
    -   [`LinkedList[T]` extends `Linked[T]`](./src/linked/list.py) **- space: O(n)**
        -   `Linked.__len__` **- O(1)**
        -   `Linked.__iter__` **- O(n)**
        -   `push` **- O(n)**
        -   `pop` (index deletion) **- O(n)**
        -   `remove` (value deletion) **- O(n)**
        -   `get` (same as `Linked.index`, but faster) **- O(n)**
        -   `reverse` **- O(n)**
    -   [`Queue[T]` extends `Linked[T]`](./src/linked/queue.py) **- space: O(n)**
        -   `Linked.__len__` **- O(1)**
        -   `Linked.__iter__` **- O(n)**
        -   `offer` **- O(1)**
        -   `poll` **- O(1)**
        -   `peek` **- O(1)**
    -   [`Stack[T]` extends `Linked[T]`](./src/linked/stack.py) **- space: O(n)**
        -   `Linked.__len__` **- O(1)**
        -   `Linked.__iter__` **- O(n)**
        -   `push` **- O(1)**
        -   `pop` **- O(1)**
        -   `peek` **- O(1)**
-   [`Priority[T]` abstract](./src/priority/abc.py)
    -   `__str__` **- O(`Priority.__iter__`)**
    -   `__len__` **- abstract**
    -   `__iter__` **- abstract**
    -   `__contains__` **- O(`Priority.__iter__`)**
    -   `offer` **- abstract**
    -   `poll` **- abstract**
    -   `peek` **- abstract**
    -   [`Heap[T]` extends `Priority[T]`](./src/priority/heap.py) **- space: O(n)**
        -   utility
            -   `sift_up` **- O(log(n))**
            -   `sift_down` **- O(log(n))**
            -   `heapify_top_down` (`__init__`) **- O(n\*log(n))**
            -   `heapify_bottom_up` (`__init__`) **- O(n)**
        -   `Priority.__len__` **- O(1)**
        -   `Priority.__iter__` **- O(n\*log(n))**
        -   `Priority.offer` **- O(log(n))**
        -   `Priority.poll` **- O(log(n))**
        -   `Priority.peek` **- O(1)**
    -   [`KHeap[T]` extends `Priority[T]`](./src/priority/kheap.py) **- space: O(n)**
        -   utility
            -   `sift_up` **- O(k\*log<sub>k</sub>(n))**
            -   `sift_down` **- O(k\*log<sub>k</sub>(n))**
            -   `heapify_top_down` (`__init__`) **- O(n\*k\*log<sub>k</sub>(n))**
            -   `heapify_bottom_up` (`__init__`) **- O(n\*k)**
        -   `__str__` (override `Priority.__str__`) **- O(`Priority.__iter__`)**
        -   `Priority.__len__` **- O(1)**
        -   `Priority.__iter__` **- O(n\*k\*log<sub>k</sub>(n))**
        -   `Priority.offer` **- O(k\*log<sub>k</sub>(n))**
        -   `Priority.poll` **- O(k\*log<sub>k</sub>(n))**
        -   `Priority.peek` **- O(1)**
    -   [benchmark](./src/priority/benchmark.py) _- includes trees, see data structures trees section_
-   [`Map[K, V]` abstract](./src/map/abc.py)
    -   Implemented probers
        -   Linear Probing
        -   Quadratic Prime Probing
        -   Quadratic Triangular Probing
    -   `__str__` **- O(`Map.__iter__`)**
    -   `__len__` **- abstract**
    -   `__iter__` **- abstract**
    -   `__contains__` **- O(`Map.get`)**
    -   `keys` **- O(`Map.__iter__`)**
    -   `values` **- O(`Map.__iter__`)**
    -   `put` **- abstract**
    -   `take` **- abstract**
    -   `get` **- abstract**
    -   `contains_value` **- O(`Map.__iter__`)**
    -   [`OpenAddressingHashtable[K, V]` extends `Map[K, V]`](./src/map/oa_hashtable.py) **- space: O(n)**
        -   `Map.__len__` **- O(1)**
        -   `Map.__iter__` **- O(n)**
        -   `Map.put` **- O(1) amortized**
        -   `Map.take` **- O(1) amortized**
        -   `Map.get` **- O(1) amortized**
    -   [`SequenceChainingHashtable[K, V]` extends `Map[K, V]`](./src/map/sc_hashtable.py) **- space: O(n)**
        -   `Map.__len__` **- O(1)**
        -   `Map.__iter__` **- O(n)**
        -   `Map.put` **- O(1) amortized**
        -   `Map.take` **- O(1) amortized**
        -   `Map.get` **- O(1) amortized**
    -   [benchmark](./src/map/benchmark.py) _- includes trees, see data structures trees section_
-   [`Tree[K = Comparable, V]` abstract extends `Map[K, V]` `Heap[K]`](./src/tree/abc.py)
    -   `minimum` **- abstract**
    -   `maximum` **- abstract**
    -   `predecessor` **- abstract**
    -   `successor` **- abstract**
    -   `Heap.offer` **- O(`Map.put`)**
    -   `Heap.poll` **- O(`Tree.minimum` + `Map.take`)**
    -   `Heap.peek` **- O(`Tree.minimum`)**
    -   [Binary Search Tree - `BST[K = Comparable, V]` extends `Tree[K, V]`](./src/tree/bst.py) **- space: O(n)**
        -   `__str__` (override `Map.__str__` and `Priority.__str__`) - **O(traverse)**
        -   `Map.__len__ , Priority.__len__` **- O(1)**
        -   `Map.__iter__ , Priority.__iter__` **- O(traverse)**
        -   `traverse` (pre, in, post, breadth) - **- O(n)**
        -   `Map.put` **- average: O(log(n)), worst: O(n)**
        -   `Map.take` **- average: O(log(n)), worst: O(n)**
        -   `Map.get` **- average: O(log(n)), worst: O(n)**
        -   `Tree.minimum` **- average: O(log(n)), worst: O(n)**
        -   `Tree.maximum` **- average: O(log(n)), worst: O(n)**
        -   `Tree.predecessor` **- average: O(log(n)), worst: O(n)**
        -   `Tree.successor` **- average: O(log(n)), worst: O(n)**
    -   [Adelson Velsky and Landis - `AVL[K = Comparable, V]` extends `BST[K, V]`](./src/tree/avl.py) **- space: O(n)**
        -   `put` (override `Map.put` in `BST`) **- O(log(n))**
        -   `take` (override `Map.take` in `BST`) **- O(log(n))**
        -   **all functions worst case drop to O(log(n))**
    -   [Red-Black Tree - `RBT[K = Comparable, V]` extends `BST[K, V]`](./src/tree/rbt.py) **- space: O(n)**
        -   `put` (override `Map.put` in `BST`) **- O(log(n))**
        -   `take` (override `Map.take` in `BST`) **- O(log(n))**
        -   **all functions worst case drop to O(log(n))**
    -   [van Emde Boas - `VEB[V]` extends `Tree[int, V]`](./src/tree/rbt.py) **- space: O(n\*log(log(u)))**
        -   `__str__` (override `Map.__str__` and `Priority.__str__`) - **O(traverse)**
        -   `Map.__len__ , Priority.__len__` **- O(1)**
        -   `Map.__iter__ , Priority.__iter__` **- O(traverse)**
        -   `traverse` (pre, in, post, breadth) - **O(n\*log(log(u)))**
        -   `Map.put` **- O(log(log(u)))**
        -   `Map.take` **- O(log(log(u))**
        -   `Map.get` **- O(log(log(u))**
        -   `Tree.minimum` **- O(1)**
        -   `Tree.maximum` **- O(1)**
        -   `Tree.predecessor` **- O(log(log(u)))**
        -   `Tree.successor` **- O(log(log(u)))**
    -   [benchmark](./src/tree/benchmark.py)
-   [`DisjointSet` and `HashDisjointSet[T]`](./src/dset.py) **- space: O(n)**
    -   `__init__` **- O(n)**
    -   `__str__` **- O(n)**
    -   `__len__` **- O(1)**
    -   `sets` (number of unique sets) **- O(1)**
    -   `set_size` (size of a set) **- O(1)**
    -   `make_set` **O(1)**
    -   `find` **- O(1)**
    -   `union` **- O(1)**
    -   `connected` **- O(1)**
-   [Binary Index Tree (Fenwick Tree) - `BIT`](./src/bit.py) **- space: O(n)**
    -   `__init__` **- O(n)**
    -   `__str__` **- O(n)**
    -   `__len__` **- O(1)**
    -   `sum` (prefix sum) **- O(log(n))**
    -   `sum_range` (prefix sum range) **- O(log(n))**
    -   `add` **- O(log(n))**
    -   `set` **- O(log(n))**
-   [`Graph[V, E]` (adjacency list)](./src/graph/graph.py) _- see graph theory algorithms section_ **- space: O(v + e)**
    -   [factory](./src/graph/factory.py)
        -   complete
        -   random undirected
        -   random directed
        -   random undirected paired _(all vertices have even degree)_
        -   random directed paired _(all vertices have out-degree - in-degree = 0)_
        -   random directed acyclic
        -   random flow (_for max-flow/min-cut_)
    -   `__init__` **- O(1)**
    -   `__str__` **- O(v + e)**
    -   `__len__` **- O(1)**
    -   `__iter__` **- O(v)**
    -   `traverse` (depth, breadth) **- O(v + e)**
    -   `vertices` (not traverse) **- O(v)**
    -   `edges` (not traverse) **- O(v + e)**
    -   `vertices_count` **- O(1)**
    -   `edges_count` **- O(1)**
    -   `unique_edges_count` **- O(1)**
    -   `is_undirected` **- O(1)**
    -   `is_directed` **- O(1)**
    -   `has_directed_edges` **- O(1)**
    -   `has_edge_cycles` **- O(1)**
    -   `make_vertex` **- O(1)**
    -   `make_edge` **- O(1)**
    -   `get_vertex` **- O(1)**
    -   `get_edges` **- O(v + e)**
    -   `copy` **- O(v + e)**
    -   `transposed` **- O(v + e)**
    -   `adjacency_matrix` **- O(v<sup>2</sup>)**

## Graph Theory

-   [minimum spanning tree](./src/graph/mst.py)
    -   prim **- O(e\*log(v))**
    -   kruskal **- O(e\*log(v))**
    -   boruvka **- O(e\*log(v))**
-   [connectivity](./src/graph/connectivity.py)
    -   undirected graphs
        -   connected depth first search **- O(v + e)**
        -   connected breadth first search **- O(v + e)**
        -   connected disjoint set **- O(v + e)**
        -   articulations, bridges and biconnected tarjan **- O(v + e)**
    -   directed graphs
        -   strongly connected tarjan **- O(v + e)**
        -   strongly connected kosaraju **- O(v + e)**
-   [topological sorting](./src/graph/topsort.py)
    -   khan **- O(v + e)**
    -   depth first search **- O(v + e)**
    -   strongly connected tarjan _(from connectivity algorithms, used as topsort algorithm)_ **- O(v + e)**
    -   strongly connected kosaraju _(from connectivity algorithms, used as topsort algorithm)_ **- O(v + e)**
-   [path finding](./src/graph/path)
    -   [shortest path](./src/graph/path/ssp.py)
        -   directed acyclic graphs
            -   single source **- O(v + e)**
            -   single source (longest) **- O(v + e)**
        -   all graphs
            -   single source dijkstra **- O(e\*log(v))**
            -   single source dijkstra (optimized, visited + skip stale) **- O(e\*log(v))**
            -   single source bellman ford **- O(v\*e)**
            -   all pairs floyd warshall **- O(v<sup>3</sup>)**
    -   [traveling salesman problem](./src/graph/path/tsp.py)
        -   brute force **- O(v!)**
        -   held-karp bitset **- O(2<sup>v</sup>\*v<sup>2</sup>)**
        -   held-karp hashset **- O(2<sup>v</sup>\*v<sup>2</sup>)**
        -   nearest neighbors (heuristic) **- O(v<sup>2</sup>)**
    -   [eulerian cycle/path](./src/graph/path/euler.py)
        -   undirected graphs
            -   fleury **- O(e<sup>2</sup>)**
            -   hierholzer recursive **- O(v + e)**
            -   hierholzer iterative **- O(v + e)**
        -   directed graphs
            -   hierholzer recursive **- O(v + e)**
            -   hierholzer iterative **- O(v + e)**
    -   [hamiltonian cycle/path](./src/graph/path/hamilton.py)
        -   brute force _(from traveling salesman, used as hamiltonian path algorithm)_ **- O(v!)**
        -   held-karp bitset _(from traveling salesman, used as hamiltonian path algorithm)_ **- O(2<sup>v</sup>\*v<sup>2</sup>)**
        -   held-karp hashset _(from traveling salesman, used as hamiltonian path algorithm)_ **- O(2<sup>v</sup>\*v<sup>2</sup>)**
-   [max-flow/min-cut](./src/graph/maxflow)
    -   ford fulkerson
        -   depth first search **- O(f\*e)**
        -   edmonds karp **- O(v\*e<sup>2</sup>)**
        -   depth first search with capacity scaling **- O(e<sup>2</sup>\*log(u))**
        -   dinic **- O(v<sup>2</sup>\*e)**
-   [cover](./src/graph/cover)
    -   [vertex cover](./src/graph/cover/vertex.py)
        -   brute force **- O(2<sup>k</sup>\*v\*e)**
        -   greedy (heuristic) **- O(v + e)**
        -   greedy double (heuristic) **- O(v + e)**
        -   weighted brute force **- O(2<sup>v</sup>\*v\*e)**
        -   weighted greedy (heuristic) **- O(v + e)**
        -   weighted pricing method (heuristic) **- O(v + e)**
        -   weighted pricing sorted method (heuristic) **- O(e\*log(e) + v)**

## Enumeration Combinatorics

-   [factorial](./src/combinatorics/factorial.py)
    -   factorial recursive **- O(n)**
    -   factorial iterative **- O(n)**
    -   stirling's factorial approximation **- O(1)**
    -   ramanujan's factorial approximation **- O(1)**
-   [permutations](./src/combinatorics/permutations.py)
    -   count permutations **- O(n)**
    -   permutations cycles **- O(n<sup>k</sup>) ~> O(n!) when k ~ n**
    -   permutations heap **- O(n!)**
-   [combinatorics](./src/combinatorics/combinations.py)
    -   count combinations recursive **- O(min(n<sup>k</sup>, n<sup>n-k</sup>))**
    -   count combinations iterative **- O(n)**
    -   combinations **- O(n choose k)**
    -   bit combinations range **- O(n choose k)**
    -   bit combinations branch **- O(n choose k)**

## Searching Algorithms

-   [array search](./src/search/array_search.py)
    -   binary search **- O(log(n))**
    -   k-ary search **- O(k\*log<sub>k</sub>(n))**
    -   interpolation search **- O(log(log(n))) uniformly distributed arrays, worst: O(n)**
    -   exponential search **- O(log(i))**
-   [range minimum query (rmq) <-> lowest common ancestor (lca) `RangeMinimumQuery[T = Comparable]` abstract](./src/search/rmq_lca/abc.py)
    -   `__init__` **- abstract**
    -   `rmq` **- abstract**
    -   `size` **- abstract**
    -   `is_plus_minus_1` (class method) **- abstract**
    -   utility
        -   rmq to lca (CartesianTree construction) **- O(n)**
        -   lca to rmq **- O(n)**
        -   lca to rmq plus minus 1 **- O(n)**
    -   **the following rmq solving data structures can solve lca by transforming it in a rmq problem with CartesianTree**
    -   **some of the rmq solving data structures only support plus-minus-1 rmq, CartesianTree can transform rmq in plus-minus-1 rmq**
    -   [`RangeMinimumQueryNaive[T = Comparable] extends RangeMinimumQuery[T]`](./src/search/rmq_lca/naive.py) **- space: O(n<sup>2</sup>)**
        -   `RangeMinimumQuery.__init__` **- O(n<sup>2</sup>)**
        -   `RangeMinimumQuery.rmq` **- O(1)**
    -   [`RangeMinimumQueryV2[T = Comparable] extends RangeMinimumQuery[T]`](./src/search/rmq_lca/v2.py) **- space: O(n\*log(n))**
        -   `RangeMinimumQuery.__init__` **- O(n\*log(n))**
        -   `RangeMinimumQuery.rmq` **- O(1)**
    -   [`RangeMinimumQueryV3[T = Comparable] extends RangeMinimumQuery[T]`](./src/search/rmq_lca/v3.py) **- space: O(n)**
        -   `RangeMinimumQuery.__init__` **- O(n)**
        -   `RangeMinimumQuery.rmq` **- O(log(n))**
    -   [`RangeMinimumQueryV4 extends RangeMinimumQuery[int]`](./src/search/rmq_lca/v4.py) **- space: O(n)**
        -   `RangeMinimumQuery.__init__` **- O(n)**
        -   `RangeMinimumQuery.rmq` **- O(1)**
    -   [benchmark](./src/search/rmq_lca/benchmark.py)
-   [exact string search](./src/search/string_exact.py)
    -   brute force **- O(n\*p)**
    -   rabin karp **- O(n + p), worst: O(n\*p)**
    -   knuth morris pratt **- O(n + p)**
    -   baeza yates gonnet (shift-or) **- O(n + p)**
    -   boyer moore **- O(n + p)**
    -   boyer moore (optimized, extended bad char table) **- O(n + p)**
    -   aho corasick **- O(n + p)**
-   [string edit distance](./src/search/string_distance.py)
    -   brute force **- O(3<sup>n + m</sup>)**
    -   wagner fischer **- O(n\*m)**
    -   wagner fischer (optimized, reuse distance table) **- O(n\*m)**
-   [approximate/fuzzy string search](./src/search/string_fuzzy.py)
    -   sellers **- O(n\*p)**
    -   ukkonen **- O(n + (p\*min(p, d)\*c))**
    -   wu manber **- O(n\*min(p, d) + p)**
-   offline string search
    -   [`SuffixTree`](./src/search/suffix_tree.py) **- space: O(n)**
        -   `__init__ naive` **- O(n<sup>2</sup>)**
        -   `__init__ ukkonen` **- O(n)**
        -   `__str__` **- O(n<sup>2</sup>)**
        -   `occurrences` **- O(p+q)**
        -   `occurrences_count` **- O(p)**
        -   `longest_repeated_substring` **- O(n)**
        -   `longest_common_prefix` (constant time achieved using `RangeMinimumQueryV4`) **- O(1)**

## Encoding and Compression

-   [base coding](./src/encoding/base.py)
    -   base64 rfc4648 (printable) **- O(n)**
    -   base32 rfc4648 (printable) **- O(n)**
    -   base16 rfc4648 (printable) **- O(n)**
    -   ascii85 (printable) **- O(n)**
    -   base85 rfc1924 (printable) **- O(n)**
    -   base85 zeromq (printable) **- O(n)**
-   [integer coding](./src/encoding/integer.py)
    -   alphabet base (printable) **- O(log<sub>a</sub>(n))**
    -   little endian base 128 variable (non-printable, semi-compression) **- O(log<sub>128</sub>(n))**
-   [huffman coding](./src/encoding/huffman.py)
    -   huffman coding (non-printable, compression) **- O(n)**

---

## TODO

-   knapsack
-   trees: b-tree
-   linear programming: simplex
-   graph: maximum matching, edge cover, facility location
-   heaps: fibonacci heap, pairing heap
-   compression: lz77, lz78
-   string search: suffix array
