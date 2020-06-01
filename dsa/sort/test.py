from random import randint, sample
from timeit import repeat


def test(algorithms: list, /, print_tests: list = None, benchmark_tests: list = None, array_min: str = '-i**2', array_max='i**2', tries: list = 100):
    """
    Function for testing and benchmarking algorithms.
    """
    for _, function, _ in algorithms:
        globals()[function.__name__] = function
    print_tests = print_tests if print_tests is not None else \
        [[], [0], [*range(20)], [*range(20 - 1, -1, -1)], sample([*range(20)], 20)]
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
            results = repeat(
                timeit_function,
                setup=f'array=[randint({array_min}, {array_max}) for _ in range(i)]',
                globals={**globals(), **locals()},
                number=1,
                repeat=100
            )
            print(label, sum(results))
