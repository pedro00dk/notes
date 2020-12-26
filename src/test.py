import mmap
import random
import timeit
from typing import Any, Callable, Optional, TypeVar, Union

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')
CheckedOperation = tuple[Callable[..., Any], tuple[Any, ...], Any]
UncheckedOperation = tuple[Callable[..., Any], tuple[Any, ...]]
Operation = Union[CheckedOperation, UncheckedOperation]
AnyBytes = Union[bytes, bytearray, memoryview, mmap.mmap]


def match(operations: tuple[Operation, ...]):
    """
    Execution functions and compare their results with a expected value.
    The expected value may not be passed.

    > parameters
    - `operations`: iterable containing tuples with function to execute, arguments and an optional expected result
    """
    for action, arguments, *expected in operations:
        result = action(*arguments)
        if action is print:
            print()
            continue
        print(
            action.__name__,
            f'  args: {", ".join(str(arg) for arg in arguments)}',
            f'result: {result}' if result is not None else '',
            f'expected: {expected[0]}' if len(expected) > 0 and result != expected[0] else '',
        )


def benchmark(
    algorithms: tuple[tuple[str, Callable[[T], U]], ...],
    test_inputs: tuple[T, ...],
    bench_sizes: tuple[V, ...],
    bench_input: Callable[[V], T],
    bench_repeat: int = 100,
    bench_tries: int = 1,
    input_str: Callable[[T], str] = str,
    output_str: Callable[[U], str] = str,
    preprocess_input: Optional[Callable[[T], T]] = None,
):
    """
    Benchmark one or multiple algorithms against each other.

    > parameters
    - `algorithms`: labeled algorithms to benchmark
    - `test_inputs`: inputs to display algorithms results
    - `bench_sizes`: elements that identify benchmark input sizes (usually int)
    - `bench_repeat`: number of times to run the benchmark (each run generates a new input)
    - `bench_tries`: number of run tries for each repeat (each run uses the same input)
    - `bench_input`: function that takes input sizes and creates inputs for the algorithms
    - `input_str`: function to transform inputs into string
    - `output_str`: function to transform outputs into string
    - `preprocess_input`: function that preprocess inputs, usually copying the input if the algorithm mutates it, the
        preprocessing runs per repeat, not trie
    """
    print('### test')
    for input in test_inputs:
        print("# input", input_str(input))
        for label, function in algorithms:
            input = input if preprocess_input is None else preprocess_input(input)
            output = function(input)
            print(label, output_str(output))
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


def sort_benchmark(
    algorithms: tuple[tuple[str, Callable[[list[float]], list[float]]], ...],
    test_size: int = 20,
    bench_sizes: tuple[int, ...] = (0, 1, 10, 100, 1000, 10000),
    bench_repeat: int = 100,
    value_range: Callable[[int], tuple[int, int]] = lambda s: (0, s**2)
):
    """
    Benchmark one or multiple sorting algorithms against each other.

    > parameters
    - `algorithms`: labeled algorithms to benchmark
    - `test_size`: size of array to use in testing
    - `bench_sizes`: benchmark input sizes
    - `bench_repeat`: number of times to run the benchmark
    - `value_range`: function that takes input sizes and return min and max allowed input values
    """
    benchmark(
        algorithms,
        ([], [0], [*range(test_size)], [*range(test_size - 1, -1, -1)], random.sample([*range(test_size)], test_size)),
        bench_sizes,
        lambda size: [random.randint(*value_range(size)) for _ in range(size)],
        bench_repeat,
        preprocess_input=list[float].copy
    )


def heuristic_approximation(label: str, optimal_results: list[float], heuristic_results: list[float]):
    """
    Compute approximations of heuristic algorithms given the optimal and heuristic results.

    > parameters
    - `label`: label of the heuristic
    - `optimal_results`: optimal results, must be preprocessed into a list of integers or floats
    - `heuristic_results`: heuristic results, must be preprocessed into a list of integers or floats
    """
    pairs = zip(optimal_results, heuristic_results)
    approximations = [h / opt if opt != 0 else 1 for opt, h in pairs]
    perfect_results = sum(1 for approximation in approximations if approximation == 1)
    print('# heuristic ', label)
    print('   number of runs:', len(optimal_results))
    print('  perfect results:', perfect_results, f'{"%.2f" % (perfect_results / len(optimal_results) * 100)}%')
    print('          minimum:', min(approximations))
    print('          maximum:', max(approximations))
    print('          average:', sum(approximations) / len(approximations))


def read(
    *,
    path: Optional[str] = None,
    string: Optional[str] = None,
    byte: Optional[Union[bytes, bytearray]] = None
) -> tuple[AnyBytes, Callable[[], Any]]:
    """
    Returns an indexable bytes object from a file path, string, bytes or bytearray, this function allows running
    searching algorithms in any of these types.
    Only one of the parameters should be provided.

    If a file is provided, it is assumed to use the `utf-8` encoding.
    An immutable `mmap.mmap` is returned (works like `bytearray`).

    If a string is provided, it is converted to `bytes` using `utf-8` encoding (requires copying).

    > parameters
    - `path`: path to a file
    - `string`: string to be converted to bytes like
    - `byte`: a bytes-like object
    - `return`: buffer to access mmap, string, bytes or bytearray, and a finalize function to close resources
    """
    if path is not None:
        reader = open(path, 'rb')
        mm = mmap.mmap(reader.fileno(), 0, prot=mmap.PROT_READ)
        return mm, lambda: (mm.close(), reader.close())
    if string is not None:
        return bytes(string, 'utf-8'), lambda: ()
    if byte is not None:
        return byte, lambda: ()
    raise Exception('no source was provided')
