# Data Structures and Algorithms

Small collection of algorithms and data structures implementations in Python.

Any file of this project must be run as a module:

```shell
cd <project-root>
$ python -m dsa.<module>.<file> # without .py

$ python -m dsa.sorting.quicksort
$ python -m dsa.tree.avl
```

#### Notes

-   I use type hints only in functions parameters, and only the simple ones.
-   Although I use simple type hints in functions, when commenting, I use a combination of python _primitives_ (`str`, `int`, `float`, etc) and typescript complex types and operators (`|`, `&`, `typeof`, `[]`, `{}`, etc), and generics (`<T extends any>`, etc), and extra syntax for tuples `(T,)`, `(<T>, <U>)` and `<T>()`.
-   Some functions such as default functions (`__len__`, `__str__`, etc) and simple functions are not commented.
-   The `n` value in most asymptotic complexity descriptions refer to the main input size, which may be an array or string size, the absolute value of a numeric parameter, the size of a data structure, etc. Other complexity variables are usually described in the comments or in the code.

---

The time complexity in **big-O** notation is shown beside algorithms names.
Space complexity is available in algorithms files.

---

## Sorting Algorithms

-   [bubblesort](./dsa/sorting/bubblesort.py) **- O(n\*\*2)**
-   [insertionsort](./dsa/sorting/insertionsort.py) **- O(n\*\*2)**
-   [selectionsort](./dsa/sorting/selectionsort.py) **- O(n\*\*2)**
-   [heapsort](./dsa/sorting/heapsort.py) **- O(n\*log(n))**
-   [mergesort](./dsa/sorting/mergesort.py) **- O(n\*log(n))**
-   [quicksort](./dsa/sorting/quicksort.py)
    -   quicksort Hoare's partition **- average: O(n\*log(n)), worst: O(n\*\*2)**
    -   quicksort Lomuto's partition **- average: O(n\*log(n)), worst: O(n\*\*2)**
    -   quicksort dual pivot partition **- average: O(n\*log(n)), worst: O(n\*\*2)**
-   [treesort](./dsa/sorting/treesort.py) _see data structures trees section_ **- O(n\*O(tree.put))**
    -   bstsort **- average: O(n\*log(n)), worst: O(n\*\*2)**
    -   avlsort **- O(n\*log(n))**
    -   rbtsort **- O(n\*log(n))**
-   [shellsort](./dsa/sorting/shellsort.py) **- O(n \* (log(n)/log(log(n)))\*\*2), for all gaps**
    -   shellsort gap Shell1959 **- O(n\*\*2)**
    -   shellsort gap FrankLazarus1960 **- O(n\*\*(3/2))**
    -   shellsort gap Hibbard1963 **- O(n\*\*(3/2))**
    -   shellsort gap PapernovStasevich1965 **- O(n\*\*(3/2))**
    -   shellsort gap Knuth1973 **- O(n\*\*(3/2))**
    -   shellsort gap Sedgewick1982 **- O(n\*\*(4/3))**
    -   shellsort gap Tokuda1992 **- unknown**
    -   shellsort gap Ciura2001 **- unknown**
-   [countingsort](./dsa/sorting/countingsort.py) **- O(n + k)**
-   [bucketsort](./dsa/sorting/bucketsort.py) **- average: O(n + (n\*\*2/k) + k), worst O(n\*\*2), best: O(n)**
-   [radixsort](./dsa/sorting/radixsort.py)
    -   radixsort least-significant-digit **- O(n\*w)**
    -   radixsort most-significant-digit **- O(n\*w)**
-   [stoogesort](./dsa/sorting/stoogesort.py) **- O(n\*\*2.7)**
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
    -   [sequence chaining hashtable](./dsa/hashtable/oa_hashtable.py)
    -   [benchmark](./dsa/hashtable/benchmark.py)
-   [graph (adjacency list)](./dsa/graph/graph.py) _- see graph theory algorithms section_
    -   [factory](./dsa/graph/factory.py)
        -   complete
        -   random undirected
        -   random directed
        -   random directed acyclic
    -   traverse depth **O(v + e)**
    -   traverse breadth **O(v + e)**
    -   traverse vertices **O(v)**
    -   traverse edges **O(v + e)**
    -   make vertex **O(1)**
    -   make edge **O(1)**
    -   copy **O(v + e)**
    -   transpose **O(v + e)**
    -   adjacency matrix **O(v\*\*2)**

## Graph Theory

-   [connectivity algorithms](./dsa/graph/connectivity.py)
    -   undirected graphs
        -   connected depth first search **- O(v + e)**
        -   connected breadth first search **- O(v + e)**
        -   connected disjoint set **- O(v + e)**
        -   articulations, bridges and biconnected tarjan **- O(v + e)**
    -   all graphs
        -   strongly connected tarjan **- O(v + e)**
        -   strongly connected kosaraju **- O(v + e)**
-   [topological sorting](./dsa/graph/topsort.py)
    -   khan **- O(v + e)**
    -   depth first search based **- O(v + e)**
    -   strongly connected tarjan _(from connectivity algorithms, used as topsort algorithm)_ **- O(v + e)**
-   [path finding](./dsa/graph/path)
    -   [shortest path](./dsa/graph/path/ssp.py)
        -   directed acyclic graphs
            -   single source **- O(v + e)**
            -   single source (longest) **- O(v + e)**
        -   all graphs
            -   single source dijkstra **- O((v + e)\*log(v))**
            -   single source bellman ford **- O(v\*e)**
            -   all pairs floyd warshall **- O(v\*\*3)**
    -   [traveling salesman problem](./dsa/graph/path/tsp.py)
        -   brute force **- O(v!)**
        -   held-karp dynamic programming bitset **- O((2\*\*v)\*(v\*\*2))**
        -   held-karp dynamic programming hashset **- O((2\*\*v)\*(v\*\*2))**
        -   nearest neighbors **- O((v\*\*2)**

## Enumeration Combinatorics

-   [factorial](./dsa/combinatorics/factorial.py)
    -   factorial recursive **- O(n)**
    -   factorial iterative **- O(n)**
    -   stirling's factorial approximation **- O(1)**
    -   ramanujan's factorial approximation **- O(1)**
-   [permutations](./dsa/combinatorics/permutations.py)
    -   permutations count **- O(n)**
    -   permutations using permutation cycles **- O(n\*\*k) => O(n!) when k ~ n**
    -   permutations heap algorithm recursive **- O(n!)**
    -   permutations heap algorithm iterative **- O(n!)**
-   [combinatorics](./dsa/combinatorics/combinations.py)
    -   combinations count recursive **- O(min(n\*\*k, n\*\*(n-k)))**
    -   combinations count **- O(n)**
    -   combinations recursive **- O(n choose k)**
    -   combinations iterative **- O(n choose k)**
    -   bit combinations recursive range **- O(n choose k)**
    -   bit combinations recursive branch **- O(n choose k)**

## Searching Algorithms

-   [array search](./dsa/linear/abc.pǛy)
    -   binary search **- O(log(n))**
    -   k-ary search **- O(k\*log(n,k))**
    -   interpolation search **- O(log(log(n))) uniformly distributed arrays, worst: O(n)**
    -   exponential search **- O(log(i)) where i is key index**
