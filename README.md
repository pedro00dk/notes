# Notes - Data Structures and Algorithms

Collection of data structures and algorithms implemented in Python.

The minimum python version required is 3.8.
Scripts of this project must be run as a module:

```shell
cd <project-root>
$ python -m dsa.<module>.<file> # without .py

$ # examples:
$ python -m dsa.sorting.quicksort
$ python -m dsa.tree.avl
$ python -m dsa.graph.path.ssp
```

#### Notes

-   Functions have basic type hints, the docstring contains a better specification of parameters and return value types.
-   A combination of python basic types (`str`, `int`, `float`, etc) and typescript type operators (`|`, `&`, `typeof`, `[]`, `{}`, etc), generics (`<T extends any>`, etc), and extra syntax for tuples `(T,)`, `(<T>, <U>)`, `<T>()` is used to specify types.
-   The `n` value in most asymptotic complexity descriptions refer to the main input size, which may be an array or string size, the absolute value of a numeric parameter, the size of a data structure, etc. Other complexity variables are usually described in the comments or in the code.

---

The time complexity in **big-O** notation is shown beside algorithms names.
Space complexity is available in algorithms files.

---

## Sorting Algorithms

-   [bubblesort](./dsa/sorting/bubblesort.py) **- O(n<sup>2</sup>)**
-   [insertionsort](./dsa/sorting/insertionsort.py) **- O(n<sup>2</sup>)**
-   [selectionsort](./dsa/sorting/selectionsort.py) **- O(n<sup>2</sup>)**
-   [heapsort](./dsa/sorting/heapsort.py) **- O(n\*log(n))**
-   [mergesort](./dsa/sorting/mergesort.py) **- O(n\*log(n))**
-   [quicksort](./dsa/sorting/quicksort.py)
    -   quicksort Hoare's partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   quicksort Lomuto's partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   quicksort dual pivot partition **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
-   [treesort](./dsa/sorting/treesort.py) _see data structures trees section_ **- O(n\*O(tree.put))**
    -   bstsort **- average: O(n\*log(n)), worst: O(n<sup>2</sup>)**
    -   avlsort **- O(n\*log(n))**
    -   rbtsort **- O(n\*log(n))**
-   [shellsort](./dsa/sorting/shellsort.py)
    -   Shell1959 **- O(n<sup>2</sup>)**
    -   FrankLazarus1960 **- O(n<sup>3/2</sup>)**
    -   Hibbard1963 **- O(n<sup>3/2</sup>)**
    -   PapernovStasevich1965 **- O(n<sup>3/2</sup>)**
    -   Knuth1973 **- O(n<sup>3/2</sup>)**
    -   Sedgewick1982 **- O(n<sup>4/3</sup>)**
    -   Tokuda1992 **- unknown**
    -   Ciura2001 **- unknown**
-   [countingsort](./dsa/sorting/countingsort.py) **- O(n + k)**
-   [bucketsort](./dsa/sorting/bucketsort.py) **- average: O(n + (n<sup>2</sup>/k) + k), worst O(n<sup>2</sup>), best: O(n)**
-   [radixsort](./dsa/sorting/radixsort.py)
    -   radixsort least-significant-digit **- O(n\*w)**
    -   radixsort most-significant-digit **- O(n\*w)**
-   [stoogesort](./dsa/sorting/stoogesort.py) **- O(n<sup>2.7</sup>)**
-   [slowsort](./dsa/sorting/slowsort.py) **- O(T(n)), where T(n) = T(n-1) + T(n/2)\*2 + 1**
-   [bogosort](./dsa/sorting/bogosort.py)
    -   bogosort random **- unbounded**
    -   bogosort deterministic **- O((n + 1)!)**

## Data Structures

-   [linear (base class)](./dsa/linear/abc.py)
    -   traversal **- O(n)**
    -   value index **- O(n)**
    -   contains value **- O(n)**
    -   [linked list (double)](./dsa/linear/list.py)
        -   push **- O(n)**
        -   pop (index deletion) **- O(n)**
        -   remove (value deletion) **- O(n)**
        -   get (index) **- O(n)**
        -   reverse **- O(n)**
    -   [queue](./dsa/linear/queue.py)
        -   offer **- O(1)**
        -   poll **- O(1)**
        -   peek **- O(1)**
    -   [stack](./dsa/linear/stack.py)
        -   push **- O(1)**
        -   pop **- O(1)**
        -   peek **- O(1)**
-   [tree (base class)](./dsa/tree/abc.py)
    -   traversal **- O(n)**
    -   get **- average or balanced trees: O(log(n)), worst: O(n)**
    -   contains key **- average or balanced trees: O(log(n)), worst: O(n)**
    -   contains value **- O(n)**
    -   ancestor **- average or balanced trees: O(log(n)), worst: O(n)**
    -   successor **- average or balanced trees: O(log(n)), worst: O(n)**
    -   minimum **- average or balanced trees: O(log(n)), worst: O(n)**
    -   maximum **- average or balanced trees: O(log(n)), worst: O(n)**
    -   [binary search tree](./dsa/tree/bst.py)
        -   put **- average: O(log(n)), worst: O(n)**
        -   take **- average: O(log(n)), worst: O(n)**
    -   [avl tree (with ranks)](./dsa/tree/avl.py)
        -   put **- O(log(n))**
        -   take **- O(log(n))**
    -   [red-black tree](./dsa/tree/rbt.py)
        -   put **- O(log(n))**
        -   take **- O(log(n))**
    -   [benchmark](./dsa/tree/benchmark.py)
-   [heap (base class)](./dsa/heap/abc.py)
    -   peek **- O(1)**
    -   [binary heap](./dsa/heap/heap.py)
        -   sift up **- O(log(n))**
        -   sift down **- O(log(n))**
        -   heapify top down **- O(n\*log(n))**
        -   heapify bottom up **- O(n)**
        -   init **- O(n)**
        -   offer **- O(log(n))**
        -   poll **- O(log(n))**
    -   [k-ary heap](./dsa/heap/kheap.py)
        -   sift up **- O(k\*log(n,k))**
        -   sift down **- O(k\*log(n,k))**
        -   heapify top down **- O(n\*k\*log(n,k))**
        -   heapify bottom up **- O(n)**
        -   init **- O(n)**
        -   offer **- O(k\*log(n,k))**
        -   poll **- O(k\*log(n,k))**
    -   [benchmark](./dsa/heap/benchmark.py)
-   [disjoint set](./dsa/dset.py)
    -   implemented:
        -   Numeric keys disjoint set
        -   Hashed keys disjoint set
    -   init **- O(n)**
    -   make set **- O(1)**
    -   find **- O(1)**
    -   union **- O(1)**
    -   connected **- O(1)**
-   [binary index tree (fenwick tree)](./dsa/bit.py)
    -   init **- O(n)**
    -   prefix sum **- O(log(n))**
    -   prefix sum range **- O(log(n))**
    -   add **- O(log(n))**
    -   set **- O(log(n))**
-   [hashtable (base class)](./dsa/hashtable/abc.py)
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
    -   [open addressing hashtable](./dsa/hashtable/oa_hashtable.py)
    -   [sequence chaining hashtable](./dsa/hashtable/sc_hashtable.py)
    -   [benchmark](./dsa/hashtable/benchmark.py)
-   [graph (adjacency list)](./dsa/graph/graph.py) _- see graph theory algorithms section_
    -   [factory](./dsa/graph/factory.py)
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

-   [minimum spanning tree](./dsa/graph/mst.py)
    -   prim **- O(e\*log(v))**
    -   kruskal **- O(e\*log(v))**
    -   boruvka **- O(e\*log(v))**
-   [connectivity](./dsa/graph/connectivity.py)
    -   undirected graphs
        -   connected depth first search **- O(v + e)**
        -   connected breadth first search **- O(v + e)**
        -   connected disjoint set **- O(v + e)**
        -   articulations, bridges and biconnected tarjan **- O(v + e)**
    -   directed graphs
        -   strongly connected tarjan **- O(v + e)**
        -   strongly connected kosaraju **- O(v + e)**
-   [topological sorting](./dsa/graph/topsort.py)
    -   khan **- O(v + e)**
    -   depth first search **- O(v + e)**
    -   strongly connected tarjan _(from connectivity algorithms, used as topsort algorithm)_ **- O(v + e)**
    -   strongly connected kosaraju _(from connectivity algorithms, used as topsort algorithm)_ **- O(v + e)**
-   [path finding](./dsa/graph/path)
    -   [shortest path](./dsa/graph/path/ssp.py)
        -   directed acyclic graphs
            -   single source **- O(v + e)**
            -   single source (longest) **- O(v + e)**
        -   all graphs
            -   single source dijkstra **- O(e\*log(v))**
            -   single source dijkstra (optimized, visited + skip stale) **- O(e\*log(v))**
            -   single source bellman ford **- O(v\*e)**
            -   all pairs floyd warshall **- O(v<sup>3</sup>)**
    -   [traveling salesman problem](./dsa/graph/path/tsp.py)
        -   brute force **- O(v!)**
        -   held-karp bitset **- O(2<sup>v</sup>\*v<sup>2</sup>)**
        -   held-karp hashset **- O(2<sup>v</sup>\*v<sup>2</sup>)**
        -   nearest neighbors (heuristic) **- O(v<sup>2</sup>)**
    -   [eulerian cycle/path](./dsa/graph/path/euler.py)
        -   undirected graphs
            -   fleury **- O(e<sup>2</sup>)**
            -   hierholzer recursive **- O(v + e)**
            -   hierholzer iterative **- O(v + e)**
        -   directed graphs
            -   hierholzer recursive **- O(v + e)**
            -   hierholzer iterative **- O(v + e)**
    -   [hamiltonian cycle/path](./dsa/graph/path/hamilton.py)
        -   brute force _(from traveling salesman, used as hamiltonian path algorithm)_ **- O(v!)**
        -   held-karp bitset _(from traveling salesman, used as hamiltonian path algorithm)_ **- O(2<sup>v</sup>\*v<sup>2</sup>)**
        -   held-karp hashset _(from traveling salesman, used as hamiltonian path algorithm)_ **- O(2<sup>v</sup>\*v<sup>2</sup>)**
-   [max-flow/min-cut](./dsa/graph/maxflow)
    -   ford fulkerson
        -   depth first search **- O(f\*e)**
        -   edmonds karp **- O(v\*e<sup>2</sup>)**
        -   depth first search with capacity scaling **- O(e<sup>2</sup>\*log(u))**
        -   dinic **- O(v<sup>2</sup>\*e)**
-   [cover](./dsa/graph/cover)
    -   [vertex cover](./dsa/graph/cover/vertex.py)
        -   brute force **- O(2<sup>k</sup>\*v\*e)**
        -   greedy (heuristic) **- O(v + e)**
        -   greedy double (heuristic) **- O(v + e)**
        -   weighted brute force **- O(2<sup>v</sup>\*v\*e)**
        -   weighted greedy (heuristic) **- O(v + e)**
        -   weighted pricing method (heuristic) **- O(v + e)**
        -   weighted pricing sorted method (heuristic) **- O(e\*log(e) + v)**

## Enumeration Combinatorics

-   [factorial](./dsa/combinatorics/factorial.py)
    -   factorial recursive **- O(n)**
    -   factorial iterative **- O(n)**
    -   stirling's factorial approximation **- O(1)**
    -   ramanujan's factorial approximation **- O(1)**
-   [permutations](./dsa/combinatorics/permutations.py)
    -   count permutations **- O(n)**
    -   permutations cycles **- O(n<sup>k</sup>) ~> O(n!) when k ~ n**
    -   permutations heap **- O(n!)**
-   [combinatorics](./dsa/combinatorics/combinations.py)
    -   count combinations recursive **- O(min(n<sup>k</sup>, n<sup>n-k</sup>))**
    -   count combinations iterative **- O(n)**
    -   combinations **- O(n choose k)**
    -   bit combinations range **- O(n choose k)**
    -   bit combinations branch **- O(n choose k)**

## Searching Algorithms

-   [array search](./dsa/search/array_search.py)
    -   binary search **- O(log(n))**
    -   k-ary search **- O(k\*log(n,k))**
    -   interpolation search **- O(log(log(n))) uniformly distributed arrays, worst: O(n)**
    -   exponential search **- O(log(i))**
-   [string search](./dsa/search/string_search.py)
    -   exact brute force **- O(n\*p)**
    -   exact rabin karp **- O(n + p), worst: O(n\*p)**
    -   exact knuth morris pratt **- O(n + p)**
    -   exact baeza yates gonnet (shift-or) **- O(n + p)**
    -   exact boyer moore **- O(n + p)**
    -   exact boyer moore (optimized, extended bad char table) **- O(n + p)**
    <!-- -   exact multi-pattern aho-corasick **- O(n + p)** -->


---

## TODO

-   knapsack
-   trees: b-tree
-   linear programming: simplex
-   graph: maximum matching, edge cover, facility location
-   heaps: fibonacci heap, pairing heap
-   encoding: base32, base64
-   compression: lz77, lz78
-   string search: aho corasick, sellers, ukkonen
-   indexing: suffix array, suffix tree


