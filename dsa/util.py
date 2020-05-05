import random
import time


def match(operations):
    for action, args, expected in operations:
        result = action(*args)
        correct = result == expected
        if action.__name__ == 'print':
            print()
            continue
        print(
            action.__name__,
            '  args: ', ', '.join(str(arg) for arg in args),
            f'result: {str(result)}' if result is not None else '',
            f'expected: {expected}' if not correct else ''
        )


def benchmark(sorter, size=1000, tries=100, check=True):
    print('benchmark', sorter.__name__)
    average = 0
    for i in range(tries):
        array = [random.randint(0, size) for j in range(size)]
        start = time.time()
        array = sorter(array)
        end = time.time()
        elapsed = end - start
        average += elapsed
        is_sorted = True
        if check:
            for j in range(len(array) - 1):
                if array[i] > array[i + 1]:
                    is_sorted = False
                    break
        print('trie:', i, 'time: ', (end - start), 'not sorted' if check and not is_sorted else '')
    print('average: ', average / tries)
