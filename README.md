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
-   [heapsort](./dsa/sort/heapsort.py) **- O(n*log(n))**
-   [mergesort](./dsa/sort/mergesort.py) **- O(n*log(n))**
-   [quicksort](./dsa/sort/quicksort.py)
    -    quicksort Hoare's partition **- average: O(n*log(n)), worst: O(n^2)**
    -    quicksort Lomuto's partition **- average: O(n*log(n)), worst: O(n^2)**
    -    quicksort dual pivot partition **- average: O(n*log(n)), worst: O(n^2)**
