import functools
import random
import time


def random_array(size=1000, min_value=0, max_value=100000):
    return [random.randint(min_value, max_value) for i in range(size)]

def test_sort(sorter, size=1000, tries=100, check=True):
    average = 0
    for i in range(tries):
        array = random_array(size)
        start = time.time()
        array = sorter(array)
        end = time.time()
        elapsed = end - start
        average += elapsed
        print(i, end - start)
        if not check:
            continue
        for i in range(len(array) - 1):
            if array[i] > array[i + 1]:
                print('unsorted')                
                break
    print('average: ', average / tries)
