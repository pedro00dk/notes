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
    -   quicksort Hoare's partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   quicksort Lomuto's partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   quicksort dual pivot partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
-   [treesort](./src/sorting/treesort.py) _see data structures trees section_ **- O(n\*O(tree.put))**
    -   bstsort **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   avlsort **- O(n\*log(n))**
    -   rbtsort **- O(n\*log(n))**
-   [shellsort](./src/sorting/shellsort.py)
    -   Shell1959 **- O(n<sup>2</sup>)**
    -   FrankLazarus1960 **- O(n<sup>3/2</sup>)**
    -   Hibbard1963 **- O(n<sup>3/2</sup>)**
    -   PapernovStasevich1965 **- O(n<sup>3/2</sup>)**
    -   Knuth1973 **- O(n<sup>3/2</sup>)**
    -   Sedgewick1982 **- O(n<sup>4/3</sup>)**
    -   Tokuda1992 **- unknown**
    -   Ciura2001 **- unknown**
-   [countingsort](./src/sorting/countingsort.py) **- O(n + k)**
-   [bucketsort](./src/sorting/bucketsort.py) **- average: O(n + (n<sup>2</sup>/k) + k), worst O(n<sup>2</sup>), best: O(n)**
-   [radixsort](./src/sorting/radixsort.py)
    -   radixsort least-significant-digit **- O(n\*w)**
    -   radixsort most-significant-digit **- O(n\*w)**
-   [stoogesort](./src/sorting/stoogesort.py) **- O(n<sup>2.7</sup>)**
-   [slowsort](./src/sorting/slowsort.py) **- O(T(n)), where T(n) = T(n-1) + T(n/2)\*2 + 1**
-   [bogosort](./src/sorting/bogosort.py)
    -   bogosort random **- unbounded**
    -   bogosort deterministic **- O((n + 1)!)**

## Data Structures

-   [linear (base class)](./src/linear/abc.py)
    -   traversal **- O(n)**
    -   value index **- O(n)**
    -   contains value **- O(n)**
    -   [linked list (double)](./src/linear/list.py)
        -   push **- O(n)**
        -   pop (index deletion) **- O(n)**
        -   remove (value deletion) **- O(n)**
        -   get (index) **- O(n)**
        -   reverse **- O(n)**
    -   [queue](./src/linear/queue.py)
        -   offer **- O(1)**
        -   poll **- O(1)**
        -   peek **- O(1)**
    -   [stack](./src/linear/stack.py)
        -   push **- O(1)**
        -   pop **- O(1)**
        -   peek **- O(1)**
-   [tree (base class)](./src/tree/abc.py)
    -   traversal **- O(n)**
    -   get **- average or balanced trees: O(log(n)), worst: O(n)**
    -   contains key **- average or balanced trees: O(log(n)), worst: O(n)**
    -   contains value **- O(n)**
    -   ancestor **- average or balanced trees: O(log(n)), worst: O(n)**
    -   successor **- average or balanced trees: O(log(n)), worst: O(n)**
    -   minimum **- average or balanced trees: O(log(n)), worst: O(n)**
    -   maximum **- average or balanced trees: O(log(n)), worst: O(n)**
    -   [binary search tree](./src/tree/bst.py)
        -   put **- average: O(log(n)), worst: O(n)**
        -   take **- average: O(log(n)), worst: O(n)**
    -   [avl tree (with ranks)](./src/tree/avl.py)
        -   put **- O(log(n))**
        -   take **- O(log(n))**
    -   [red-black tree](./src/tree/rbt.py)
        -   put **- O(log(n))**
        -   take **- O(log(n))**
    -   [benchmark](./src/tree/benchmark.py)
-   [heap (base class)](./src/heap/abc.py)
    -   peek **- O(1)**
    -   [binary heap](./src/heap/heap.py)
        -   sift up **- O(log(n))**
        -   sift down **- O(log(n))**
        -   heapify top down **- O(n\*log(n))**
        -   heapify bottom up **- O(n)**
        -   init **- O(n)**
        -   offer **- O(log(n))**
        -   poll **- O(log(n))**
    -   [k-ary heap](./src/heap/kheap.py)
        -   sift up **- O(k\*log(n,k))**
        -   sift down **- O(k\*log(n,k))**
        -   heapify top down **- O(n\*k\*log(n,k))**
        -   heapify bottom up **- O(n)**
        -   init **- O(n)**
        -   offer **- O(k\*log(n,k))**
        -   poll **- O(k\*log(n,k))**
    -   [benchmark](./src/heap/benchmark.py)
-   [disjoint set](./src/dset.py)
    -   implemented:
        -   Numeric keys disjoint set
        -   Hashed keys disjoint set
    -   init **- O(n)**
    -   make set **- O(1)**
    -   find **- O(1)**
    -   union **- O(1)**
    -   connected **- O(1)**
-   [binary index tree (fenwick tree)](./src/bit.py)
    -   init **- O(n)**
    -   prefix sum **- O(log(n))**
    -   prefix sum range **- O(log(n))**
    -   add **- O(log(n))**
    -   set **- O(log(n))**
-   [hashtable (base class)](./src/hashtable/abc.py)
    -   implemented probers:
        -   Linear Probing
        -   Quadratic Prime Probing
        -   Quadratic Triangular Probing
    -   traversal **- O(n)**
    -   put **- O(1) amortized**
    -   take **- O(1) amortized**
    -   get **- O(1)**
    -   contains key **O(1)**
    -   contains value **- O(n)**
    -   [open addressing hashtable](./src/hashtable/oa_hashtable.py)
    -   [sequence chaining hashtable](./src/hashtable/sc_hashtable.py)
    -   [benchmark](./src/hashtable/benchmark.py)
-   [graph (adjacency list)](./src/graph/graph.py) _- see graph theory algorithms section_
    -   [factory](./src/graph/factory.py)
        -   complete
        -   random undirected
        -   random directed
        -   random undirected paired _(all vertices have even degree)_
        -   random directed paired _(all vertices have out-degree - in-degree = 0)_
        -   random directed acyclic
        -   random flow _(for max-flow/min-cut)_
    -   traverse depth **O(v + e)**
    -   traverse breadth **O(v + e)**
    -   traverse vertices **O(v)**
    -   traverse edges **O(v + e)**
    -   make vertex **O(1)**
    -   make edge **O(1)**
    -   copy **O(v + e)**
    -   transpose **O(v + e)**
    -   adjacency matrix **O(v<sup>2</sup>)**

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
    -   k-ary search **- O(k\*log(n,k))**
    -   interpolation search **- O(log(log(n))) uniformly distributed arrays, worst: O(n)**
    -   exponential search **- O(log(i))**
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

## Encoding and Compression

-   [base coding](./src/encoding/base.py)
    -   base64 rfc4648 (printable) **- O(n)**
    -   base32 rfc4648 (printable) **- O(n)**
    -   base16 rfc4648 (printable) **- O(n)**
    -   ascii85 (printable) **- O(n)**
    -   base85 rfc1924 (printable) **- O(n)**
    -   base85 zeromq (printable) **- O(n)**
-   [integer coding](./src/encoding/integer.py)
    -   alphabet base (printable) **- O(log(n))**
    -   little endian base 128 variable (non-printable, semi-compression) **- O(log(n))**
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
-   string search, sellers, ukkonen
-   indexing: suffix array, suffix tree
