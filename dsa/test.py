import random
import time
import timeit


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
            f'result: {result}' if result is not None else '',
            f'expected: {expected}' if not correct else ''
        )


def benchmark(algorithms: list, /, loads: list = None, print_tests: list = None, print_length: int = 20, benchmark_tests: list = None, array_min: str = '-i**2', array_max='i**2', tries: list = 100):
    """
    Function for testing and benchmarking sorting algorithms.
    """
    for load in loads if loads is not None else []:
        globals()[load.__name__] = load
    for _, function, _ in algorithms:
        globals()[function.__name__] = function
    print_tests = print_tests if print_tests is not None else \
        [
            [],
            [0],
            [*range(print_length)],
            [*range(print_length - 1, -1, -1)],
            random.sample([*range(print_length)], print_length)
        ]
    benchmark_tests = benchmark_tests if benchmark_tests is not None else [0, 1, 10, 100, 1000, 10000]
    print('print tests')
    for array in print_tests:
        print('array:', array)
        for label, function, timeit_function in algorithms:
            print(label, function([*array]))
    print('benchmark tests')
    for i in benchmark_tests:
        print('array length:', i)
        for label, function, timeit_function in algorithms:
            results = timeit.repeat(
                timeit_function,
                setup=f'array=[random.randint({array_min}, {array_max}) for _ in range(i)]',
                globals={**globals(), **locals()},
                number=1,
                repeat=tries
            )
            print(label, sum(results))
