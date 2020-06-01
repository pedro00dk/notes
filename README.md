# Data Structures and Algorithms

I did not study algorithms and data structures for a long time.
So I am making this collection for practicing purposes, and for future consultation.

Any file of this project must be run as a module:

```shell
cd <project-root>
$ python -m dsa.<category>.<file> # file without .py

$ python -m dsa.sort.quicksort
$ python -m dsa.tree.avl
```

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
    -   permutations using permutation cycles **- O(n^k) -> O(n!) when k --> n**
    -   permutations heap algorithm recursive **- O(n!)**
    -   permutations heap algorithm iterative **- O(n!)**
-   [combinatorics](./dsa/combinatorics/combinations.py)
    -   combinations count recursive **- O(min(n^k, n^(n-k)))**
    -   combinations count **- O(n)**
    -   combinations recursive **- O(n choose k)**
    -   combinations iterative **- O(n choose k)**

## Sorting Algorithms

-   [bubblesort](./dsa/sort/bubblesort.py) **- O(n^2)**
-   [insertionsort](./dsa/sort/insertionsort.py) **- O(n^2)**
-   [selectionsort](./dsa/sort/selectionsort.py) **- O(n^2)**
-   [heapsort](./dsa/sort/heapsort.py) **- O(n\*log(n))**
-   [mergesort](./dsa/sort/mergesort.py) **- O(n\*log(n))**
-   [quicksort](./dsa/sort/quicksort.py)
    -   quicksort Hoare's partition **- average: O(n\*log(n)), worst: O(n^2)**
    -   quicksort Lomuto's partition **- average: O(n\*log(n)), worst: O(n^2)**
    -   quicksort dual pivot partition **- average: O(n\*log(n)), worst: O(n^2)**
-   [shellsort](./dsa/sort/shellsort.py) **- O(n * (log(n)/log(log(n)))^2), for all gaps**
    -   shellsort gap Shell1959 **- O(n^2)**
    -   shellsort gap FrankLazarus1960 **- O(n^(3/2))**
    -   shellsort gap Hibbard1963 **- O(n^(3/2))**
    -   shellsort gap PapernovStasevich1965 **- O(n^(3/2))**
    -   shellsort gap Knuth1973 **- O(n^(3/2))**
    -   shellsort gap Sedgewick1982 **- O(n^(4/3))**
    -   shellsort gap Tokuda1992 **- unknown**
    -   shellsort gap Ciura2001 **- unknown**
-   [countingsort](./dsa/sort/countingsort.py) **- O(n + k)**
-   [bucketsort](./dsa/sort/bucketsort.py) **- average: O(n + (n^2/k) + k), worst O(n^2), best: O(n)**
-   [radixsort](./dsa/sort/radixsort.py)
    -   radixsort least-significant-digit **- O(n\*w)**
    -   radixsort most-significant-digit **- O(n\*w)**
-   [stoogesort](./dsa/sort/stoogesort.py) **- O(n^2.7)**
-   [slowsort](./dsa/sort/slowsort.py) **- O(T(n)), where T(n) = T(n-1) + T(n/2)\*2 + 1**
-   [bogosort](./dsa/sort/bogosort.py)
    -   bogosort random **- unbounded**
    -   bogosort deterministic **- O((n + 1)!)**
