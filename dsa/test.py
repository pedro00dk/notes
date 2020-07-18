import random
import time
import timeit


def match(operations: list):
    """
    Match operations and expected results.
    If the builtin `print` function is passed

    > parameters:
    - `operations: (any => any, any[], any?)`: function to check, arguments and expected result, which is optional
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


def benchmark(
    algorithms,  # (label, function)[]
    /, *,
    loads=None,  # load globals necessary for the algorithm to work
    test_input_iter,  # iterator the generates some inputs for initial tests
    bench_size_iter,  # iterator that generates sizes for benchmark tests
    bench_repeats=1,  # number of times to repeat each bench size (each repeat generates a new benchmark input)
    bench_tries=100,  # number of tries in each repeat (each try reuses the previous benchmark input)
    bench_input,  # function that takes size and repeat as arguments and create a new input
    test_print_input=True,  # print test input
    test_print_output=True  # print test output
):
    for load in loads if loads is not None else []:
        globals()[load.__name__] = load
    for label, function in algorithms:
        globals()[function.__name__] = function

    print('### test')
    for inp in test_input_iter:
        if test_print_input:
            print('# input:', inp)
        for label, function in algorithms:
            out = function(inp)
            if test_print_output:
                print(label, out)
    print()
    print('### benchmark')
    for s in bench_size_iter:
        print('# size:', s)
        for label, function in algorithms:
            time = 0
            for r in range(bench_repeats):
                inp = bench_input(s, r)
                time += timeit.timeit('function(inp)', globals={**globals(), **locals()}, number=bench_tries)
            print(label, time)


def sort_benchmark(
    algorithms,
    /, *,
    loads=None,
    test_size=20,  # input size for test arrays
    bench_size_iter=(0, 1, 10, 100, 1000, 10000),
    bench_repeats=100,
    value_range=lambda s: (0, s**2)  # value ranges for benchmake inputs
):
    test_input_iter = [
        [], [0], [*range(test_size)], [*range(test_size - 1, -1, -1)], random.sample([*range(test_size)], test_size)
    ]
    bench_input = lambda s, r: [random.randint(*value_range(s)) for _ in range(s)]
    benchmark(
        algorithms,
        loads=loads,
        test_input_iter=test_input_iter,
        bench_size_iter=bench_size_iter,
        bench_repeats=bench_repeats,
        bench_tries=1,
        bench_input=bench_input
    )
