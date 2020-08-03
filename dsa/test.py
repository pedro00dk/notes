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


def benchmark(algorithms, /, *, input_str=str, output_str=str, test_inputs, bench_sizes, bench_repeat=100, bench_tries=1, bench_input, preprocess_input=None):
    """
    Benchmark on or multiple algorithms against each other.

    > generics:
    - `<T>`: type of algorithm input
    - `<U>`: type of algorithm output

    > parameters:
    - `algorithms: (str, <T> => <U>)()`: list of labels and algorithms to benchmark
    - `input_str: (<T> => str)? = str`: function to transform inputs into string
    - `output_str: (<U> => str)? = str`: function to transform outputs into string
    - `test_inputs: iter<T>`: list of inputs to display algorithms results
    - `bench_sizes: iter<V>`: list of elements that identify benchmark input sizes (usually int)
    - `bench_repeat: int? = 100`: number of times to run the benchmark (each repeat generates a new input)
    - `bench_tries: int? = 1`: number of run tries for each repeat (each trie reuses the same repeat input)
    - `bench_input: int => <T>`: function that takes input sizes and creates inputs for the algorithms
    - `preprocess_input: (<T> => <T>)? = None`: function that preprocess inputs, usually copying the input if the
        algorithm mutates it, the preprocessing runs per repeat, not trie.
    """
    print('### test')
    for input in test_inputs:
        print("# input", input_str(input))
        for label, function in algorithms:
            input = input if preprocess_input is None else preprocess_input(input)
            print(label, output_str(function(input)))
        print()
    print('### benchmark')
    for size in bench_sizes:
        print('# size:', size)
        inputs = [bench_input(size) for _ in range(bench_repeat)]
        for label, function in algorithms:
            times = []
            for input in inputs:
                input = input if preprocess_input is None else preprocess_input(input)
                time = timeit.timeit(stmt='function(input)', globals={**globals(), **locals()}, number=bench_tries)
                times.append(time)
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
    - `value_range: int => (int, int)`: function that takes input sizes and return min and max allowed values in array
    -
    """
    benchmark(
        algorithms,
        test_inputs=(
            [], [0], [*range(test_size)], [*range(test_size - 1, -1, -1)], random.sample([*range(test_size)], test_size)
        ),
        bench_sizes=bench_sizes,
        bench_repeat=bench_repeat,
        bench_input=lambda s: [random.randint(*value_range(s)) for _ in range(s)],
        preprocess_input=list.copy
    )


def heuristic_approximation(label: str, optimal_results: list, heuristic_results: list):
    """
    Helper function for computing approximations statistics of heuristics.

    > parameters:
    - `label: str`: label of the heuristic
    - `optimal_results: (int | float)[]`: optimal results (must be preprocessed into a list of integers or floats)
    - `heuristic_results: (int | float)[]`: heuristic results (must be preprocessed into a list of integers or floats)
    """
    pairs = zip(optimal_results, heuristic_results)
    approximations = [h / opt if opt != 0 else 1 for opt, h in pairs]
    print('approximation of', label)
    print('     number of runs:', len(optimal_results))
    perfect_results = sum(1 for approximation in approximations if approximation == 1)
    print('    perfect results:', perfect_results, f'{"%.2f" % (perfect_results / len(optimal_results))}%')
    print('            minimum:', min(approximations))
    print('            maximum:', max(approximations))
    print('            average:', sum(approximations) / len(approximations))
