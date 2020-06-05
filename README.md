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

The time complexity in **big-O** notation is shown beside the algorithms names.
Space complexity is available in the algorithms files.

--

## Enumeration Combinatorics

-   [factorial](./dsa/combinatorics/factorial.py)
    -   factorial recursive **- O(n)**
    -   factorial iterative **- O(n)**
    -   stirling's factorial approximation **- O(1)**
    -   ramanujan's factorial approximation **- O(1)**
-   [permutations](./dsa/combinatorics/permutations.py)
    -   permutations count **- O(n)**
    -   permutations using permutation cycles **- O(n\*\*k) -> O(n!) when k --> n**
    -   permutations heap algorithm recursive **- O(n!)**
    -   permutations heap algorithm iterative **- O(n!)**
-   [combinatorics](./dsa/combinatorics/combinations.py)
    -   combinations count recursive **- O(min(n\*\*k, n\*\*(n-k)))**
    -   combinations count **- O(n)**
    -   combinations recursive **- O(n choose k)**
    -   combinations iterative **- O(n choose k)**

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
    -   [bst](./dsa/tree/bst.py)
        -   put **- average: O(log(n)), worst: O(n)**
        -   take **- average: O(log(n)), worst: O(n)**
    -   [avl](./dsa/tree/avl.py)
        -   put **- O(log(n))**
        -   take **- O(log(n))**
    -   [rbt](./dsa/tree/rbt.py)
        -   put **- O(log(n))**
        -   take **- O(log(n))**
-   [binary heap](./dsa/heap/heap.py)
    -   sift up **- O(log(n))**
    -   sift down **- O(log(n))**
    -   heapify top down **- O(n\*log(n))**
    -   heapify bottom up **- O(n)**
    -   init **- O(n)**
    -   offer **- O(log(n))**
    -   poll **- O(log(n))**
    -   peek **- O(1)**
-   [k-ary heap](./dsa/heap/heap.py)
    -   sift up **- O(k\*log(n, k))**
    -   sift down **- O(k\*log(n, k))**
    -   heapify top down **- O(n\*k\*log(n, k))**
    -   heapify bottom up **- O(n)**
    -   init **- O(n)**
    -   offer **- O(k\*log(n, k))**
    -   poll **- O(k\*log(n, k))**
    -   peek **- O(1)**
