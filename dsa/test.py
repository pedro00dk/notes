import random
import time
import timeit


def match(operations: list):
    """
    Match operations and expected results.
    If the builtin `print` function is passed

    > parameters:
    - `operations: (any => any, any(), any?)`: function to check, arguments and expected result, which is optional
    """
    for action, arguments, *expected in operations:
        result = action(*arguments)
        if action == print:
            print()
            continue
        print(
            action.__name__,
            f'  args: {", ".join(str(arg) for arg in arguments)}',
            f'result: {result}' if result is not None else '',
            f'expected: {expected[0]}' if len(expected) > 0 and result != expected[0] else ''
        )


def benchmark(algorithms, /, *, input_str=str, output_str=str, test_inputs, bench_sizes, bench_repeat=100, bench_tries=1, bench_input):
    """
    Benchmark on or multiple algorithms against each other.

    > parameters:
    - `algorithms: (str, <T> => <U>)()`: list of labels and algorithms to benchmark
    - `input_str: (<T> => str)? = str`: function to transform inputs into string
    - `output_str: (<U> => str)? = str`: function to transform outputs into string
    - `test_inputs: iter<T>`: list of inputs to display algorithms results
    - `bench_sizes: iter<V>`: list of elements that identify benchmark input sizes (usually int)
    - `bench_repeat: int? = 100`: number of times to run the benchmark (each repeat generates a new input)
    - `bench_tries: int? = 1`: number of run tries for each repeat (each trie reuses the same repeat input)
    - `bench_input: <V> => <T>`: function that takes input sizes and creates inputs for the algorithms
    """
    print('### test')
    for input in test_inputs:
        print("# input", input_str(input))
        for label, function in algorithms:
            print(label, output_str(function(input)))
        print()
    print('### benchmark')
    for size in bench_sizes:
        print('# size:', size)
        for label, function in algorithms:
            times = timeit.repeat(
                stmt='function(i)',
                setup='i=bench_input(size)',
                globals={**globals(), **locals()},
                repeat=bench_repeat,
                number=bench_tries
            )
            print(label, sum(times))
        print()


def sort_benchmark(algorithms, /, *, test_size=20, bench_sizes=(0, 1, 10, 100, 1000, 10000), bench_repeat=100, value_range=lambda s: (0, s**2)):
    """
    Helper benchmarking function for sorting algorithms.

    > parameters:
    - `algorithms: (str, (int | float)[] => (int | float)[])()`: list of labels and algorithms to benchmark
    - `test_size: int? = 20`: size of array to use in testing
    - `bench_sizes: iter<int>? = (0, 1, 10, 100, 1000, 10000)`: list of elements that identify benchmark input sizes
    - `bench_repeat: int? = 100`: number of times to run the benchmark (each repeat generates a new input)
    - `value_ramge: int => (int, int)`: function that takes input sizes and return min and max allowed values in array
    -
    """
    benchmark(
        algorithms,
        test_inputs=(
            [], [0], [*range(test_size)], [*range(test_size - 1, -1, -1)], random.sample([*range(test_size)], test_size)
        ),
        bench_sizes=bench_sizes,
        bench_repeat=bench_repeat,
        bench_input=lambda s: [random.randint(*value_range(s)) for _ in range(s)]
    )
